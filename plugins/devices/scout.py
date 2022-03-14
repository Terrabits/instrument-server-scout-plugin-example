from instrument_server.device import Base, DeviceError
from serial                   import Serial


class Scout(Base):
    def __init__(self, **settings):
        self.serial = Serial(**settings)

    def read(self):
        return self.serial.readall()

    def write(self, bytes):
        self.serial.write(bytes)
        self._ignore_echo()

    def close(self):
        self.serial.close()

    # helpers

    def _ignore_echo(self):
        self.serial.readline()


# export
IS_DEVICE_PLUGIN = True
plugin_name      = 'scout'
plugin           = Scout
