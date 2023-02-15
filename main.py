from functions import *
import msvcrt


def mainAI(terminateAI):
    prev=""
    if __name__ == "__main__":
        while not terminateAI:
            command = predict_speech()
            if command == "yes" and check_highlighted_text():
                prev = highlight_copy(prev)
            if command == "stop":
                stop_UI()
            if msvcrt.kbhit():
                if msvcrt.getwch()=="Z":
                    kill_pyaudio()
                    terminateAI=True
            if terminateAI==False:
                time.sleep(1)
                mainAI(terminateAI)
            else:
                print("Quitting..")
                pya.hotkey('alt','f4')


tk_loop(mainAI)