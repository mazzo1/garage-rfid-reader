import atexit
import threading
import paho.mqtt.client as mqtt
import hashlib

from datetime import datetime
from oled import oled
from config import *
from time import sleep, time
from mfrc522 import SimpleMFRC522


class RFIDReader(threading.Thread):
    """RFID Reader Object and Controller"""

    def run(self):
        # Function that runs in separate thread
        self.reader = SimpleMFRC522()
        self.enabled = True
        self.last_scan = time()

        while True:
            # Main loop waiting for RFID scan running in thread
            rfid_id, rfid_txt = self.reader.read()  # read RFID data
            self.process_rfid(rfid_id, rfid_txt.strip())

    def process_rfid(self, rfid_id, rfid_txt):
        """Check scanned RFID tag, meat of the code"""
        # convert raw RFID data into bytes
        RFID_ID, RFID_TXT = bytes(
            str(rfid_id), 'utf-8'), bytes(rfid_txt, 'utf-8')
        # get time delta to enforce cooldown
        time_delta = time() - self.last_scan
        if time_delta > TOGGLE_COOLDOWN:
            OLED.clear()
            # check if scanned RFID is authorized
            scanned_key = authenticate_key(RFID_ID, RFID_TXT)
            if scanned_key:
                # open garage if key is valid
                print("opening garage")
                oled_thread = threading.Thread(target=display_scan_result,
                                               args=('Authenticated', f'Key: {scanned_key}'))
            else:
                # if key is invalid
                oled_thread = threading.Thread(target=display_scan_result,
                                               args=('UNAUTHORIZED', 'SYSTEM NOTIFIED'))
            oled_thread.start()  # display status of RFID scan in separate thread
            oled_thread.join()  # to not block program from opening garage while OLED finishes
            # set the OLED back to the time after RFID status display
            update_time(get_time())


def authenticate_key(rfid_key_num, rfid_key_name):
    """Calculate hash of the RFID data, return name of key if authentic, or False if invalid"""
    hashed_key = hashlib.sha256(rfid_key_name + rfid_key_num).hexdigest()
    for key in KEYS:
        if key.hash == hashed_key:
            return key.name
        return False


def check_time():
    """Continuously update the time on the OLED if the minute changes"""
    prev_min = -1
    while True:
        h, m, p = get_time()
        if prev_min != m and OLED.busy == False:
            prev_min = m
            update_time((h, m, p))
        sleep(1)


def update_time(cur_time):
    h, m, p = cur_time
    """Write supplied time input to OLED"""
    OLED.clear()
    OLED.text(f'{h}:{m} {p}', (28, 10))
    OLED.poll(None)


def get_time():
    """Return current Hour, Minute, and PM/AM as a list of 3"""
    return datetime.now().strftime("%I:%M:%p").split(':')


def display_scan_result(line1, line2):
    """Display feedback from the RFID scan, name of key if valid, else unauthorized"""
    OLED.text(line1, (15, 0))
    OLED.text(line2, (0, 30))
    OLED.poll()


def parse_mqtt_msg(msg):
    """Parse MQTT messages and execute corresponding function"""
    topic = msg.topic
    payload = msg.payload.decode()
    commands = {
        (CLIENT_STATUS_TOPIC, "lifecheck"): life_check,
    }
    command = commands.get((topic, payload))
    if command is not None:
        command()


def life_check():
    """Respond to lifecheck message with alive"""
    publish(CLIENT_STATUS_TOPIC, 'alive')


def publish(topic, msg='ok'):
    """Publish MQTT message"""
    mqtt_client.publish(topic, payload=msg, qos=0)


def on_message_cb(client, userdata, msg):
    """Callback function when message is received"""
    parse_mqtt_msg(msg)


def on_connect_cb(client, userdata, flags, rc):
    """Callback function when MQTT client is connected successfully"""
    publish(CLIENT_STATUS_TOPIC, "init")
    for t in topics:
        client.subscribe(t)


def exit_handler():
    """Exit handler"""
    publish(CLIENT_STATUS_TOPIC, "died")
    rfid_reader_obj.join()
    update_clock_thread.join()
    mqtt_client.loop_stop()


if __name__ == "__main__":
    atexit.register(exit_handler)
    rfid_reader_obj = RFIDReader()
    OLED = oled()
    update_clock_thread = threading.Thread(target=check_time)
    mqtt_client = mqtt.Client()
    mqtt_client.on_connect = on_connect_cb
    mqtt_client.on_message = on_message_cb
    mqtt_client.username_pw_set(CLIENT_USERNAME, CLIENT_PW)
    mqtt_client.connect(MQTT_BROKER_HOSTNAME, MQTT_PORT, MQTT_TIMEOUT)
    rfid_reader_obj.start()
    update_clock_thread.start()
    mqtt_client.loop_forever()
