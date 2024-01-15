import asyncio
import os
from dotenv import load_dotenv
import random
from random import randint
import time
import redis

load_dotenv()

async def generate_metric(device_id):
    metric_type = "kwh"  # Puedes cambiar esto según tus necesidades
    metric_value = random.uniform(10, 100)
    timestamp = str(time.time())
    
    metric_data = {
        "device_id": device_id,
        "metric_type": metric_type,
        "metric_value": metric_value,
        "timestamp": timestamp
    }
    
    return metric_data


async def send_metric_to_redis(redis_client, metric_data):
    redis_client.xadd(os.getenv("STREAM_KEY"), metric_data)

async def simulate_device(device_id, redis_client):
    while True:
        metric_data = await generate_metric(device_id)
        await send_metric_to_redis(redis_client, metric_data)
        
        # Espera un tiempo aleatorio antes de generar la próxima métrica
        await asyncio.sleep(random.uniform(1, 4))

async def main():
    redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True, db=0)

    # Configura múltiples dispositivos simulados (puedes ajustar según tus necesidades)
    device_ids = ["device1", "device2", "device3"]

    # Inicia los simuladores en paralelo
    tasks = [simulate_device(device_id, redis_client) for device_id in device_ids]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())

    