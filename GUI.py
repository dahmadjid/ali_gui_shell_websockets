import asyncio, websockets


from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from threading import Thread
from time import sleep
from queue import SimpleQueue

new_messages = SimpleQueue()


async def wsClient():
    async with websockets.connect("ws://localhost:8765") as websocket:
        while True:
            message = await websocket.recv()
            print("Received from TeamServer websockets: ", message)
            new_messages.put_nowait(message)


# GUI:
app = QApplication([])
text_area = QPlainTextEdit()
# text_area.setFocusPolicy(Qt.NoFocus)
message = QLineEdit()
layout = QVBoxLayout()
layout.addWidget(text_area)
layout.addWidget(message)
window = QWidget()
window.setLayout(layout)
window.show()


def startWSConnections():
    asyncio.run(wsClient())


thread = Thread(target=startWSConnections, daemon=True)
thread.start()

def displayNewMessages():
    while new_messages.qsize() > 0:
        text_area.appendPlainText(new_messages.get())

def sendMessage():
    print("Sending message to WS: ", message.text, " (not yet implemented)")
    message.clear()

# Signals:
message.returnPressed.connect(sendMessage)
timer = QTimer()
timer.timeout.connect(displayNewMessages)
timer.start(1000)

app.exec()