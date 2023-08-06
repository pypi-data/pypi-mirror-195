# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['demos',
 'flexsea',
 'flexsea.specs',
 'flexsea.specs._api_specs',
 'flexsea.specs.device_specs']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.26.8,<2.0.0',
 'pyserial>=3.5,<4.0',
 'semantic-version>=2.10.0,<3.0.0']

entry_points = \
{'console_scripts': ['flexsea-demos = demos.console.main:main']}

setup_kwargs = {
    'name': 'flexsea',
    'version': '10.1.3',
    'description': '',
    'long_description': '# FlexSEA\n\n\n`flexsea` is a Python package for interacting with Dephy\'s wearable robotic devices.\nIt can be used for gathering data from a device or for writing your own controller.\n\n\n## Installation\n\nIt is **strongly** recommended that you install `flexsea` in a [virtual environment](https://docs.python.org/3/library/venv.html).\nAdditionally, `flexsea` requires [Python >= 3.11](https://www.python.org/downloads/release/python-3111/), and has been tested\non Windows and Ubuntu.\n\n**NOTE**: These instructions use the `python3` executable. If you are on Windows, you\nwill need to replace `python3` -> `python`.\n\n### Pip\n\n```bash\npython3 -m pip install flexsea\n```\n\n\n### From Source\n\nIn order to install from source, you will need [git](https://git-scm.com/downloads).\n\n```bash\ngit clone https://github.com/DephyInc/Actuator-Package.git\ncd Actuator-Package/\ngit checkout v10.0.0 # Or the branch you want\npython3 -m pip install .\n```\n\n\n## Usage\n\n### Demos\n\nA good reference for what `flexsea` is capable of and how various tasks, such as\ncontrolling the device\'s motor, can be accomplished, is the collection of demo scripts\nthat live in the `demos/` directory of the repository. There are currently six demos,\nand they should be viewed in order, as each successive demo builds off of the information\npresented in the previous one.\n\n\n### API Overview\n\n#### Importing and Instantiating\nThe central object in `flexsea` is the `Device` class. For most use cases, this is the\nonly aspect of `flexsea` that you will need to interact with directly. You can import\nit into your code like so:\n\n```python\nfrom flexsea.device import Device\n```\n\nThe constructor takes five keyword arguments:\n\n```python\nclass Device(\n    port: str="",\n    baudRate: int=cfg.baudRate,\n    cLibVersion: str=cfg.LTS,\n    logLevel: int=4,\n    loggingEnabled: bool=True\n)\n```\n\n* `port`: The name of the serial port that the device is connected to. On Windows, this is typically something akin to "COM3" and on Linux it is usually something like "/dev/ttyACM0". If you do not provide a value, `flexsea` will scan through all of the available serial ports, stopping at the first valid device that it finds. This means that this keyword is typically only useful if you have more than one device connected at once.\n* `baudRate`: The baud rate used for communicating with the device. Most of Dephy\'s devices all use the same baud rate, which is set as the default value for you.\n* `cLibVersion`: `flexsea` is a wrapper around a pre-compiled C library that actually handles all of the heavy lifting of communicating with the device. This parameter allows you to specify the semantic version string of the version of this library that you would like to use. These libraries are stored in a public AWS S3 bucket. If you do not already have the version you specify installed, then `flexsea` will attempt to download it from this bucket for you. By default, the latest LTS version is selected for you. In most cases, changing this value is only necessary for bootloading.\n* `logLevel`: Under the hood, the pre-compiled C library makes use of the [spdlog](https://github.com/gabime/spdlog) logging library. This parameter controls the verbosity of the logs, with `0` being the most verbose and `6` disabling logging all together.\n* `loggingEnabled`: If set to `True` then both data and debug logs will be generated (unless `logLevel=6`). If `False`, then no logs are generated, regardless of the value of `logLevel`.\n\nTypically, all you\'ll need to do to create an instance of the object is:\n\n```python\ndevice = Device()\n```\n\n#### Connecting and Streaming\n\nOnce instantiated, you need to establish a connection between the computer and the device. This is done via the `open` method:\n\n```python\ndevice.open()\n```\n\nAdditionally, if you would like the device to send its data to the computer -- an action called *streaming* -- then you must invoke the `start_streaming` method:\n\n```python\ndevice.start_streaming(frequency)\n```\n\nwhere `frequency` is the rate (in Hertz) at which the device will send data.\n\n**NOTE**: Currently, the maximum supported frequency is 1000Hz.\n\n\n#### Reading and Printing\n\nIf you are streaming, you can get the most recent device data from the `read` method:\n\n```python\ndata = device.read()\n```\n\nWhere `data` is a dictionary. The available fields depend on the type of device as well as the firmware version. If you have not read from the device in a while, you can get all of the data that\'s currently in the device\'s internal queue by using the `allData` keyword:\n\n```python\nallData = device.read(allData=True)\n```\n\nIn this case, the return value `allData` will be a list of dictionaries, one for each time stamp.\n\nTo conveniently display the most recent data:\n\n```python\ndevice.print()\n```\n\n`print` takes an optional keyword argument called `data`, which should be a dictionary returned by `read`. This lets you display data that was read at some arbitrary point in the past.\n\n\n#### Controlling the Motor\n```python\ndevice.command_motor_current(current) # milliamps\ndevice.command_motor_position(position) # motor ticks\ndevice.command_motor_voltage(voltage) # millivolts\ndevice.command_motor_impedance(position) # motor ticks\ndevice.stop_motor()\ndevice.set_gains(kp, ki, kd, k, b, ff) # See below\n```\n\nWhen setting the gains:\n\n* `kp`: The proportional gain\n* `ki`: The integral gain\n* `kd`: The differential gain\n* `k`: The stiffness gain for impedance control\n* `b`: The damping gain for impedance control\n* `ff`: The feed-forward gain\n\n\n#### Device State\n\nYou can also introspect certain aspects of the device\'s state, depending on the firmware version you\'re running:\n\n* `isOpen` : Indicates whether or not the computer and the device are connected\n* `isStreaming`: Indicates whether or not the device is sending data\n* `deviceName`: The name of the type of the device, e.g., "actpack"\n* `deviceSide`: Either "left" or "right", if applicable; `None` otherwise. **Requires firmware >= v10.0.0**.\n* `libsVersion`: The semantic version string of the pre-compiled C library being used. **Requires >= v10.0.0 of the pre-compiled C library**.\n* `firmware`: The semantic version string of the firmware version\n* `uvlo`: Used to both get and set the device\'s UVLO in millivolts\n\n\n#### Cleaning Up\n\nWhen finished commanding the device, it is good practice to call the `close` method:\n\n```python\ndevice.close()\n```\n\nAdditionally, when done streaming, you can call the `stop_streaming` method:\n\n```python\ndevice.stop_streaming()\n```\n\n**NOTE**: `stop_streaming` is called automatically by `close`, and `close` is called automatically by the `Device` class\' destructor\n',
    'author': 'Jared',
    'author_email': 'jcoughlin@dephy.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.11.0rc1,<4.0.0',
}


setup(**setup_kwargs)
