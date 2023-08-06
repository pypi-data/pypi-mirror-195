# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['canvas_course_tools']

package_data = \
{'': ['*'], 'canvas_course_tools': ['templates/*']}

install_requires = \
['appdirs>=1.4.4,<2.0.0',
 'canvasapi>=2.2.0,<3.0.0',
 'click>=8.1.3,<9.0.0',
 'jinja2>=3.1.2,<4.0.0',
 'python-dateutil>=2.8.1,<3.0.0',
 'rich-click>=1.5.2,<2.0.0',
 'rich>=12.5.1,<13.0.0',
 'tomli-w>=1.0.0,<2.0.0',
 'tomli>=2.0.1,<3.0.0']

entry_points = \
{'console_scripts': ['canvas = canvas_course_tools.cli:cli']}

setup_kwargs = {
    'name': 'canvas-course-tools',
    'version': '0.5.0',
    'description': 'Canvas course tools',
    'long_description': "# canvas-course-tools\n\nCanvas course tools was created at the physics practicals at the Vrije\nUniversiteit Amsterdam to greatly reduce the time needed to create class lists\n(with photos!) for staff and teaching assistants. Class lists are also created\nfor students so that they can easily lookup their assigned experiments and TA's.\nFurthermore, we use it to create student groups on Canvas for peer feedback.\n\nThis package provides the `canvas` command-line utility. After registering a\nCanvas URL and API key (which you can generate on your profile settings page)\nthis tool allows you to list courses and students in different sections of your\ncourses. The output has a light markup and is ideally suited for saving as a\ntext file. It is then easy to copy and move lines inside the file to create\nstudent groups. The file can then be parsed by the `canvas templates` command to\nrender templates based on the text file. This allows for creating class lists\n(with short notes for each student) and even class lists with photos (if you\nprovide photos).\n\nYou can also use this tool to create groups and group sets on Canvas based on a\ngroup list file.",
    'author': 'David Fokkema',
    'author_email': 'd.b.r.a.fokkema@vu.nl',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/davidfokkema/canvas-course-tools',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
