import json

from kafka import KafkaConsumer
from dotenv import load_dotenv

import os
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

import signal
from threading import Thread

load_dotenv()

bucket = 'monitoring'
token = os.environ.get('INFLUXDB_TOKEN')
url = os.environ.get('INFLUXDB_URL')

kafka_url = os.environ.get('KAFKA_URL')

influx_client = InfluxDBClient(url, token, org="iot")
write_api = influx_client.write_api(write_options=SYNCHRONOUS)

consumer_event = KafkaConsumer('event', bootstrap_servers = [kafka_url])
consumer_metric = KafkaConsumer('metrics', bootstrap_servers = [kafka_url])

print('KAFKA CONNECTION')

def consume_event():
  for message in consumer_event:
    plain_message = message.value.decode()
    print(plain_message)

def consume_metric():
  golds = {}

  for message in consumer_metric:
    plain_message = message.value.decode()
    message = json.loads(plain_message)

    print(plain_message)

    metric = message['metric']
    arena = message['arena']

    if metric == 'character':
      character = message['data']
      statistics = character['statistics']

      point = (
        Point("character")
          .tag("arena", arena)
          .tag("character", character['id'])
          .field("life", float(statistics['life']))
          .field("strength", float(statistics['strength']))
          .field("armor", float(statistics['armor']))
          .field("speed", float(statistics['speed']))
      )

      write_api.write(bucket, "iot", point)

    if metric == 'state':
      data = message['data']

      point = (
        Point("state")
          .tag("arena", arena)
          .field("turn", data['turn'])
          .field("death", data['death'])
          .field("alive", data['alive'])
          .field("total", data['total'])
      )

      write_api.write(bucket, "iot", point)

    if metric == 'gold_reward':
      data = message['data']
      source = data['source']

      if arena not in golds:
        golds[arena] = {}

      if source not in golds[arena]:
        golds[arena][source] = 0

      golds[arena][source] += data['value']

      point = (
        Point("golds")
          .tag("arena", arena)
          .tag("source", source)
          .field("value", golds[arena][source])
      )

      write_api.write(bucket, "iot", point)

thread_event = Thread(target=consume_event)
thread_event.daemon = True

thread_metric = Thread(target=consume_metric)
thread_metric.daemon = True

signal.signal(signal.SIGINT, signal.SIG_DFL)

thread_event.start()
thread_metric.start()

thread_event.join()
thread_metric.join()
