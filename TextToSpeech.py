from gtts import gTTS
import time
import os
import subprocess
language = 'en'
myobj = gTTS("Starting up", lang=language, slow=False) 
myobj.save("test.mp3")
#soundCmd = '"C:/Program Files (x86)/Windows Media Player/wmplayer.exe" "C:/Users/azhon/Documents/SourceAmerica/Testing/test.mp3"'
os.system("vlc test.mp3 vlc://quit")
soundCmd = "omxplayer test.mp3"
#sound = subprocess.Popen(soundCmd)
while True:
    try:
        text=input("Type something!")
        #sound.kill()
        if text == "quit":
            break
        start = time.time()
        myobj = gTTS(text, lang=language, slow=False) 
        myobj.save("test.mp3")
        print(time.time() - start)
        os.system("vlc test.mp3 vlc://quit")
        #sound = subprocess.Popen(soundCmd)
    except:
        print("No text detected")
