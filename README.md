# Instrument Server Scout Plugin Example

Instrument Server Scout Plugin Example is an [Instrument Server](https://github.com/Terrabits/instrument-server) microservice for controlling an RFFE via a SignalCraft Scout MIPI interface.

## Requirements

-   Python ~= 3.7
-   instrument-server ~= 1.3.7
-   pyserial ~= 3.5
-   A SignalCraft Scout MIPI Interface

## Install

Run `scripts/install` to install a known-good package and version set.

See the lock file for details:

[requirements.txt.lock](./requirements.txt.lock)

## Scout Device Plugin

### Background

The Instrument Server Device Plugin interface is used to include support for additional busses and device types.

Device Plugins are typically subclasses of the `instrument_server.device.Base` class.

Device Plugins are required to implement the following methods.

```python
Device.__init__(self, **settings)
Device.read(self)
Device.write(self, bytes)
Device.close(self)
```

Note that the device `Base` class implements `Base.query(self, bytes)`, which uses `Device.read` and `Device.write`.

### Scout

The `Scout` device plugin can be found in [plugins/devices/scout.py](plugins/devices/scout.py).

Internally, `Scout` uses `pyserial` to connect.

#### `Scout.__init__`

All `kwargs` (in `**settings`) are passed directly to the `pyserial` `Serial.__init__` constructor:

~~~python
def __init__(self, **settings):
      self.serial = Serial(**settings)
~~~

From [`Serial.__init__` docs](https://pythonhosted.org/pyserial/pyserial_api.html#serial.Serial.__init__), parameters include:

| Key                | Description                                                    |
| ------------------ | -------------------------------------------------------------- |
| port               | Device name                                                    |
| baudrate           | (int) Baud rate such as 9600 or 115200 etc.                    |
| bytesize           | FIVEBITS, SIXBITS, SEVENBITS, EIGHTBITS                        |
| parity             | PARITY_NONE, PARITY_EVEN, PARITY_ODD PARITY_MARK, PARITY_SPACE |
| stopbits           | STOPBITS_ONE, STOPBITS_ONE_POINT_FIVE, STOPBITS_TWO            |
| timeout            | (float) Set a read timeout value.                              |
| xonxoff            | (bool) Enable software flow control.                           |
| rtscts             | (bool) Enable hardware (RTS/CTS) flow control.                 |
| dsrdtr             | (bool) Enable hardware (DSR/DTR) flow control.                 |
| write_timeout      | (float) Set a write timeout value.                             |
| inter_byte_timeout | (float) Inter-character timeout, None to disable (default).    |

#### `Scout.read`

`Scout.read` calls `Serial.readall` and returns all data.

```python
def read(self):
      return self.serial.readall()
```

#### `Scout.write`

`Scout.write` calls `Serial.write` with argument `bytes`. It also suppresses the Scout's echo.

```python
def write(self, bytes):
      self.serial.write(bytes)
      self._ignore_echo()
```

#### `Scout.close`

```python
def close(self):
      self.serial.close()
```

## Project Config File

Every `instrument-server` project is required to include a YAML config file. By convention, the config file must contain the following sections:

```yaml
plugins: {...}
devices: {...}
# Translation Commands (Optional)
...
```

The config file for this project is [scout_plugin_example.yaml](scout_plugin_example.yaml). Each section of the file is explained below.

### Plugins

The `Scout` device plugin is imported from the local directory `plugins.devices.scout`.

No configuration settings are required.

```yaml
plugins:
  plugins.devices.scout: {}
```

This plugin declares device `type` `scout`, which is referenced in the `devices` section below.

### Devices

We use the `scout` device plugin to define a device named `rffe` with the following connection settings:

```yaml
rffe:
  type:     scout
  port:     /dev/tty.usbmodem1234
  baudrate: 115200
  timeout:  0.001
```

Edit `port` to include the correct port of the RFFE.

See [Serial.__init__](https://pythonhosted.org/pyserial/pyserial_api.html#serial.Serial.__init__) for more connection settings.

### Commands

An `instrument-server` project file may include `Translation` command definition(s). `scout_plugin_example.yaml` defines one `Translation` command `init`.

```yaml
init:
  - rffe: mode 1      # RFFE mode
  - rffe: vio  2      # Vio = 2 V
  - rffe: clk  39000  # clock: 39 KHz
```

## Start

Run `scripts/start` to serve `scout_plugin_example.yaml` on all network interfaces on port `9000`.

`scripts/start` calls the `instrument-server` Command Line Interface (CLI), which provides additional settings.

From `instrument-server --help`:

```comment
usage: instrument-server [-h] [--address ADDRESS] [--port PORT]
                         [--termination TERMINATION] [--debug-mode]
                         config_filename

Command Line Interface for starting Instrument Server microservices

positional arguments:
  config_filename

optional arguments:
  -h, --help            show this help message and exit
  --address ADDRESS, -a ADDRESS
                        Set listening address. Default: 0.0.0.0
  --port PORT, -p PORT  Set listening port. Default: random
  --termination TERMINATION, -t TERMINATION
                        Set the termination character. Default: "\n"
  --debug-mode, -d      print debug info to stdout
```

## Client Script

The `client.py` script is provided for testing. It connects to the Instrument Server Scout Plugin Example microservice, sends `init`, then checks for errors.

`client.py` can be run from the command line as follows:

```shell
scripts/start-in-background
# => Running on 0.0.0.0:9000...

# run client
python client.py
```

Note that `client.py` generates no output on success. If error(s) occur, they will be printed to `stdout`.

## References

-   [Introduction to YAML](https://dev.to/paulasantamaria/introduction-to-yaml-125f)
-   [instrument-server](https://github.com/Terrabits/instrument-server)
