import socket
import threading
from pcaspy import Driver, SimpleServer

# Define PVs
prefix = "TCPDATA:"
pvdb = {
    "FLOAT": {
        "prec": 3,
        "unit": "V",
        "scan": 0.1,
        "type": "float"
    }
}

# EPICS PV Driver
class TCPDriver(Driver):
    def __init__(self):
        super().__init__()
        self.setParam("FLOAT", 0.0)

    def update_float(self, value):
        self.setParam("FLOAT", value)
        self.updatePVs()

# TCP Listener
def tcp_listener(driver, host='120.10.10.247', port=4024):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        while True:
            data = s.recv(1024)
            if not data:
                break
            try:
                val = float(data.decode().strip())
                print("Received:", val)
                driver.update_float(val)
            except ValueError:
                continue

# Main EPICS Server
def main():
    server = SimpleServer()
    server.createPV(prefix, pvdb)
    driver = TCPDriver()

    threading.Thread(target=tcp_listener, args=(driver,), daemon=True).start()

    print("EPICS TCP IOC running...")
    while True:
        server.process(0.1)

if __name__ == "__main__":
    main()
