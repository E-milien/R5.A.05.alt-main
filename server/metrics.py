import os
import json

from kafka import KafkaProducer

class Metrics:
	KAFKA_URL = os.environ.get("KAFKA_URL", "localhost:29092")

	def __init__(self) -> None:
		print("Kafka", self.KAFKA_URL)

		self.producer = KafkaProducer(bootstrap_servers = [self.KAFKA_URL])
		self.metrics = {}

	def increment_metric(self, metric, value):
		if metric not in self.metrics:
			self.metrics[metric] = 0

		self.metrics[metric] += value

		value = self.metrics[metric]
		self.push_metric(metric, value)

	def push_metric(self, metric, value):
		v = {}
		v[metric] = value

		self.push_metrics(metric, v)

	def push_metrics(self, metric, values):
		print(metric, values)

		self.producer.send(metric, json.dumps(values).encode('utf-8'))
		self.producer.flush(timeout=10)