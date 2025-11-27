"""
Простой скрипт для добавления тестовых товаров
"""
import asyncio
import asyncpg
import requests
import uuid
from pathlib import Path
import random

DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/edu_na_bazar"

# Тестовые товары по категориям
PRODUCTS_BY_CATEGORY = {
    "Овощи и фрукты": [
        {"name": "Помидоры свежие", "price": 150, "unit": "кг", "image_url": "https://images.unsplash.com/photo-1546094096-0df4bcaaa337?w=800"},
        {"name": "Огурцы парниковые", "price": 120, "unit": "кг", "image_url": "https://images.unsplash.com/photo-1604977042946-1eecc30f269e?w=800"},
        {"name": "Картофель молодой", "price": 80, "unit": "кг", "image_url": "https://images.unsplash.com/photo-1518977676601-b53f82aba655?w=800"},
        {"name": "Морковь отборная", "price": 70, "unit": "кг", "image_url": "https://images.unsplash.com/photo-1598170845058-32b9d6a5da37?w=800"},
        {"name": "Свекла столовая", "price": 60, "unit": "кг", "image_url": "https://images.unsplash.com/photo-1590165482129-1b8b27698780?w=800"},
        {"name": "Капуста белокочанная", "price": 50, "unit": "кг", "image_url": "https://images.unsplash.com/photo-1594282486552-05b4d80fbb9f?w=800"},
        {"name": "Перец болгарский", "price": 200, "unit": "кг", "image_url": "https://images.unsplash.com/photo-1563565375-f3fdfdbefa83?w=800"},
        {"name": "Баклажаны", "price": 180, "unit": "кг", "image_url": "https://images.unsplash.com/photo-1659261200833-ec8761558af7?w=800"},
        {"name": "Кабачки", "price": 90, "unit": "кг", "image_url": "https://images.unsplash.com/photo-1597362925123-77861d3fbac7?w=800"},
        {"name": "Лук репчатый", "price": 40, "unit": "кг", "image_url": "https://images.unsplash.com/photo-1618512496248-a07fe83aa8cb?w=800"},
    ],
    "Молочные продукты": [
        {"name": "Молоко 3.2%", "price": 85, "unit": "л", "image_url": "https://images.unsplash.com/photo-1550583724-b2692b85b150?w=800"},
        {"name": "Кефир 2.5%", "price": 80, "unit": "л", "image_url": "https://images.unsplash.com/photo-1623065422902-30a2d299bbe4?w=800"},
        {"name": "Творог 9%", "price": 150, "unit": "кг", "image_url": "https://images.unsplash.com/photo-1628088062854-d1870b4553da?w=800"},
        {"name": "Сметана 20%", "price": 120, "unit": "кг", "image_url": "https://images.unsplash.com/photo-1628088062854-d1870b4553da?w=800"},
        {"name": "Сыр Российский", "price": 450, "unit": "кг", "image_url": "https://images.unsplash.com/photo-1486297678162-eb2a19b0a32d?w=800"},
        {"name": "Масло сливочное 82%", "price": 600, "unit": "кг", "image_url": "https://images.unsplash.com/photo-1589985270826-4b7bb135bc9d?w=800"},
        {"name": "Йогурт натуральный", "price": 95, "unit": "л", "image_url": "https://images.unsplash.com/photo-1488477181946-6428a0291777?w=800"},
        {"name": "Ряженка 4%", "price": 75, "unit": "л", "image_url": "https://images.unsplash.com/photo-1623065422902-30a2d299bbe4?w=800"},
        {"name": "Сливки 33%", "price": 180, "unit": "л", "image_url": "https://images.unsplash.com/photo-1628088062854-d1870b4553da?w=800"},
        {"name": "Сырок глазированный", "price": 45, "unit": "шт", "image_url": "https://images.unsplash.com/photo-1571212515416-fca2ce42c9f5?w=800"},
    ],
    "Мясо и птица": [
        {"name": "Куриная грудка", "price": 380, "unit": "кг", "image_url": "https://images.unsplash.com/photo-1604503468506-a8da13d82791?w=800"},
        {"name": "Свинина вырезка", "price": 550, "unit": "кг", "image_url": "https://images.unsplash.com/photo-1607623814075-e51df1bdc82f?w=800"},
        {"name": "Говядина мраморная", "price": 750, "unit": "кг", "image_url": "https://images.unsplash.com/photo-1603048588665-791ca8aea617?w=800"},
        {"name": "Фарш говяжий", "price": 420, "unit": "кг", "image_url": "https://images.unsplash.com/photo-1603048588665-791ca8aea617?w=800"},
        {"name": "Куриные окорочка", "price": 220, "unit": "кг", "image_url": "https://images.unsplash.com/photo-1587593810167-a84920ea0781?w=800"},
        {"name": "Индейка филе", "price": 480, "unit": "кг", "image_url": "https://images.unsplash.com/photo-1626082927389-6cd097cdc6ec?w=800"},
        {"name": "Колбаса докторская", "price": 350, "unit": "кг", "image_url": "https://images.unsplash.com/photo-1599894380345-d8c0c9e4c5a5?w=800"},
        {"name": "Сосиски молочные", "price": 280, "unit": "кг", "image_url": "https://images.unsplash.com/photo-1612741214270-c0e5c9f8b9d5?w=800"},
        {"name": "Бекон", "price": 520, "unit": "кг", "image_url": "https://images.unsplash.com/photo-1528607929212-2636ec44253e?w=800"},
        {"name": "Крылышки куриные", "price": 250, "unit": "кг", "image_url": "https://images.unsplash.com/photo-1562967916-ca8ed48f87ea?w=800"},
    ],
    "Услуги": [
        {"name": "Вспашка земли", "price": 1500, "unit": "сотка", "image_url": "https://images.unsplash.com/photo-1625246333195-78d9c38ad449?w=800"},
        {"name": "Покос травы", "price": 800, "unit": "сотка", "image_url": "https://images.unsplash.com/photo-1625246333195-78d9c38ad449?w=800"},
        {"name": "Доставка грузов", "price": 500, "unit": "час", "image_url": "https://images.unsplash.com/photo-1601584115197-04ecc0da31d7?w=800"},
        {"name": "Уборка участка", "price": 1000, "unit": "сотка", "image_url": "https://images.unsplash.com/photo-1625246333195-78d9c38ad449?w=800"},
        {"name": "Посадка саженцев", "price": 200, "unit": "шт", "image_url": "https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=800"},
        {"name": "Обрезка деревьев", "price": 300, "unit": "дерево", "image_url": "https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=800"},
        {"name": "Полив участка", "price": 400, "unit": "час", "image_url": "https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=800"},
        {"name": "Сбор урожая", "price": 600, "unit": "час", "image_url": "https://images.unsplash.com/photo-1625246333195-78d9c38ad449?w=800"},
        {"name": "Консультация агронома", "price": 1200, "unit": "час", "image_url": "https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=800"},
        {"name": "Ветеринарные услуги", "price": 1500, "unit": "визит", "image_url": "https://images.unsplash.com/photo-1587593810167-a84920ea0781?w=800"},
    ],
    "Хлеб и выпечка": [
        {"name": "Хлеб белый", "price": 45, "unit": "шт", "image_url": "https://images.unsplash.com/photo-1509440159596-0249088772ff?w=800"},
        {"name": "Хлеб черный", "price": 50, "unit": "шт", "image_url": "https://images.unsplash.com/photo-1586444248902-2f64eddc13df?w=800"},
        {"name": "Батон нарезной", "price": 40, "unit": "шт", "image_url": "https://images.unsplash.com/photo-1549931319-a545dcf3bc73?w=800"},
        {"name": "Булочки с маком", "price": 60, "unit": "кг", "image_url": "https://images.unsplash.com/photo-1555507036-ab1f4038808a?w=800"},
        {"name": "Круассаны", "price": 120, "unit": "кг", "image_url": "https://images.unsplash.com/photo-1555507036-ab1f4038808a?w=800"},
        {"name": "Пирожки с капустой", "price": 35, "unit": "шт", "image_url": "https://images.unsplash.com/photo-1608198093002-ad4e005484ec?w=800"},
        {"name": "Торт Наполеон", "price": 450, "unit": "кг", "image_url": "https://images.unsplash.com/photo-1464349095431-e9a21285b5f3?w=800"},
        {"name": "Печенье овсяное", "price": 180, "unit": "кг", "image_url": "https://images.unsplash.com/photo-1558961363-fa8fdf82db35?w=800"},
        {"name": "Пряники", "price": 150, "unit": "кг", "image_url": "https://images.unsplash.com/photo-1606313564200-e75d5e30476c?w=800"},
        {"name": "Слойки с повидлом", "price": 90, "unit": "кг", "image_url": "https://images.unsplash.com/photo-1509365465985-25d11c17e812?w=800"},
    ],
    "Агротовары и удобрения": [
        {"name": "Удобрение универсальное", "price": 250, "unit": "кг", "image_url": "https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=800"},
        {"name": "Семена томатов", "price": 45, "unit": "упак", "image_url": "https://images.unsplash.com/photo-1592841200221-a6898f307baa?w=800"},
        {"name": "Грунт для рассады", "price": 180, "unit": "кг", "image_url": "https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=800"},
        {"name": "Торф", "price": 150, "unit": "кг", "image_url": "https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=800"},
        {"name": "Компост", "price": 120, "unit": "кг", "image_url": "https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=800"},
        {"name": "Перегной", "price": 100, "unit": "кг", "image_url": "https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=800"},
        {"name": "Семена огурцов", "price": 40, "unit": "упак", "image_url": "https://images.unsplash.com/photo-1604977042946-1eecc30f269e?w=800"},
        {"name": "Семена перца", "price": 50, "unit": "упак", "image_url": "https://images.unsplash.com/photo-1563565375-f3fdfdbefa83?w=800"},
        {"name": "Удобрение для томатов", "price": 280, "unit": "кг", "image_url": "https://images.unsplash.com/photo-1546094096-0df4bcaaa337?w=800"},
        {"name": "Стимулятор роста", "price": 350, "unit": "л", "image_url": "https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=800"},
    ],
    "Готовые продукты": [
        {"name": "Салат Цезарь", "price": 320, "unit": "шт", "image_url": "https://images.unsplash.com/photo-1546793665-c74683f339c1?w=800"},
        {"name": "Пицца Маргарита", "price": 450, "unit": "шт", "image_url": "https://images.unsplash.com/photo-1513104890138-7c749659a591?w=800"},
        {"name": "Суши сет", "price": 850, "unit": "шт", "image_url": "https://images.unsplash.com/photo-1579584425555-c3ce17fd4351?w=800"},
        {"name": "Блины с мясом", "price": 180, "unit": "шт", "image_url": "https://images.unsplash.com/photo-1567620832903-9fc6debc209f?w=800"},
        {"name": "Пельмени домашние", "price": 350, "unit": "кг", "image_url": "https://images.unsplash.com/photo-1626200419199-391ae4be7a41?w=800"},
        {"name": "Вареники с картошкой", "price": 280, "unit": "кг", "image_url": "https://images.unsplash.com/photo-1626200419199-391ae4be7a41?w=800"},
        {"name": "Котлеты куриные", "price": 420, "unit": "кг", "image_url": "https://images.unsplash.com/photo-1604503468506-a8da13d82791?w=800"},
        {"name": "Голубцы", "price": 380, "unit": "кг", "image_url": "https://images.unsplash.com/photo-1594282486552-05b4d80fbb9f?w=800"},
        {"name": "Манты", "price": 400, "unit": "кг", "image_url": "https://images.unsplash.com/photo-1626200419199-391ae4be7a41?w=800"},
        {"name": "Чебуреки", "price": 60, "unit": "шт", "image_url": "https://images.unsplash.com/photo-1608198093002-ad4e005484ec?w=800"},
    ],
    "Зерно": [
        {"name": "Пшеница", "price": 15, "unit": "кг", "image_url": "https://images.unsplash.com/photo-1574323347407-f5e1ad6d020b?w=800"},
        {"name": "Рожь", "price": 12, "unit": "кг", "image_url": "https://images.unsplash.com/photo-1574323347407-f5e1ad6d020b?w=800"},
        {"name": "Ячмень", "price": 10, "unit": "кг", "image_url": "https://images.unsplash.com/photo-1574323347407-f5e1ad6d020b?w=800"},
        {"name": "Овес", "price": 11, "unit": "кг", "image_url": "https://images.unsplash.com/photo-1574323347407-f5e1ad6d020b?w=800"},
        {"name": "Гречка", "price": 90, "unit": "кг", "image_url": "https://images.unsplash.com/photo-1586201375761-83865001e31c?w=800"},
        {"name": "Рис", "price": 85, "unit": "кг", "image_url": "https://images.unsplash.com/photo-1586201375761-83865001e31c?w=800"},
        {"name": "Кукуруза", "price": 45, "unit": "кг", "image_url": "https://images.unsplash.com/photo-1551754655-cd27e38d2076?w=800"},
        {"name": "Просо", "price": 35, "unit": "кг", "image_url": "https://images.unsplash.com/photo-1574323347407-f5e1ad6d020b?w=800"},
        {"name": "Горох", "price": 60, "unit": "кг", "image_url": "https://images.unsplash.com/photo-1587735243615-c03f25aaff15?w=800"},
        {"name": "Чечевица", "price": 120, "unit": "кг", "image_url": "https://images.unsplash.com/photo-1587735243615-c03f25aaff15?w=800"},
    ],
    "Корма и добавки": [
        {"name": "Комбикорм для кур", "price": 35, "unit": "кг", "image_url": "https://images.unsplash.com/photo-1587593810167-a84920ea0781?w=800"},
        {"name": "Комбикорм для свиней", "price": 32, "unit": "кг", "image_url": "https://images.unsplash.com/photo-1607623814075-e51df1bdc82f?w=800"},
        {"name": "Комбикорм для КРС", "price": 28, "unit": "кг", "image_url": "https://images.unsplash.com/photo-1603048588665-791ca8aea617?w=800"},
        {"name": "Сено луговое", "price": 8, "unit": "кг", "image_url": "https://images.unsplash.com/photo-1625246333195-78d9c38ad449?w=800"},
        {"name": "Солома", "price": 5, "unit": "кг", "image_url": "https://images.unsplash.com/photo-1625246333195-78d9c38ad449?w=800"},
        {"name": "Отруби пшеничные", "price": 18, "unit": "кг", "image_url": "https://images.unsplash.com/photo-1574323347407-f5e1ad6d020b?w=800"},
        {"name": "Премикс витаминный", "price": 450, "unit": "кг", "image_url": "https://images.unsplash.com/photo-1587593810167-a84920ea0781?w=800"},
        {"name": "Соль-лизунец", "price": 80, "unit": "кг", "image_url": "https://images.unsplash.com/photo-1474440692490-2e83ae13ba29?w=800"},
        {"name": "Мел кормовой", "price": 25, "unit": "кг", "image_url": "https://images.unsplash.com/photo-1474440692490-2e83ae13ba29?w=800"},
        {"name": "Ракушка кормовая", "price": 30, "unit": "кг", "image_url": "https://images.unsplash.com/photo-1474440692490-2e83ae13ba29?w=800"},
    ],
    "Мед": [
        {"name": "Мед цветочный", "price": 650, "unit": "кг", "image_url": "https://images.unsplash.com/photo-1587049352846-4a222e784eaf?w=800"},
        {"name": "Мед липовый", "price": 700, "unit": "кг", "image_url": "https://images.unsplash.com/photo-1587049352846-4a222e784eaf?w=800"},
        {"name": "Мед гречишный", "price": 680, "unit": "кг", "image_url": "https://images.unsplash.com/photo-1587049352846-4a222e784eaf?w=800"},
        {"name": "Мед акациевый", "price": 750, "unit": "кг", "image_url": "https://images.unsplash.com/photo-1587049352846-4a222e784eaf?w=800"},
        {"name": "Мед подсолнечный", "price": 600, "unit": "кг", "image_url": "https://images.unsplash.com/photo-1587049352846-4a222e784eaf?w=800"},
        {"name": "Мед разнотравье", "price": 720, "unit": "кг", "image_url": "https://images.unsplash.com/photo-1587049352846-4a222e784eaf?w=800"},
        {"name": "Прополис", "price": 2500, "unit": "кг", "image_url": "https://images.unsplash.com/photo-1587049352846-4a222e784eaf?w=800"},
        {"name": "Перга", "price": 1800, "unit": "кг", "image_url": "https://images.unsplash.com/photo-1587049352846-4a222e784eaf?w=800"},
        {"name": "Воск пчелиный", "price": 800, "unit": "кг", "image_url": "https://images.unsplash.com/photo-1587049352846-4a222e784eaf?w=800"},
        {"name": "Маточное молочко", "price": 5000, "unit": "кг", "image_url": "https://images.unsplash.com/photo-1587049352846-4a222e784eaf?w=800"},
    ],
    "Оборудование и техника": [
        {"name": "Лопата штыковая", "price": 450, "unit": "шт", "image_url": "https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=800"},
        {"name": "Грабли садовые", "price": 350, "unit": "шт", "image_url": "https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=800"},
        {"name": "Секатор", "price": 280, "unit": "шт", "image_url": "https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=800"},
        {"name": "Тяпка", "price": 320, "unit": "шт", "image_url": "https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=800"},
        {"name": "Вилы", "price": 400, "unit": "шт", "image_url": "https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=800"},
        {"name": "Шланг поливочный 20м", "price": 850, "unit": "шт", "image_url": "https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=800"},
        {"name": "Лейка 10л", "price": 250, "unit": "шт", "image_url": "https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=800"},
        {"name": "Опрыскиватель 5л", "price": 650, "unit": "шт", "image_url": "https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=800"},
        {"name": "Тачка садовая", "price": 3500, "unit": "шт", "image_url": "https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=800"},
        {"name": "Культиватор ручной", "price": 1200, "unit": "шт", "image_url": "https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=800"},
    ],
    "Саженцы и семена": [
        {"name": "Саженцы яблони", "price": 450, "unit": "шт", "image_url": "https://images.unsplash.com/photo-1560806887-1e4cd0b6cbd6?w=800"},
        {"name": "Саженцы груши", "price": 480, "unit": "шт", "image_url": "https://images.unsplash.com/photo-1568909344668-6f14a07b56a0?w=800"},
        {"name": "Саженцы вишни", "price": 420, "unit": "шт", "image_url": "https://images.unsplash.com/photo-1528821128474-27f963b062bf?w=800"},
        {"name": "Саженцы малины", "price": 180, "unit": "шт", "image_url": "https://images.unsplash.com/photo-1577069861033-55d04cec4ef5?w=800"},
        {"name": "Саженцы смородины", "price": 150, "unit": "шт", "image_url": "https://images.unsplash.com/photo-1577069861033-55d04cec4ef5?w=800"},
        {"name": "Семена укропа", "price": 25, "unit": "упак", "image_url": "https://images.unsplash.com/photo-1592841200221-a6898f307baa?w=800"},
        {"name": "Семена петрушки", "price": 30, "unit": "упак", "image_url": "https://images.unsplash.com/photo-1592841200221-a6898f307baa?w=800"},
        {"name": "Семена салата", "price": 35, "unit": "упак", "image_url": "https://images.unsplash.com/photo-1592841200221-a6898f307baa?w=800"},
        {"name": "Семена редиса", "price": 28, "unit": "упак", "image_url": "https://images.unsplash.com/photo-1592841200221-a6898f307baa?w=800"},
        {"name": "Семена моркови", "price": 32, "unit": "упак", "image_url": "https://images.unsplash.com/photo-1598170845058-32b9d6a5da37?w=800"},
    ],
    "Яйца": [
        {"name": "Яйца куриные С0", "price": 120, "unit": "десяток", "image_url": "https://images.unsplash.com/photo-1582722872445-44dc5f7e3c8f?w=800"},
        {"name": "Яйца куриные С1", "price": 100, "unit": "десяток", "image_url": "https://images.unsplash.com/photo-1582722872445-44dc5f7e3c8f?w=800"},
        {"name": "Яйца куриные С2", "price": 85, "unit": "десяток", "image_url": "https://images.unsplash.com/photo-1582722872445-44dc5f7e3c8f?w=800"},
        {"name": "Яйца перепелиные", "price": 180, "unit": "десяток", "image_url": "https://images.unsplash.com/photo-1582722872445-44dc5f7e3c8f?w=800"},
        {"name": "Яйца утиные", "price": 150, "unit": "десяток", "image_url": "https://images.unsplash.com/photo-1582722872445-44dc5f7e3c8f?w=800"},
        {"name": "Яйца гусиные", "price": 200, "unit": "десяток", "image_url": "https://images.unsplash.com/photo-1582722872445-44dc5f7e3c8f?w=800"},
        {"name": "Яйца домашние", "price": 140, "unit": "десяток", "image_url": "https://images.unsplash.com/photo-1582722872445-44dc5f7e3c8f?w=800"},
        {"name": "Яйца фермерские", "price": 160, "unit": "десяток", "image_url": "https://images.unsplash.com/photo-1582722872445-44dc5f7e3c8f?w=800"},
        {"name": "Яйца органические", "price": 220, "unit": "десяток", "image_url": "https://images.unsplash.com/photo-1582722872445-44dc5f7e3c8f?w=800"},
        {"name": "Яйца цесарки", "price": 250, "unit": "десяток", "image_url": "https://images.unsplash.com/photo-1582722872445-44dc5f7e3c8f?w=800"},
    ],
}

