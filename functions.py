import pathlib,pyaudio,time,pyperclip,math,os
import tensorflow as tf
import pyautogui as pya
import numpy as np
from tkinter import *
from win32api import GetSystemMetrics

snipAI = tf.saved_model.load(pathlib.Path("SnipAI"))
terminateAI = False

_width = GetSystemMetrics(0)/2
_height = GetSystemMetrics(1)/2

def prepare_audio(waveform):
  x = waveform/32768
  x = tf.convert_to_tensor(x, dtype=tf.float32)
  x = tf.expand_dims(x,0)
  return x

FRAMES_PER_BUFFER=3200
FORMAT=pyaudio.paInt16
CHANNELS=1
RATE = 16000
p = pyaudio.PyAudio()

def recAudio():
    stream = p.open(
        rate=RATE,
        channels=CHANNELS,
        format=FORMAT,
        input=True,
        frames_per_buffer=FRAMES_PER_BUFFER
    )

    frames=[]
    seconds=1
    for i in range(0, int(RATE/FRAMES_PER_BUFFER * seconds)):
        data=stream.read(FRAMES_PER_BUFFER)
        frames.append(data)
    
    stream.stop_stream()
    stream.close()

    return np.frombuffer(b''.join(frames), dtype=np.int16)

def kill_pyaudio():
    p.terminate()

def get_spec(waveform):
  spectrogram = tf.signal.stft(
      waveform, frame_length=255, frame_step=128)
  spectrogram = tf.abs(spectrogram)
  spectrogram = spectrogram[..., tf.newaxis]
  return spectrogram

def predict_speech():
    audio = recAudio()
    audio = prepare_audio(audio)
    audio = get_spec(audio)
    prediction = snipAI.model(audio,  training=False)
    label_pred = np.argmax(prediction,axis=1)
    cmds = ['environment','stop','up','yes']
    command = cmds[label_pred[0]]
    return command

quit=False
def quitFn():
        quit=True


def tk_loop(fxn):
    win=Tk()
    Label(win,bg="black",fg="green",text="Say 'yes' to copy highlighted text",font=("Helvetica","9")).pack()
    Label(win,bg="black",fg="green",text="Say 'stop' to pause copying functions",font=("Helvetica","9")).pack()
    Label(win,bg="black",fg="green",text="Say 'up' to resume copying functions",font=("Helvetica","9")).pack()
    q = Button(win,
        text="Start Listening",
        width=100,height=30,
        activebackground="green",
        activeforeground="yellow",
        command=lambda:[quitFn(),win.destroy()],
        cursor="circle",
        relief=RAISED,
        pady=30,padx=30,
        font=("Helvetica","16","bold")
        )
    q.pack()
    win.overrideredirect(True)
    win['bg']="black"
    win.geometry("250x120+"+str(math.floor(_width-125))+"+"+str(math.floor(_height-80)))
    win.attributes('-topmost',True)
    win.mainloop()
    print("\nListening for: \n\t'yes',\n\t'stop',\nhit Uppercase [Z] \nto terminate.\n")
    fxn(terminateAI)

def highlight_copy(previousSnip):
    pyperclip.copy("")
    try:
        pya.hotkey('ctrl','c')
    except:
        print()
    snip = pyperclip.paste()
    time.sleep(.01)
    
    
    if snip != "" and snip != '\r\n':
        snip = snip.replace('\r\n','\r')
        if snip != previousSnip:
            with open("snips.html", "a") as f:
                if os.path.getsize("snips.html") == 0:
                    f.write("!DOCTYPE html\n<html>\n<link rel=\"text/css\" href=\"css/snip.css\">\n<body>\n\n")
                f.write("<snip-pet>\n")
                f.write(snip)
                f.write("\n</snip-pet>\n\n<br/><br/>\n")
                f.close()
            print("Saved Snip:",snip[0:4]+"...")

    return snip

def check_highlighted_text():
    try:
        time.sleep(1)
        pyperclip.copy("")
        pya.hotkey('ctrl','c')
        highlight = pyperclip.paste()
        if highlight != "":
            pyperclip.copy("")
            return True
        return False
    except:
        time.sleep(0.1)
        return False

def stop_UI():
    ui=Tk()
    Button(ui,
        text="Resume",
        width=100,height=30,
        command=lambda:[ui.destroy()],
        cursor="circle",
        relief=RAISED,
        pady=30,padx=30,
        font=("Helvetica","16","bold")
        ).pack()
    ui.geometry("250x80+"+str(math.floor(_width-125))+"+"+str(math.floor(_height-80)))
    ui.attributes('-topmost',True)
    ui.update()
    ui.attributes('-topmost',False)
    ui.title(' ')
    ui.mainloop()