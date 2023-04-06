import board
import digitalio
import adafruit_ssd1306
from time import sleep, time
from PIL import Image, ImageDraw, ImageFont


msg_timeout = 3

i2c = board.I2C()

class oled:

    def __init__(self):

        self.busy = False
        self.display = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3C, reset=digitalio.DigitalInOut(board.D4))
        self.font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 14)
        self.lines = [[10, 5], [10, 15], [10, 25], [10, 35]]
        self.image = Image.new("1", (self.display.width, self.display.height))
        self.draw = ImageDraw.Draw(self.image)


    def clear(self):
        self.display.fill(0)
        self.image = Image.new("1", (self.display.width, self.display.height))
        self.draw = ImageDraw.Draw(self.image)
        self.display.show()

    def text(self, msg, pos):
        self.draw.text(pos, msg, font=self.font, fill=255)


    def poll(self, timeout=3):
        self.busy = True
        self.display.image(self.image)
        self.display.show()
        if timeout != None:
            sleep(timeout)
            self.clear()
        self.busy = False


