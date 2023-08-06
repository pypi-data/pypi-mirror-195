# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src',
 'mnemocards_anki': 'src/mnemocards_anki',
 'mnemocards_essentials': 'src/mnemocards_essentials'}

packages = \
['mnemocards', 'mnemocards_anki', 'mnemocards_essentials']

package_data = \
{'': ['*']}

install_requires = \
['fire>=0.5.0,<0.6.0',
 'pydantic>=1.10.4,<2.0.0',
 'pyyaml>=6.0,<7.0',
 'rich>=13.2.0,<14.0.0']

entry_points = \
{'console_scripts': ['mnemocards = mnemocards.__main__:main']}

setup_kwargs = {
    'name': 'mnemocards',
    'version': '1.0.0a0',
    'description': "In addition to helping you memorise, this code helps you do other things that I don't remember...",
    'long_description': '<p align="center">\n    <a href="https://guiferviz.github.io/mnemocards" target="_blank">\n        <img src="/mnemocards/images/logo.jpg"\n             alt="Mnemocards logo"\n             width="200">\n    </a>\n</p>\n<p align="center">\n    <a href="https://github.com/guiferviz/mnemocards/actions/workflows/cicd.yaml" target="_blank">\n        <img src="https://github.com/guiferviz/mnemocards/actions/workflows/cicd.yaml/badge.svg"\n             alt="Mnemocards CI pipeline status">\n    </a>\n    <a href="https://app.codecov.io/gh/guiferviz/mnemocards/" target="_blank">\n        <img src="https://img.shields.io/codecov/c/github/aidictive/mnemocards"\n             alt="Mnemocards coverage status">\n    </a>\n    <a href="https://github.com/guiferviz/mnemocards/issues" target="_blank">\n        <img src="https://img.shields.io/github/issues/guiferviz/mnemocards"\n             alt="Mnemocards issues">\n    </a>\n    <a href="https://github.com/aidictive/mnemocards/graphs/contributors" target="_blank">\n        <img src="https://img.shields.io/github/contributors/guiferviz/mnemocards"\n             alt="Mnemocards contributors">\n    </a>\n    <a href="https://pypi.org/project/mnemocards/" target="_blank">\n        <img src="https://pepy.tech/badge/mnemocards"\n             alt="Mnemocards total downloads">\n    </a>\n    <a href="https://pypi.org/project/mnemocards/" target="_blank">\n        <img src="https://pepy.tech/badge/mnemocards/month"\n             alt="Mnemocards downloads per month">\n    </a>\n    <br />\n    In addition to helping you memorise, this code helps you do other things that I don\'t remember...\n</p>\n\n---\n\n:books: **Documentation**:\n<a href="https://guiferviz.com/mnemocards" target="_blank">\n    https://guiferviz.com/mnemocards\n</a>\n\n:keyboard: **Source Code**:\n<a href="https://github.com/guiferviz/mnemocards" target="_blank">\n    https://github.com/guiferviz/mnemocards\n</a>\n\n---\n\n## 🤔 What is this?\n\n**Mnemocards** is a Python package originally intended for creating Anki\nflashcards from text files. It allows users to define a series of steps to read\nflashcards from any source, transform them and export them to different formats\nsuch as Anki APKG packages. Mnemocards is designed to be fully extensible,\nwhich means that users can create their own tasks and customize the card\ngeneration process to their specific needs.\n\nReading **flashcards from text files** has several **advantages** over binary\nformats or manually creating cards in the Anki app. Text files are easily\nreadable and editable by humans. This means that users can easily understand\nand modify the flashcard content **using common text editors**, and also can\nuse version control systems like **Git to track changes and collaborate** with\nothers.\n\n\n## 🏷️ Features\n\n* Generates Anki APKG packages that you can later import into the Anki app.\n* Auto generate pronunciations from the words that you are learning.\n* Generates flashcards from text files that can be stored in Git repositories.\nThis brings several positive things:\n    * Keep track of changes.\n    * Maintain different versions of flashcards using Git branches.\n    * Easily share and collaborate with others. If you know how to work with\n      Git you can create forks and pull requests to existing repositories.\n* Fully extensible architecture that allows you to define tasks that perform\ncustom transformations on a list of notes.\n    * Possibility to export flashcards to other existing flashcards apps.\n    * Create indexes or analyze your collection of cards, create\n      visualizations, clustering, analyze how the cards relate to each other...\n\n\n## 🤓 How it works?\n\nTo get started with Mnemocards, you\'ll need to have Python >= 3.10 installed on\nyour computer. Then, you can install Mnemocards using `pip`:\n\n```cmd\n$ pip install mnemocards\n```\n\nYou can check that the installation went well by executing the following\ncommand:\n\n```cmd\n$ mnemocards --version\n╔╦╗╔╗╔╔═╗╔╦╗╔═╗┌─┐┌─┐┬─┐┌┬┐┌─┐\n║║║║║║║╣ ║║║║ ║│  ├─┤├┬┘ ││└─┐\n╩ ╩╝╚╝╚═╝╩ ╩╚═╝└─┘┴ ┴┴└──┴┘└─┘ X.Y.Z\n╭────────────────────────────────╮\n│ <A super mega funny joke here> │\n╰────────────────────────────────╯\n```\n\nIf the joke made you laugh you can continue with this tutorial, otherwise this\nprogram is not for you and you should consider other alternatives.\n\nOnce you have Mnemocards installed, you can start creating your own flashcards.\nLet\'s start creating our own vocabulary file.\n\nYou can use the provided sample files as a starting point, or create your own.\nMnemocards uses a configuration file to define the steps that will be used to\nprocess the flashcards. In this file, you can specify the tasks that you want\nto use, the order in which they will be executed, and any necessary parameters\nor settings.\n\nHere\'s an example of a simple configuration file that reads in a CSV file containing flashcard data, and then generates an Anki APKG package:\n\n```yaml\nsteps:\n  - type: ReadFile\n    path: flashcards.csv\n  - type: Anki\n    deck:\n      name: My Flashcards\n      id: b45f6d48-d1ab-4d0e-80a9-08a2ab473a41\n    note_type:\n      type: BasicNoteType\n  - type: Package\n```\n\nIn this example, the first step reads in a CSV file called "flashcards.csv", the second step generates an Anki package with a deck named "My Flashcards" and a specific id, and the last step creates the APKG package.\n\nYou can run the configuration file using the mnemocards command:\n\nCopy code\nmnemocards run my_config.yml\nThis will execute the steps in the configuration file, and create the Anki APKG package.\n\nYou can also use the package to export your flashcards to other flashcard apps like Quizlet by adding a Quizlet task to the configuration file and providing the necessary credentials.\n\nWith Mnemocards, you can customize the flashcard generation process to suit your needs and easily collaborate with others. Give it a try and see how it can help you learn more efficiently!\n\nTODO\n\n\n## 🧪 Examples\n\n<details markdown>\n<summary markdown>Japanese Flashcards :jp:</summary>\nThinks you will learn:\n\n* UnionPipeline task.\n* Audio generation.\n</details>\n\n\n## DELETEME: Fast ideas\n\nMnemocards is a tool for processing your flashcards.\nMnemocards first appeared with the objective of generating Anki APKG packages that you can later import into the Anki app.\nMnemocards allow us to generate our cards from text files that we can store in repositories.\nHaving text files in repos allow us to keep track of the changes, maintain different versions of our flashcards and easily collaborate with others (creating forks of existing projects or creating pull requests, for example).\nIt is fully extensible, you can define tasks that perform transformations on a list of notes.\nYou can also auto generate pronunciations from the words that you are learning.\nYou may even export your flashcards to other existing flashcards apps.\nThe possibilities are endless, you can create an index or somehow analyze your collection of cards, create visualizations, clustering, analyze how the cards relate to each other...\n',
    'author': 'guiferviz',
    'author_email': 'guiferviz@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/guiferviz/mnemocards',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
