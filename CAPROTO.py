import asyncio
import struct
from caproto.server import pvproperty, PVGroup, run

HOST = '127.0.0.1'
PORT = 9999

class TCPDataIOC(PVGroup):
    float_val = pvproperty(name='TCPDATA:FLOAT', dtype=float, value=0.0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    async def tcp_reader(self):
        reader, _ = await asyncio.open_connection(HOST, PORT)
        print(f"Connected to TCP server at {HOST}:{PORT}")
        while True:
            data = await reader.readexactly(4)  # assuming 4-byte float
            value = struct.unpack('f', data)[0]
            print(f"Received: {value}")
            await self.float_val.write(value)

async def main():
    ioc = TCPDataIOC()
    # start the IOC and TCP reader concurrently
    await asyncio.gather(
        run(ioc.pvdb, startup_hook=None),  # this starts the Caproto server
        ioc.tcp_reader()  # this starts reading data
    )

if __name__ == "__main__":
    asyncio.run(main())
