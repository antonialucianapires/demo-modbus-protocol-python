from client import IndustrialIoTClient

def main():
    server_ip = "127.0.0.1"
    port = 5020    
    scan_interval = 1.0 
    client = IndustrialIoTClient(server_ip, port, scan_interval)
    client.run()

if __name__ == "__main__":
    main()
