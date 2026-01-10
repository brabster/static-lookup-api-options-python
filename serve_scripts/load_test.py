import json
import random

import locust


with open('../uncommitted/recommendations_dataset.sample.json', 'r') as f:
    CUSTOMER_IDS = json.load(f)

class HelloWorldUser(locust.HttpUser):
    @locust.task
    def hello_world(self):
        self.client.get(f"/recommendations/{random.choice(CUSTOMER_IDS)['id']}", name="/recommendations")
