import asyncio, websockets


endpoint_gui_queue = asyncio.Queue()
gui_endpoint_queue = asyncio.Queue()




async def clientHandlerTCP(reader, writer):
    message = (await reader.read(255)).decode('utf8')
    print("Message Recieved from Endpoint=", message)
    await endpoint_gui_queue.put(message)

    writer.close()

    
async def tcpServer():
    server = await asyncio.start_server(clientHandlerTCP, '127.0.0.1', 6205)
    async with server:
        await server.serve_forever()



async def clientHandlerWS(websocket):
    print("WS Client Connected")
    while True:
        message = await endpoint_gui_queue.get()
        await websocket.send(message)


async def wsServer():
    
    async with websockets.serve(clientHandlerWS, "localhost", 8765):
        await asyncio.Future()  # run forever

async def main():
    tcp_server_task = asyncio.create_task(tcpServer())
    ws_server_task = asyncio.create_task(wsServer())
    await tcp_server_task



asyncio.run(main())