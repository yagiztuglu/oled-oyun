from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import framebuf
import time
import uasyncio
import random

i2c = I2C(0, scl = Pin(17), sda = Pin(16), freq=400000)

oled = SSD1306_I2C(128, 64, i2c)

bt1 = Pin(15,Pin.IN,Pin.PULL_DOWN)
bt2 = Pin(14,Pin.IN,Pin.PULL_DOWN)
bt3 = Pin(13,Pin.IN,Pin.PULL_DOWN)

gemi_x = 45
gemi_y = 55
fire_y = 50
fire_start = 0
astro_x = random.randint(20,100)
astro_y = 15
oyun_start = 0
fire_x = 0
score_count = 0
a = 0
b = 0

def başlangıç_ekranı():
    if oyun_start == 0:
        oled.fill(0)
        time.sleep(0.1)
        oled.invert(1)
        oled.text("Press button ",15,30)
        oled.text("to start game",12,40)
        oled.show()
        astro_y = 15

def gemi_sol_hareket():
    global gemi_x
    if bt1.value()  == 1:
        gemi_x = gemi_x - 10
        if gemi_x <= 0:
            gemi_x = 0
            
def gemi_sag_hareket():
    global gemi_x
    if bt3.value() == 1:
        gemi_x = gemi_x + 10
        if  gemi_x > 90:
            gemi_x = 90

def hit():
    global astro_y
    global a
    global b
    global score_count
    if fire_x == astro_x or fire_x ==( astro_x + 1) or fire_x ==( astro_x + 2) or fire_x ==( astro_x + 3) or fire_x ==( astro_x + 4) or fire_x ==( astro_x + 5) or fire_x ==( astro_x + 6) or fire_x ==( astro_x + 7) or fire_x ==( astro_x + 8) or fire_x ==( astro_x + 9) or fire_x ==( astro_x + 10):
        oled.fill(0)
        astro_y = 15 
        time.sleep(0.1)
        print("hit")
        score_count += 1
        a = 0
        b = 1

async def fire():
    global fire_x
    global fire_y
    oled.vline(fire_x,15,fire_y,1)
    oled.show()
        
async def fire_():
    uasyncio.create_task(fire())
    
def yanma():
    global oyun_start
    global astro_y
    if astro_y > 54:
        oyun_start = 0
        oled.text("GAME OVER",25,30)
        oled.show()
        astro_y = 15
        for i in range (0,5):
            oled.invert(1)
            time.sleep(0.2)
            oled.invert(0)
            time.sleep(0.2)
            i = i + 1
    
def astroid():
    global astro_x
    global astro_y
    astro_y = astro_y + 2
    oled.fill_rect(astro_x,astro_y,10,10,1)
    oled.show()
    
def oyun():
    global a
    if oyun_start == 1:
        oled.invert(0)
        oled.text("score = ",0,0)
        oled.text(str(score_count),60,0)
        fire_x = gemi_x + 19
       # astro_x = random.randint(5,100)
        gemi_sol_hareket()
        gemi_sag_hareket()
        if bt2.value() == 1:
            uasyncio.run(fire_())
            a = 1
        astroid()

        time.sleep(0.2)
        oled.fill(0)
        oled.text("|_I_|",gemi_x,gemi_y)
        oled.show()
        yanma()




        


while True:
    başlangıç_ekranı()
    
    if bt1.value() or bt2.value() or bt3.value():
        oyun_start = 1
        
    if oyun_start == 0:
        b = 0
        score_count = 0

    fire_x = gemi_x + 19
    if b == 1:
        astro_x = random.randint(5,100)
    oyun()
    if a == 1:
        hit()

