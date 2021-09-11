import random, time
import threading

from paho.mqtt import client as mqtt_client


broker = '192.168.1.30'
port = 1883
topic = "/python/stepper"
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 100)}'

# global variable where messages are placed for processing by the main thread
received_msgs = []


def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        received_msgs.append(msg.payload.decode())
        # print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

    client.subscribe(topic)
    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()

def listen_for_msgs():
    global received_msgs
    print('listening for messages')
    msg_count = len(received_msgs)
    while True:
        new_count = len(received_msgs)
        if new_count != msg_count:
            new_msg = received_msgs[-1]
            break
        time.sleep(0.2)
    return new_msg    

if __name__ == '__main__':
    x = threading.Thread(target=run)
    x.start()
    
    while True:
        msg = listen_for_msgs()
        print(f'{msg}')
    
