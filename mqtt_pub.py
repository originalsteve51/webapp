from paho.mqtt import client as mqtt_client

import random, time

broker = '192.168.1.30'
port = 1883
topic = "/python/stepper"
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 1000)}'


def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def publish(client):
    msg_count = 0
    while True:
        time.sleep(1)
        msg = f"messages: {msg_count}"
        result = client.publish(topic, msg)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send `{msg}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")
        msg_count += 1

def publish_one(client, a_topic, a_msg):
    result = client.publish(a_topic, a_msg)
    status = result[0]
    """
    if status == 0:
        print(f"Sent `{a_msg}` to topic `{a_topic}`")
    else:
        print(f"Failed to send message to topic {a_topic}")
    """

def run():
    client = connect_mqtt()
    client.loop_start()
    return client

if __name__ == '__main__':
    client = run()
    publish_one(client, topic, 'holy crap')
    
