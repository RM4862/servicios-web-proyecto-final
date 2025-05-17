# response_listener.py (placeholder)
import pika

def callback(ch, method, properties, body):
    print("\n RESPUESTA FINAL:")
    print(body.decode())

conn = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = conn.channel()
channel.queue_declare(queue='api.response')
channel.basic_consume(queue='api.response', on_message_callback=callback, auto_ack=True)
print("Esperando respuestas...")
channel.start_consuming()