def download_image(url: str, product_name: str) -> str:
    """Скачать изображение"""
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            upload_dir = Path("uploads/products")
            upload_dir.mkdir(parents=True, exist_ok=True)
            
            filename = f"{uuid.uuid4()}.jpg"
            filepath = upload_dir / filename
            
            with open(filepath, 'wb') as f:
                f.write(response.content)
            
            print(f"  ✅ Скачано: {product_name}")
            return f"/uploads/products/{filename}"
        return ""
    except Exception as e:
        print(f"  ❌ Ошибка: {product_name} - {e}")
        return ""

async def main():
    conn = await asyncpg.connect(DATABASE_URL)
    
    try:
        # Получаем категории
        categories = await conn.fetch("SELECT id, name FROM market.categories")
        
        # Получаем первый магазин
        store = await conn.fetchrow("SELECT id, name FROM market.store_owners LIMIT 1")
        
        if not store:
            print("❌ Нет магазинов")
            return
        
        print(f"📦 Магазин: {store['name']}\n")
        
        added = 0
        
        for category in categories:
            cat_name = category['name']
            cat_id = category['id']
            
            products_data = PRODUCTS_BY_CATEGORY.get(cat_name, [])
            
            if not products_data:
                continue
            
            print(f"📁 {cat_name}:")
            
            for prod in products_data:
                image_path = download_image(prod["image_url"], prod["name"])
                
                await conn.execute("""
                    INSERT INTO market.products 
                    (store_owner_id, name, description, price, category_id, 
                     in_stock, unit, image, created_at, updated_at)
                    VALUES ($1, $2, $3, $4, $5, $6, $7, $8, NOW(), NOW())
                """, 
                    store['id'],
                    prod['name'],
                    f"Качественный товар - {prod['name']}. Всегда свежий и по доступной цене!",
                    prod['price'],
                    cat_id,
                    True,
                    prod['unit'],
                    image_path if image_path else None
                )
                
                added += 1
            
            print()
        
        print(f"🎉 Добавлено: {added} товаров")
        
    finally:
        await conn.close()

if __name__ == "__main__":
    print("🚀 Запуск...\n")
    asyncio.run(main())
    print("\n✅ Готово!")
