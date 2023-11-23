import pydirectinput as pdi
import pyaudio
import time
import audioop

THRESHOLD = 12500  # Set the intensity level here
HOLD_TIME = 0.4  # Time to hold the click in seconds

def main():
    # setup 
    p = pyaudio.PyAudio()
    CHUNK = 1024  # adjust this value depending on your mic/source
    stream = p.open(format=pyaudio.paInt16, input_device_index=1, channels=1, rate=44100, input=True, frames_per_buffer=CHUNK)
   
    holding_click = False  # Variable to track if we are currently holding down the click
    last_loud_audio_time = None  # Variable to track the time of the last loud audio

    try:
        while True:
            # read audio input
            data = stream.read(CHUNK, exception_on_overflow=False)
            rms = audioop.rms(data, 2)  # here's where we calculate the rms value

            # If loud enough audio is detected, start holding and record the time
            if rms > THRESHOLD:
                if not holding_click:
                    pdi.mouseDown()
                    holding_click = True
                    print('Mouse down')
                last_loud_audio_time = time.time()  

            # If we are holding the click and it's been quiet for the specified HOLD_TIME, release 
            if holding_click and (time.time() - last_loud_audio_time >= HOLD_TIME):
                pdi.mouseUp()
                holding_click = False
                print('Mouse up')

            time.sleep(0.01)  # Short sleep to prevent high CPU usage

    except KeyboardInterrupt:
        # Ensure we clean up and release the mouse if interrupted
        if holding_click:
            pdi.mouseUp()
        stream.close()
        p.terminate()
        print('Program interrupted and terminated')
        
if __name__ == '__main__':
    main()
