import socket
import threading
import RPi.GPIO as GPIO
import hashlib
import os
import secrets

from collections import namedtuple
from datetime import datetime
from oled import oled
from config import *
from time import sleep, time
from mfrc522 import SimpleMFRC522

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
OLED = oled()

class RFIDReader(threading.Thread):
    """RFID Reader Object and Controller"""
    def run(self):
        # Function that runs in separate thread
        self.reader = SimpleMFRC522()
        self.enabled = True
        self.last_scan = time()

        while True:
            # Main loop waiting for RFID scan running in thread
            rfid_id, rfid_txt = self.reader.read()
            print('scanned')
            self.process_rfid(rfid_id, rfid_txt.strip())

    def process_rfid(self, rfid_id, rfid_txt):
        RFID_ID = bytes(str(rfid_id), 'utf-8')
        RFID_TXT = bytes(rfid_txt, 'utf-8')
        cur_timestamp = time()
        time_difference = cur_timestamp - self.last_scan
        if time_difference > TOGGLE_COOLDOWN :
            # system_output_log.write_to_log(f'RFID Scan Attempt! Key Name: {rfid_txt}')
            OLED.clear()
            print(authenticate_key(RFID_ID, RFID_TXT))


class system_log:
    def __init__(self):
        try:
            os.mkdir("logs")
        except:
            print("ERROR: Could not make logs file.")

        #self.LOG_DIR = os.path.join(os.getcwd(), "rfid_reader/logs")
        self.LOG_DIR = "/home/pi/rfid_reader/logs"

        self.LOG_COUNT = len(os.listdir(self.LOG_DIR))
        self.LOG_FILE = os.path.join(self.LOG_DIR, f"system_log_{self.LOG_COUNT}")


    def write_to_log(self, msg):
        now = datetime.now()
        timestamp = now.strftime("%d/%m/%Y %H:%M:%S")
        to_write = f"[{timestamp}]: {msg}\n"
        with open(self.LOG_FILE, 'a') as log_file:
            log_file.write(to_write)



def authenticate_key(rfid_key_num, rfid_key_name):
    hashed_key = hashlib.sha256(rfid_key_name + rfid_key_num).hexdigest()
    for key in KEYS:
        if key.hash == hashed_key:
            transaction_id = secrets.token_hex(5)
            # lprint(f"Authenticated User Toggled Garage! Key Name: {registered_key['NAME']}")
            # lprint(f"Transaction ID: {transaction_id}")
            # open_garage(key.hash, transaction_id)
            OLED.text("Authenticated", (15, 0))
            OLED.text(f"Key: {key.name}", (0, 30))
            OLED.poll()
            return key.name

        else:

            # lprint("Unauthorized tag attempt!")

            # if LOGGING:
                # system_output_log.write_to_log(f"UNAUTHORIZED ATTEMPT TO TOGGLE GARAGE!")
            OLED.text("UNAUTHORIZED", (10, 0))
            OLED.text("SYSTEM NOTIFIED", (0, 30))
            OLED.poll()
            return False
            # break
    # display_time()

def open_garage(identification, transaction_id):
    assert(identification)
    assert(transaction_id)
    msg = f"{CMD}*{transaction_id}"
    sock.sendto(bytes(msg, 'utf-8'), (HOSTNAME_TARGET, UDP_PORT))

def lprint(msg):
    print(msg)
    if LOGGING:
        system_output_log.write_to_log(msg)

def display_time():
    OLED.clear()
    t_obj = time_of_day()
    formatted_time = f"{t_obj.hour}:{t_obj.minute} {t_obj.day_half}"
    OLED.text(formatted_time, (28, 10))
    print("Updated time!!")
    OLED.poll(None)

def time_of_day():
    now = datetime.now()
    hour = now.strftime("%I")
    minute = now.strftime("%M")
    day_half = now.strftime("%p")

    current_time = time_obj(hour, minute, day_half)

    return current_time

def display_time_check():
    prev_min = "x"
    while True:
        minute = time_of_day().minute
        if prev_min != minute and OLED.busy == False:
            prev_min = minute
            display_time()
        sleep(1)

def main():
    rfid_reader_obj = RFIDReader()
    rfid_reader_obj.start()
    # display_time_check()

time_obj = namedtuple('time_object', 'hour minute day_half')

if __name__ == "__main__":
    #oled_time_thread = threading.Thread(target=display_time_check, args='')
    #oled_time_thread.start()
    # if LOGGING:
    #     system_output_log = system_log()

    main()
