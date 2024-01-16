import asyncio
import redis
import os
from dotenv import load_dotenv

load_dotenv()

async def process_metric_alert(metric_data):
    # Aquí puedes definir la lógica para generar alertas o notificaciones
    if float(metric_data["metric_value"]) > 50:
        print(f"ALERT: Metric exceeds threshold - {metric_data}")

async def consume_alerts(redis_client):
    stream_name = os.getenv("STREAM_KEY")
    last_id = "0"  # Inicializamos con un ID bajo para comenzar desde el principio

    while True:
        try:
            # Consume eventos del stream desde el último ID leído
            event = redis_client.xread({stream_name: last_id}, count=1, block=4000)

            if event:
                # Extrae la información del evento
                stream, messages = event[0]
                message = messages[0][1]
                metric_data = {key: value for key, value in message.items()}

                # Procesa alertas si la métrica supera el umbral
                await process_metric_alert(metric_data)

                # Actualiza el último ID leído
                last_id = messages[0][0]

        except Exception as e:
            print(f"Error consuming alerts: {e}")
            await asyncio.sleep(5)  # Espera antes de volver a intentar

async def main():
    redis_client = redis.Redis(host='redis', port=6379, decode_responses=True, db=0)

    # Crea el consumidor de alertas en un bucle asyncio
    await consume_alerts(redis_client)

if __name__ == "__main__":
    asyncio.run(main())