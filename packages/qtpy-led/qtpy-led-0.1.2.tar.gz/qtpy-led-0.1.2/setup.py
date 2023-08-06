# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['qtpy_led']

package_data = \
{'': ['*']}

install_requires = \
['PyAutoGUI>=0.9.53,<0.10.0', 'QtPy>=2.3.0,<3.0.0', 'numpy>=1.24.2,<2.0.0']

setup_kwargs = {
    'name': 'qtpy-led',
    'version': '0.1.2',
    'description': 'Simple LED widget for QyPt',
    'long_description': '# qtpy_led\nSimple LED widget for QtPy.  \nForked from [pyqt_led](https://github.com/Neur1n/pyqt_led) by Neur1n and modified to work with QtPy.\n\n![on](./screenshots/on.png)\n![off](./screenshots/off.png)\n\n## Table of Contents\n- [Installation](#installation)\n- [Usage](#usage)\n- [Tips](#tips)\n- [License](#license)\n\n## Installation\n### pip\n```\n$ pip install qtpy-led\n```\n\n### poetry\n```\n$ poetry install\n```\n\n## Usage\nThe following example is also provided in the package, and will result in the screenshots shown above.\n\n```python\nfrom qtpy.QtCore import Qt\nfrom qtpy.QtWidgets import QApplication\nfrom qtpy.QtWidgets import QGridLayout\nfrom qtpy.QtWidgets import QWidget\nfrom qtpy_led import Led\nimport numpy as np\nimport sys\n\n\nclass Demo(QWidget):\n    def __init__(self, parent=None):\n        QWidget.__init__(self, parent)\n        self._shape = np.array(["capsule", "circle", "rectangle"])\n        self._color = np.array(\n            ["blue", "green", "orange", "purple", "red", "yellow"]\n        )\n        self._layout = QGridLayout(self)\n        self._create_leds()\n        self._arrange_leds()\n\n    def keyPressEvent(self, e):\n        if e.key() == Qt.Key_Escape:\n            self.close()\n\n    def _create_leds(self):\n        for s in self._shape:\n            for c in self._color:\n                exec(\n                    \'self._{}_{} = Led(self, on_color=Led.{}, \\\n                      shape=Led.{}, build="debug")\'.format(\n                        s, c, c, s\n                    )\n                )\n                exec("self._{}_{}.setFocusPolicy(Qt.NoFocus)".format(s, c))\n\n    def _arrange_leds(self):\n        for r in range(3):\n            for c in range(6):\n                exec(\n                    "self._layout.addWidget(self._{}_{}, {}, {}, 1, 1, \\\n                      Qt.AlignCenter)".format(\n                        self._shape[r], self._color[c], r, c\n                    )\n                )\n                c += 1\n            r += 1\n\n\napp = QApplication(sys.argv)  # type: ignore\ndemo = Demo()\ndemo.show()\nsys.exit(app.exec_())\n\n```\n\n## Tips\n- If you want to be able to toggle the LED, then either use `setEnable(True)` or pass an empty string to the `build` argument in Led.\n- The `status_changed` signal will emit a boolean when the LED\'s state has changed.\n- Currently, the only way to shrink the LED beyond the default size is to use `setFixedSize` \n\n## License\n\n[MIT License](LICENSE). Copyright (c) 2023 crash8229.\n',
    'author': 'crash8229',
    'author_email': 'mu304007@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/crash8229/qtpy_led',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
