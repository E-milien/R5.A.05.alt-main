from metrics import Metrics
from random import randint

from time import sleep

metrics = Metrics()

while True:
    sleep(5)
    metrics.push_metric('arena3', randint(0, 300))