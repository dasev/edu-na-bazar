"""
Route Optimizer Service - оптимизация маршрутов доставки
Использует Yandex Routes API для расчета кратчайшего маршрута
"""
import httpx
import asyncio
from typing import List, Dict, Tuple
from itertools import permutations


class RouteOptimizer:
    """Сервис оптимизации маршрутов доставки"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or "your-yandex-api-key"  # Получить на https://developer.tech.yandex.ru/
        self.base_url = "https://api.routing.yandex.net/v2/route"
    
    async def calculate_route(
        self, 
        waypoints: List[Tuple[float, float]]
    ) -> Dict:
        """
        Рассчитать маршрут через несколько точек
        
        Args:
            waypoints: Список координат [(lat, lon), ...]
            
        Returns:
            Dict с distance (км), duration (мин), geometry
        """
        if len(waypoints) < 2:
            return {"distance": 0, "duration": 0, "geometry": None}
        
        # Формируем параметры запроса
        points = []
        for lat, lon in waypoints:
            points.append(f"{lon},{lat}")  # Yandex использует lon,lat
        
        params = {
            "apikey": self.api_key,
            "waypoints": "|".join(points),
            "mode": "driving",  # или "walking", "transit"
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(self.base_url, params=params, timeout=10.0)
                
                if response.status_code == 200:
                    data = response.json()
                    route = data.get("route", {})
                    
                    # Извлекаем метрики
                    distance_meters = route.get("distance", {}).get("value", 0)
                    duration_seconds = route.get("duration", {}).get("value", 0)
                    geometry = route.get("geometry", {}).get("selection", "")
                    
                    return {
                        "distance": distance_meters / 1000,  # в км
                        "duration": duration_seconds / 60,  # в минутах
                        "geometry": geometry
                    }
                else:
                    print(f"Yandex API error: {response.status_code}")
                    return {"distance": 0, "duration": 0, "geometry": None}
                    
        except Exception as e:
            print(f"Route calculation error: {e}")
            return {"distance": 0, "duration": 0, "geometry": None}
    
    async def optimize_waypoints(
        self,
        start_point: Tuple[float, float],
        waypoints: List[Tuple[float, float]],
        end_point: Tuple[float, float]
    ) -> Dict:
        """
        Оптимизировать порядок посещения точек (решение TSP)
        
        Args:
            start_point: Начальная точка (склад/курьер)
            waypoints: Промежуточные точки (магазины)
            end_point: Конечная точка (покупатель)
            
        Returns:
            Dict с optimized_order, distance, duration, geometry
        """
        if len(waypoints) == 0:
            # Прямой маршрут от старта до конца
            route = await self.calculate_route([start_point, end_point])
            return {
                "optimized_order": [],
                "distance": route["distance"],
                "duration": route["duration"],
                "geometry": route["geometry"]
            }
        
        if len(waypoints) <= 3:
            # Для малого количества точек - перебор всех вариантов
            best_route = None
            best_distance = float('inf')
            best_order = None
            
            for perm in permutations(range(len(waypoints))):
                # Формируем маршрут: старт → точки в порядке perm → конец
                route_points = [start_point]
                route_points.extend([waypoints[i] for i in perm])
                route_points.append(end_point)
                
                route = await self.calculate_route(route_points)
                
                if route["distance"] < best_distance:
                    best_distance = route["distance"]
                    best_route = route
                    best_order = list(perm)
            
            return {
                "optimized_order": best_order,
                "distance": best_route["distance"],
                "duration": best_route["duration"],
                "geometry": best_route["geometry"]
            }
        else:
            # Для большого количества - жадный алгоритм (ближайший сосед)
            return await self._greedy_tsp(start_point, waypoints, end_point)
    
    async def _greedy_tsp(
        self,
        start_point: Tuple[float, float],
        waypoints: List[Tuple[float, float]],
        end_point: Tuple[float, float]
    ) -> Dict:
        """Жадный алгоритм для TSP (ближайший сосед)"""
        unvisited = list(range(len(waypoints)))
        current = start_point
        order = []
        
        # Посещаем ближайшую непосещенную точку
        while unvisited:
            nearest_idx = None
            nearest_dist = float('inf')
            
            for idx in unvisited:
                # Упрощенное расстояние (Евклидово)
                dist = self._euclidean_distance(current, waypoints[idx])
                if dist < nearest_dist:
                    nearest_dist = dist
                    nearest_idx = idx
            
            order.append(nearest_idx)
            current = waypoints[nearest_idx]
            unvisited.remove(nearest_idx)
        
        # Рассчитываем финальный маршрут
        route_points = [start_point]
        route_points.extend([waypoints[i] for i in order])
        route_points.append(end_point)
        
        route = await self.calculate_route(route_points)
        
        return {
            "optimized_order": order,
            "distance": route["distance"],
            "duration": route["duration"],
            "geometry": route["geometry"]
        }
    
    @staticmethod
    def _euclidean_distance(p1: Tuple[float, float], p2: Tuple[float, float]) -> float:
        """Евклидово расстояние между двумя точками"""
        return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5


# Пример использования:
# optimizer = RouteOptimizer(api_key="your-key")
# result = await optimizer.optimize_waypoints(
#     start_point=(55.75, 37.61),  # Склад
#     waypoints=[(55.76, 37.62), (55.77, 37.63)],  # Магазины
#     end_point=(55.78, 37.64)  # Покупатель
# )
