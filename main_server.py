from server import IndustrialIoTServer

if __name__ == "__main__":
    server = IndustrialIoTServer(host_ip="127.0.0.1", port=5020)
    server.start()
