#!/usr/bin/env python
from flask import Flask
import pika, yaml
app = Flask(__name__)


@app.route('/')
def check_devo():
    try:
        # Read configuration RabbitMQ server
        with open("rabbitmq.yaml", "r") as ymlfile:
            cfg = yaml.load(ymlfile)

        # Test RabbitMQ Status
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=cfg["rabbitmq"]["host"],
                                                                       port=cfg["rabbitmq"]["port"]))
        if connection.is_open:
           connection.close()
           return 'OK\n'
    except Exception as error:
      return 'KO\n'


if __name__ == '__main__':
    app.run(host='0.0.0.0')     # open for everyone
