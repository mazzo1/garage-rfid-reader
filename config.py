from collections import namedtuple
KeyEntry = namedtuple('KeyEntry',['name', 'hash'])
# RFID Reader Configuration

# MQTT BROKER SETTINGS 
MQTT_BROKER_HOSTNAME = 'cash.local'
MQTT_PORT = 1883
MQTT_TIMEOUT = 60

# CLIENT SETTINGS
CLIENT_USERNAME = 'garage-rfid-reader'
CLIENT_PW = 'H7xc.shf&8'

# Topics
CLIENT_STATUS_TOPIC = 'garage_reader/status'

topics = [CLIENT_STATUS_TOPIC]

# Cooldown time between toggling the garage door
TOGGLE_COOLDOWN = 1.5

#_______________    Registered Keys    _______________#
KEYS = [
    KeyEntry('azzo-tag-1', '0ac4ed82bb7951274d54ec62413066ca2bcdf806b663df0b0ef70f2f3b3eab3d'),
    KeyEntry('azzo-tag-2', '11aec1e608354ca2992ef67ee76cfba839cb51334ab59814694964592c898a3f'),
    KeyEntry('azzo-tag-3', '041e4e20bce1d0f09c6b1bc636eb4dd5559e6694ef4f8706ee5861aed652dd55'),
    KeyEntry('azzo-card-4', '8e5313d7c34481568c55a6339279688f80b3a39c1f96d4bf29abe37103d920fe'),
    KeyEntry('azzo-card-5', '8781254743f432736480194df1c088648b83b938a70dfc0a796c4f5bf85e6d87'),
    KeyEntry('azzo-card-6', 'd197c10cfeb57e253aca001e6707fa104b89e923f10070bc0d17bf9697334ae4')
]
