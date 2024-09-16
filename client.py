from pyModbusTCP.client import ModbusClient
from time import sleep

class IndustrialIoTClient:
    def __init__(self, server_ip: str, port: int, scan_interval: float = 1.0):
        self._client = ModbusClient(host=server_ip, port=port)
        self._scan_interval = scan_interval

    def run(self):
        self._client.open()
        try:
            active = True
            while active:
                choice = self._get_user_choice()
                if choice == '1':
                    self._handle_read_operation()
                elif choice == '2':
                    self._handle_write_operation()
                elif choice == '3':
                    self._configure_scan_interval()
                elif choice == '4':
                    self._client.close()
                    active = False
                else:
                    print("Invalid selection")
        except Exception as e:
            print(f'Error during operation: {e}')

    def _get_user_choice(self) -> str:
        return input("Choose operation: (1- Read | 2- Write | 3- Configure | 4- Exit): ")

    def _handle_read_operation(self):
        data_type = int(input("Select data type to read (1- Holding Register | 2- Coil | 3- Input Register | 4- Discrete Input): "))
        address = int(input("Enter MODBUS table address: "))
        num_reads = int(input("Enter the number of reads: "))
        for i in range(num_reads):
            print(f"Read {i + 1}: {self._read_data(data_type, address)}")
            sleep(self._scan_interval)

    def _handle_write_operation(self):
        data_type = int(input("Select data type to write (1- Holding Register | 2- Coil): "))
        address = int(input("Enter MODBUS table address: "))
        value = int(input("Enter value to write: "))
        self._write_data(data_type, address, value)

    def _configure_scan_interval(self):
        scan_time = float(input("Enter desired scan interval [s]: "))
        self._scan_interval = scan_time

    def _read_data(self, data_type: int, address: int):
        if data_type == 1:
            return self._client.read_holding_registers(address, 1)
        elif data_type == 2:
            return self._client.read_coils(address, 1)
        elif data_type == 3:
            return self._client.read_input_registers(address, 1)
        elif data_type == 4:
            return self._client.read_discrete_inputs(address, 1)
        else:
            print(f'Error: Invalid data type {data_type}')
            return 'Error: Invalid data type'

    def _write_data(self, data_type: int, address: int, value: int):
        if data_type == 1:
            return self._client.write_single_register(address, value)
        elif data_type == 2:
            return self._client.write_single_coil(address, value)
        else:
            print(f'Error: Invalid data type for writing {data_type}')