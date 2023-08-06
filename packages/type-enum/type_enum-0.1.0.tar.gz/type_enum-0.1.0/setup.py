# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['type_enum']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'type-enum',
    'version': '0.1.0',
    'description': 'Concise sum types in Python.',
    'long_description': '# `type_enum`: Concise sum types in Python\n\n### Installation\n\n```\npip install type-enum\n```\n\n### Usage\n\n```python\nfrom type_enum import TypeEnum\n\nclass BgColor(TypeEnum):\n    transparent = ()\n    name = (str,)\n    rgb = (int, int, int)\n    hsv = (int, int, int)\n\nbackground_color: BgColor = BgColor.rgb(39, 127, 168)\nassert isinstance(background_color, BgColor)\nassert not isinstance(BgColor.rgb, BgColor)  # different from Enum\n\nmatch background_color:\n    case BgColor.transparent():\n        print("no color")\n    case BgColor.name(color_name):\n        print(f"color name: {color_name}")\n    case BgColor.rgb(red, green, blue):\n        print(f"RGB: {red}, {green}, {blue}")\n    case BgColor.hsv(hue, saturation, value):\n        print(f"HSV: {hue}, {saturation}, {value}")\n# will print "RGB: 39, 127, 168"\n```\n\nYou can also specify field names by using a dictionary instead of a tuple:\n\n```python\nfrom type_enum import TypeEnum\n\nclass BgColor(TypeEnum):\n    transparent = ()\n    name = (str,)\n    rgb = {"red": int, "green": int, "blue": int}  # named args\n    hsv = {"hue": int, "saturation": int, "value": int}\n\nbackground_color = BgColor.rgb(red=39, green=127, blue=168)\nassert isinstance(background_color, BgColor)\n\nmatch background_color:\n    case BgColor.transparent():\n        print("no color")\n    case BgColor.name(color_name):\n        print(f"color name: {color_name}")\n    case BgColor.rgb(red=r, green=g, blue=b):\n        print(f"RGB: {r}, {g}, {b}")\n    case BgColor.hsv(hue=h, saturation=s, value=v):\n        print(f"HSV: {h}, {s}, {v}")\n```\n',
    'author': 'Thomas MK',
    'author_email': 'tmke8@posteo.net',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/tmke8/type_enum',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
