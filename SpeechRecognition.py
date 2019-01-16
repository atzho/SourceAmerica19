import speech_recognition as sr
print("Imported sr")
import time
import RPi.GPIO as GPIO
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

mic_name = "USB PnP"
#Sample rate is how often values are recorded 
sample_rate = 48000
#Chunk is like a buffer. It stores 2048 samples (bytes of data) 
#here. 
#it is advisable to use powers of 2 such as 1024 or 2048 
chunk_size = 2048
r = sr.Recognizer() 
print("SR Initialized")
#generate a list of all audio cards/microphones 
mic_list = sr.Microphone.list_microphone_names() 
print("Fetched list of mics")
#the following loop aims to set the device ID of the mic that 
#we specifically want to use to avoid ambiguity.
device_id = 0
for i, microphone_name in enumerate(mic_list): 
        print('Mic Name:', microphone_name, "id: ",i)
        if mic_name in microphone_name: 
                device_id = i
#        else:
#                print(i)
#time.sleep(50000)
##device_id = 1
print("Set Mic ID as", device_id)

vibrate = 32
GPIO.setmode(GPIO.BOARD)
GPIO.setup(vibrate, GPIO.OUT)

RST = None
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0

disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)

disp.begin()

disp.clear()
disp.display()

width = disp.width
height = disp.height
image = Image.new('1', (width, height))

draw = ImageDraw.Draw(image)

draw.rectangle((0,0,width,height), outline=0, fill=0)

padding = -2
top = padding
bottom = height-padding
x = 0
font = ImageFont.load_default()
font = ImageFont.truetype('neoletters.ttf', 14)

def vibrateFor(delay):
        GPIO.output(vibrate,GPIO.HIGH)
        time.sleep(delay)
        GPIO.output(vibrate,GPIO.LOW)
vibrateFor(0.3)
with sr.Microphone(device_index = device_id, sample_rate = sample_rate, 
                                                chunk_size = chunk_size) as source: 
        #wait for a second to let the recognizer adjust the 
        #energy threshold based on the surrounding noise level 
        print("Found Mic")
        print("Calibrating...")
                r.adjust_for_ambient_noise(source)
        while True:
                print("Say Something")
                #listens for the user's input
                #before = time.time()
                audio = r.listen(source) 
                before = time.time()        
                try: 
                        text = r.recognize_google(audio) 
                        print("you said: " + text) 
                        vibrateFor(0.3)
#                        GPIO.output(vibrate,GPIO.HIGH) 
#                        time.sleep(0.3) 
#                        GPIO.output(vibrate,GPIO.LOW)
                        if len(text) <= 20:
                                draw.text((x,top+5),text,font=font,fill=255)
                        elif len(text) > 20 & len(text) <= 40:
                                draw.text((x,top+5),text[0:20],font=font,fill=255)
                                draw.text((x,top+25),text[21:40],font=font,fill=255)
                        elif len(text) > 40 & len(text) <= 60:
                                draw.text((x,top+5),text[0:20],font=font,fill=255)
                                draw.text((x,top+25),text[21:40],font=font,fill=255)
                                draw.text((x,top+45),text[41:60],font=font,fill=255)
                        else:       
                                draw.text((x,top+5),text[0:20],font=font,fill=255)
                                draw.text((x,top+25),text[21:40],font=font,fill=255)
                                draw.text((x,top+45),text[41:60],font=font,fill=255)
                                draw.text((x,top+65),text[61:80],font=font,fill=255)
                
                #error occurs when google could not understand what was said 
                
                except sr.UnknownValueError: 
                        print("Google Speech Recognition could not understand audio") 
                
                except sr.RequestError as e: 
                        print(("Could not request results from Google Speech Recognition service; {0}".format(e)))
                print("dt = " + str(time.time() - before))
