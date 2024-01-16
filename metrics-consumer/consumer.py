import asyncio
import redis
import httpx
import os
from dotenv import load_dotenv

load_dotenv()

async def process_metric(metric_data):
    # Aquí puedes realizar cualquier lógica adicional antes de almacenar la métrica
    print(f"Processing metric: {metric_data}")

    # Llama al microservicio de FastAPI o Django para almacenar la métrica
    async with httpx.AsyncClient() as client:
        response = await client.post("http://localhost:8000/metrics/savemetric", json=metric_data)
        if response.status_code != 201:
            print(f"Failed to store metric: {response.text}")

async def consume_metrics(redis_client):
    stream_name = os.getenv("STREAM_KEY")
    last_id = "0"
    
    while True:
        try:
            # Consume eventos del stream
            event = redis_client.xread({stream_name: last_id}, count=1, block=4000)

            if event:
                # Extrae la información del evento
                stream, messages = event[0]
                message = messages[0][1]
                metric_data = {key: value for key, value in message.items()}

                # Procesa y almacena la métrica
                await process_metric(metric_data)
                
                # Actualiza el último ID leído
                last_id = messages[0][0]
                

        except Exception as e:
            print(f"Error consuming metrics: {e}")
            await asyncio.sleep(5)  # Espera antes de volver a intentar

async def main():
    redis_client = redis.Redis(host='redis', port=6379, decode_responses=True, db=0)

    # Crea el consumidor de métricas en un bucle asyncio
    await consume_metrics(redis_client)

if __name__ == "__main__":
    asyncio.run(main())