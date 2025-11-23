"""
Убить зависшие процессы в PostgreSQL
"""
import asyncio
import asyncpg
from config import settings

async def kill_locks():
    """Убить все зависшие процессы"""
    
    # Парсим DATABASE_URL
    db_url = settings.DATABASE_URL.replace('postgresql+asyncpg://', 'postgresql://')
    
    # Подключаемся к БД
    conn = await asyncpg.connect(db_url)
    
    try:
        # Получаем список активных процессов
        processes = await conn.fetch("""
            SELECT pid, usename, application_name, state, query, now() - query_start as duration
            FROM pg_stat_activity
            WHERE datname = 'edu_na_bazar'
            AND pid != pg_backend_pid()
            AND state != 'idle'
            ORDER BY query_start
        """)
        
        if not processes:
            print("✅ Нет активных процессов")
        else:
            print(f"🔍 Найдено активных процессов: {len(processes)}\n")
            for p in processes:
                print(f"PID: {p['pid']}")
                print(f"User: {p['usename']}")
                print(f"App: {p['application_name']}")
                print(f"State: {p['state']}")
                print(f"Duration: {p['duration']}")
                print(f"Query: {p['query'][:100]}...")
                print("-" * 80)
        
        # Убиваем все процессы
        if processes:
            print("\n💀 Убиваем процессы...")
            for p in processes:
                try:
                    await conn.execute(f"SELECT pg_terminate_backend({p['pid']})")
                    print(f"✅ Убит процесс {p['pid']}")
                except Exception as e:
                    print(f"⚠️ Не удалось убить процесс {p['pid']}: {e}")
        
        print("\n✅ Готово!")
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")
    finally:
        await conn.close()

if __name__ == "__main__":
    asyncio.run(kill_locks())
