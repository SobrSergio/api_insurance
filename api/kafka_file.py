from kafka import KafkaProducer
import json
import logging


logger = logging.getLogger(__name__)


KAFKA_BROKER_URL = "kafka:9092"  
KAFKA_TOPIC = "insurance_tariffs_log" 

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
        producer.flush()  
        logger.info("Message sent to Kafka: %s", message)
    except Exception as e:
        logger.error("Error sending message to Kafka: %s", e)
