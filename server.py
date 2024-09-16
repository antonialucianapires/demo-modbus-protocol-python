from pymodbus.server import StartTcpServer
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.datastore.store import ModbusSequentialDataBlock
from threading import Thread
import random
from time import sleep

class IndustrialIoTServer:
    def __init__(self, host_ip: str, port: int):
        self._context = self._create_modbus_context()
        self._identity = self._create_device_identity()
        self._server_address = (host_ip, port)

    def _create_modbus_context(self) -> ModbusServerContext:
        store = ModbusSlaveContext(
            di=ModbusSequentialDataBlock(0, [0] * 100),
            co=ModbusSequentialDataBlock(0, [0] * 100),
            hr=ModbusSequentialDataBlock(1000, [0] * 100),
            ir=ModbusSequentialDataBlock(0, [0] * 100)
        )
        return ModbusServerContext(slaves=store, single=True)

    def _create_device_identity(self) -> ModbusDeviceIdentification:
        identity = ModbusDeviceIdentification()
        identity.VendorName = 'Pymodbus'
        identity.ProductCode = 'PM'
        identity.VendorUrl = 'http://github.com/riptideio/pymodbus/'
        identity.ProductName = 'Pymodbus Server'
        identity.ModelName = 'Industrial IoT CLP Server'
        identity.MajorMinorRevision = '1.0'
        return identity

    def start(self):
        try:
            server_thread = Thread(target=self._start_modbus_server)
            server_thread.daemon = True
            server_thread.start()
            self._simulate_process()
        except Exception as e:
            print("Error: ", e)

    def _start_modbus_server(self):
        print("Modbus Server running...")
        StartTcpServer(context=self._context, identity=self._identity, address=self._server_address)

    def _simulate_process(self):
        sleep(2)
        while True:
            self._update_registers()
            self._display_register_values()
            sleep(1)

    def _update_registers(self):
        simulated_value = random.randint(int(0.95 * 400), int(1.05 * 400))
        self._context[0].setValues(3, 1000, [simulated_value])

        coil_state = random.randint(0, 1)
        self._context[0].setValues(1, 1000, [coil_state])

    def _display_register_values(self):
        print('======================')
        print("Modbus Table")
        print(f'Holding Register \n R1000: {self._context[0].getValues(3, 1000, count=1)}')
        print(f'Coil \n R1000: {self._context[0].getValues(1, 1000, count=1)}')