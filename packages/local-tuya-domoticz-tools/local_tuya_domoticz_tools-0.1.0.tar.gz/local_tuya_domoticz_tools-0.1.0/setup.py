# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['local_tuya_domoticz_tools',
 'local_tuya_domoticz_tools.plugin',
 'local_tuya_domoticz_tools.units']

package_data = \
{'': ['*']}

install_requires = \
['concurrent-tasks>=1.3,<2', 'local-tuya>=1.2.5,<2', 'xmltodict>=0.13,<0.14']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata>=4,<5']}

setup_kwargs = {
    'name': 'local-tuya-domoticz-tools',
    'version': '0.1.0',
    'description': 'Tools to create a Domoticz plugin for local-tuya devices.',
    'long_description': '# local-tuya-domoticz-tools\nTools to create a Domoticz plugin for local-tuya devices.\n> 💡 The Domoticz version should be `2022.1` or higher.\n\n## Creating the plugin\nTo create a plugin, you will need to create 2 things.\n\n### Plugin metadata\nThis is the XML header that is used to populate the plugin creation page in Domoticz.\nYou can create it using `local_tuya_domoticz_tools.PluginMetadata`.\n\n### Starting the device.\nTo start the plugin, you need to create the device and register the units.\n\nCheck `local_tuya_domoticz_tools.plugin.plugin.OnStart` for the function signature.\n\nUnits should be created using `manager.register(...)`.\n\nFor a switch unit, it would look like:\n```python\nfrom typing import Dict\n\nfrom local_tuya import DeviceConfig, ProtocolConfig\nfrom local_tuya_domoticz_tools import UnitManager, switch_unit\n\nfrom my_device import SwitchState, SwitchDevice\n\n\ndef on_start(\n    protocol_config: ProtocolConfig,\n    _: Dict[str, str],\n    manager: UnitManager[SwitchState],\n) -> SwitchDevice:\n    device = SwitchDevice(config=DeviceConfig(protocol=protocol_config))\n    manager.register(\n        switch_unit(\n            id_=1,\n            name="power",\n            image=9,\n            command_func=device.switch,\n        ),\n        lambda s: s.power,\n    )\n    return device\n```\n\n### Units\nUnits represent a Domoticz device and is associated to a Domoticz hardware.\n\n#### Manager\nThe role of the manager is to\n- create/remove units: `register` method\n- dispatch the commands from units: `on_command` method\n- update units state: `update` method\n\n#### Unit types\n- [switch](./units/switch.py)\n- [selector switch](./units/selector_switch.py)\n- [temperature](./units/temperature.py) (accepts values preprocessor)\n- [set point](./units/set_point.py)\n\nFor common units parameters, see the [base](./units/base.py).\n\n## Installing the plugin\nYou should provide a script that will be used to install the plugin.\nIt would look like:\n```python\nfrom local_tuya_domoticz_tools import install_plugin, PluginMetadata\n\ndef on_start(...):\n    ...\n\n\nif __name__ == "__main__":\n    install_plugin(\n        metadata=PluginMetadata(...),\n        on_start=on_start,\n        import_path="my_device.domoticz",\n    )\n```\n\n> 💡 Domoticz path defaults to `~/domoticz` a `-p` option can be passed to change that.\n\n### Filtering units\nYou can automatically add an option to the plugin to filter created units.\n\nTo enable it, you need to implement `local_tuya_domoticz_tools.UnitId` and add all unit IDs, then simply pass it to the `install` function. `UnitManager.register` will handle device deletion.',
    'author': 'Gabriel Pajot',
    'author_email': 'gab@les-cactus.co',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/gpajot/local-tuya-domoticz-tools',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<3.12',
}


setup(**setup_kwargs)
