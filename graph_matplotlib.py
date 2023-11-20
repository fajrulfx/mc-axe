import audioop
import pyaudio
import matplotlib.pyplot as plt
import numpy as np

# Open PyAudio stream
p = pyaudio.PyAudio()
CHUNK = 1024 
stream = p.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=CHUNK)
   
def main():
    # Set up plot
    plt.ion() 
    fig = plt.figure(figsize=(10,8))
    ax = fig.add_subplot(111)
    x = np.arange(1,101,1)
    y = [0]*100
    line1, = ax.plot(x, y, 'b-', linewidth=2)  # increase linewidth

    # Add grid, title and labels
    ax.grid(True)
    ax.set_title('Real-time microphone volume')
    ax.set_xlabel('Time')
    ax.set_ylabel('Volume')

    # start RMS measurement
    print("RMS Measurement Started")
    while True:
        data = stream.read(CHUNK, exception_on_overflow=False)
        rms = audioop.rms(data, 2)
        y.pop(0)
        y.append(rms)

        # Remove previous filled area
        for coll in ax.collections:
            coll.remove()
        ax.fill_between(x, y, 0, color='blue', alpha=0.3)  # fill below the line

        line1.set_ydata(y)
        plt.ylim([min(y)-10,max(y)+10])
        plt.draw()
        plt.pause(0.1)

    print("RMS Measurement Stopped")
    stream.close()
    p.terminate()

if __name__ == "__main__":
    main()
