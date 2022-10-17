from flask import Flask, request
import threading
import asyncio
from queue import SimpleQueue, Empty



app = Flask(__name__)

tx_queue = SimpleQueue()
rx_queue = SimpleQueue()


@app.route('/', methods=['GET'])
def Home():
    return 'Hello World', 200


@app.route("/post",methods=['POST'])
def testPost():

    str_message = request.form.get('message')

    tx_queue.put_nowait(str_message)
    return '', 200


 
async def sendMessage(message:str, ip:str, port:int) -> str:
    reader, writer = await asyncio.open_connection(ip, port)
    print(f'Send: {message!r}')
    writer.write(message.encode())
    await writer.drain()

    data = await reader.read(100)
    print(f'Received: {data.decode()!r}')

    print('Close the connection')
    writer.close()
    await writer.wait_closed()


async def sendingLoop():
    print("Sending loop started ")
    while True: 
        try:
            message_from_agent = tx_queue.get_nowait()
            print("Recieved: ",message_from_agent)
            await asyncio.create_task(sendMessage(message_from_agent, '127.0.0.1', 6205))
        except Empty:
            await asyncio.sleep(0.01)  # sleep for 10ms if the queue is empty.
        except Exception as e:
            print(e)

        

async def main():
    print("Hello World")

    sending_loop_task = asyncio.create_task(sendingLoop())
    await sending_loop_task
    
    



server_thread = threading.Thread(target=app.run, daemon=True)
    
server_thread.start()
asyncio.run(main())
server_thread.join()
