# RFID Reader Configuration



#_________________   Network Settings   ______________#

HOSTNAME_TARGET = "garage-opener-switch.local"
UDP_PORT = 5005

#_______________   Operation Settings   ______________#

SCAN_COOLDOWN = 1.5
LOGGING = True
CMD = "U0_GARAGE_TOGGLE_"


#_______________    Registered Keys    _______________#

KEYS = [

{'NAME': 'azzo-tag-2', 'HASH_KEY': '11aec1e608354ca2992ef67ee76cfba839cb51334ab59814694964592c898a3f'},

{'NAME': 'azzo-tag-1', 'HASH_KEY': '0ac4ed82bb7951274d54ec62413066ca2bcdf806b663df0b0ef70f2f3b3eab3d'},

{'NAME': 'azzo-tag-3', 'HASH_KEY': '041e4e20bce1d0f09c6b1bc636eb4dd5559e6694ef4f8706ee5861aed652dd55'},

{'NAME': 'azzo-card-4', 'HASH_KEY': '8e5313d7c34481568c55a6339279688f80b3a39c1f96d4bf29abe37103d920fe'},

{'NAME': 'azzo-card-5', 'HASH_KEY': '8781254743f432736480194df1c088648b83b938a70dfc0a796c4f5bf85e6d87'},

{'NAME': 'azzo-card-6', 'HASH_KEY': 'd197c10cfeb57e253aca001e6707fa104b89e923f10070bc0d17bf9697334ae4'}

]

#_____________________________________________________#
