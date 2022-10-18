import asyncio, socket

async def clientHandler(reader, writer):
    request = (await reader.read(255)).decode('utf8')
    response = str(request)
    writer.write(response.encode('utf8'))
    writer.close()

async def runServer():
    server = await asyncio.start_server(clientHandler, '127.0.0.1', 6205)
    async with server:
        await server.serve_forever()

asyncio.run(runServer())