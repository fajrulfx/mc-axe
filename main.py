import audioop
import pyaudio
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class RealtimeGraph(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.setupGraph()
        self.startRMSMeasurement()
        
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("RealtimeGraph")
        MainWindow.resize(800, 600)
        
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        
        self.graphLayout = QtWidgets.QVBoxLayout()
        self.graphLayout.setObjectName("graphLayout")
        
        self.gridLayout.addLayout(self.graphLayout, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
    def setupGraph(self):
        self.figure = Figure(figsize=(10, 8))
        self.canvas = FigureCanvas(self.figure)
        self.graphLayout.addWidget(self.canvas)
        
        self.ax = self.figure.add_subplot(111)
        self.x = np.arange(1, 101, 1)
        self.y = [0] * 100
        self.y_line = [0] * 100
        self.line, = self.ax.plot(self.x, self.y_line, 'b-', linewidth=2)
        self.fill = self.ax.fill_between(self.x, self.y, 0, color='blue', alpha=0.3)
        self.ax.set_xlim(0, 100)
        self.ax.set_ylim(0, 20000)
        self.ax.grid(True)
        self.ax.set_title('Real-time microphone volume')
    
    def startRMSMeasurement(self):
        self.p = pyaudio.PyAudio()
        self.CHUNK = 1024
        self.stream = self.p.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=self.CHUNK, 
                                  stream_callback=self.updateGraph)
        self.stream.start_stream()
        
    def updateGraph(self, in_data, frame_count, time_info, status):
        rms = audioop.rms(in_data, 2)
        self.y.pop(0)
        self.y.append(rms)

        self.line.set_ydata(self.y)
        self.fill.remove()
        self.fill = self.ax.fill_between(self.x, self.y, 0, color='blue', alpha=0.3)
        self.canvas.draw()
        
        return (in_data, pyaudio.paContinue)
    
    def closeEvent(self, event):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    app.setStyle('Fusion')
    window = RealtimeGraph()
    window.show()
    app.exec_()
