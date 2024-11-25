import os
import json

# from kafka import KafkaProducer

class Metrics:
	KAFKA_URL = os.environ.get("KAFKA_URL", "localhost:29092")

	def __init__(self) -> None:
		print("Kafka", self.KAFKA_URL)

		# self.producer = KafkaProducer(bootstrap_servers = [self.KAFKA_URL])

	def push_events(self, event, arena):
		# self.producer.send("event", json.dumps({ 'event': event, 'arena': arena }).encode('utf-8'))
		# self.producer.flush(timeout=10)
		return

	def push_metric(self, metric, arena, data):
		# self.producer.send("metrics", json.dumps({ 'metric': metric, 'arena': arena, 'data': data }).encode('utf-8'))
		# self.producer.flush(timeout=10)
		return