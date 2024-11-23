from kafka import KafkaProducer
import json
import logging

# Настройка логирования
logger = logging.getLogger(__name__)

# Настройка Kafka Producer
KAFKA_BROKER_URL = "kafka:9092"  # URL Kafka-брокера
KAFKA_TOPIC = "insurance_tariffs_log"  # Тема для логирования

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER_URL,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def send_to_kafka(message: dict):
    """
    Отправка сообщения в Kafka.
    """
    try:
        producer.send(KAFKA_TOPIC, message)
        producer.flush()  # Убедимся, что сообщение отправлено
        logger.info("Message sent to Kafka: %s", message)
    except Exception as e:
        logger.error("Error sending message to Kafka: %s", e)
