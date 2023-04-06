import atexit
import paho.mqtt.client as mqtt
from time import sleep, time
from config import *
from mfrc522 import SimpleMFRC522

DEV_MODE = False


# Class definition of light relay output object
class RelayOutput:
	def __init__(self, topic, pin):
		self.topic = topic
		self.pin = pin
		self.is_on = False
		self.last_activated = time()
		self.armed = True

	def toggle_garage_door(self):
		if not self.armed:
			return 
		cur_timestamp = time()
		time_difference = cur_timestamp - self.last_activated
		if time_difference > TOGGLE_COOLDOWN and self.armed:
			self.last_activated = time()
			pin_on(GARAGE_TOGGLE_LED)
			pin_on(GARAGE_RELAY_PIN)
			sleep(0.5)
			pin_off(GARAGE_RELAY_PIN)
			pin_off(GARAGE_TOGGLE_LED)
			publish(self.topic, 'ok:toggled')

	def turn_on(self):
		if not self.armed:
			return
		pin_on(self.pin)
		pin_on(LIGHTS_STATUS_LED)
		self.is_on = True
		publish(self.topic, 'ok:on')

	def turn_off(self):
		if not self.armed:
			return 
		pin_off(self.pin)
		pin_off(LIGHTS_STATUS_LED)
		self.is_on = False
		publish(self.topic, 'ok:off')

	def toggle(self):
		if self.is_on:
			self.turn_off()
		else:
			self.turn_on()

	def arm(self):
		self.armed = True
		publish(self.topic, 'ok:armed')

	def disarm(self):
		self.armed = False
		publish(self.topic, 'ok:disarmed')

def parse_msg(msg):
	topic = msg.topic
	payload = msg.payload.decode()
	commands = {
		(CLIENT_STATUS_TOPIC, "lifecheck"): life_check,
	}
	command = commands.get((topic, payload))
	if command is not None:
		command()

def life_check():
	publish(CLIENT_STATUS_TOPIC, 'alive')

def publish(topic, msg='ok'):
	mqtt_client.publish(topic, payload=msg, qos=0)

def on_message_cb(client, userdata, msg):
	parse_msg(msg)

def on_connect_cb(client, userdata, flags, rc):
	publish(CLIENT_STATUS_TOPIC, "init")
	pin_on(GARAGE_STATUS_LED)
	for t in topics:
		client.subscribe(t)

def exit_handler():
	publish(CLIENT_STATUS_TOPIC, "died")
	mqtt_client.loop_stop()

atexit.register(exit_handler)

if __name__ == "__main__":
	if not DEV_MODE:
		init_gpio()
	mqtt_client = mqtt.Client()
	mqtt_client.on_connect = on_connect_cb
	mqtt_client.on_message = on_message_cb
	mqtt_client.username_pw_set(CLIENT_USERNAME, CLIENT_PW)
	mqtt_client.connect(MQTT_BROKER_HOSTNAME, MQTT_PORT, MQTT_TIMEOUT)
	mqtt_client.loop_forever()
