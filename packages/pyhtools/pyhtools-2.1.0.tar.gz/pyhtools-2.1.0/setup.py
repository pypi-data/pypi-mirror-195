# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyhtools',
 'pyhtools.UI',
 'pyhtools.attackers',
 'pyhtools.attackers.Android',
 'pyhtools.attackers.Android.forensics',
 'pyhtools.attackers.Android.mitm',
 'pyhtools.attackers.Network',
 'pyhtools.attackers.web',
 'pyhtools.attackers.web.api',
 'pyhtools.attackers.web.vuln_scanner',
 'pyhtools.detectors',
 'pyhtools.evil_files',
 'pyhtools.evil_files.malwares',
 'pyhtools.evil_files.malwares.backdoor.ssh',
 'pyhtools.evil_files.malwares.data_harvesters',
 'pyhtools.evil_files.malwares.installer',
 'pyhtools.evil_files.malwares.keylogger',
 'pyhtools.evil_files.malwares.reverse_backdoor',
 'pyhtools.evil_files.malwares.reverse_backdoor.HTTP',
 'pyhtools.evil_files.malwares.reverse_backdoor.TCP',
 'pyhtools.evil_files.malwares.reverse_backdoor.ssh',
 'pyhtools.evil_files.malwares.telegram_remote_code_executor',
 'pyhtools.evil_files.ransomwares',
 'pyhtools.evil_files.ransomwares.dmsec',
 'pyhtools.evil_files.worms']

package_data = \
{'': ['*']}

install_requires = \
['aiodns>=3.0.0,<4.0.0',
 'aiohttp>=3.8.4,<4.0.0',
 'beautifulsoup4>=4.11.2,<5.0.0',
 'colorama>=0.4.6,<0.5.0',
 'frida-tools>=12.1.1,<13.0.0',
 'kamene>=0.32,<0.33',
 'nuitka>=1.4.8,<2.0.0',
 'paramiko>=3.0.0,<4.0.0',
 'prettytable>=3.6.0,<4.0.0',
 'psutil>=5.9.4,<6.0.0',
 'pure-python-adb>=0.3.0.dev0,<0.4.0',
 'pyfiglet>=0.8.post1,<0.9',
 'pynput>=1.7.6,<2.0.0',
 'pytelegrambotapi>=4.10.0,<5.0.0',
 'requests>=2.28.2,<3.0.0',
 'scapy>=2.5.0,<3.0.0',
 'zstandard>=0.20.0,<0.21.0']

extras_require = \
{'linux': ['netfilterqueue>=1.1.0,<2.0.0'], 'windows': ['wmi>=1.5.1,<2.0.0']}

setup_kwargs = {
    'name': 'pyhtools',
    'version': '2.1.0',
    'description': 'Python Hacking Tools (PyHTools) (pht) is a collection of python written hacking tools consisting of network scanner, arp spoofer and detector, dns spoofer, code injector, packet sniffer, network jammer, email sender, downloader, wireless password harvester credential harvester, keylogger, download&execute, and reverse_backdoor along with website login bruteforce, scraper, web spider etc. PHT also includes malwares which are undetectable by the antiviruses.',
    'long_description': "# PyHTools\n\n![PyHTools Logo](https://i.ibb.co/CtwVV5T/Py-HTools-without-bg-cropped.png)\n\n- Python Hacking Tools (PyHTools) (pht) is a collection of python written hacking tools consisting of network scanner, arp spoofer and detector, dns spoofer, code injector, packet sniffer, network jammer, email sender, downloader, wireless password harvester credential harvester, keylogger, download&execute, and reverse_backdoor along with website login bruteforce, scraper, web spider etc. PHT also includes malwares which are undetectable by the antiviruses.\n\n- These tools are written in python3, refer installation to install/download tools and its dependencies.\n\n- PyHTools comes with UI, but you can also use command line to use tools individually.\n\n**`NOTE` : The UI hasn't been updated yet with new tools, Refer examples for more information**\n\n\n## Disclaimer\n\nThe disclaimer advises users to use the open source project for ethical and legitimate purposes only and refrain from using it for any malicious activities. The creators and contributors of the project are not responsible for any illegal activities or damages that may arise from the misuse of the project. Users are solely responsible for their use of the project and should exercise caution and diligence when using it. Any unauthorized or malicious use of the project may result in legal action and other consequences.\n\n[Read More](./DISCLAIMER.md)\n\n\n## Join Our Discord Community\n\n[![Join our Discord server!](https://invidget.switchblade.xyz/DJrnAg4nv2)](http://discord.gg/DJrnAg4nv2)\n\n## How To Videos\n\n- Gain access to remote shell over the Internet using HTTP Backdoor\n\n  [![YT Thumbnail](https://img.youtube.com/vi/Wg-PiywAqyw/maxresdefault.jpg)](https://youtu.be/Wg-PiywAqyw)\n\n## Installation\n\n### Using pip\n\n- Install main branch using pip\n\n  ```bash\n  python3 -m pip install git+https://github.com/dmdhrumilmistry/pyhtools.git\n  ```\n\n- Install Release from PyPi\n\n  ```bash\n  # without options\n  python3 -m pip install pyhtools\n\n  # for windows\n  python3 -m pip install pyhtools[windows]\n\n  # for linux\n  python3 -m pip install pyhtools[linux]\n  ```\n\n### Manual Method\n\n- Open terminal\n\n- Install git package\n\n  ```bash\n  sudo apt install git python3 -y\n  ```\n\n- Install [Poetry](https://python-poetry.org/docs/master#installing-with-the-official-installer)\n\n- clone the repository to your machine\n\n  ```bash\n  git clone https://github.com/dmdhrumilmistry/pyhtools.git\n  ```\n\n- Change directory\n\n  ```bash\n  cd pyhtools\n  ```\n\n- install with poetry\n\n  ```bash\n  # without options\n  poetry install\n\n  # for windows\n  poetry install -E windows\n\n  # for linux\n  poetry install -E linux\n  ```\n\n## Start PyHTools\n\n- run pyhtools.py\n\n  ```bash\n  python3 -m pyhtools\n  ```\n\n- to get all the commands use `help`\n\n  ```bash\n  pyhtools >> help\n  ```\n\n> There may be chances that pyfiglet or kamene will not be installed through requirements.txt, you can install manually using `pip3 install pyfiglet kamene`.  \n> If you're using Termux or windows, then use `pip` instead of `pip3`.  \n> Few features are only for linux os, hence they might not work on windows and require admin priviliges.\n\n### Open In Google Cloud Shell\n\n- Temporary Session  \n  [![Open in Cloud Shell](https://gstatic.com/cloudssh/images/open-btn.svg)](https://shell.cloud.google.com/cloudshell/editor?cloudshell_git_repo=https%3A%2F%2Fgithub.com%2Fdmdhrumilmistry%2Fpyhtools&ephemeral=true&show=terminal&cloudshell_print=./DISCLAIMER.md)\n- Perisitent Session  \n  [![Open in Cloud Shell](https://gstatic.com/cloudssh/images/open-btn.svg)](https://shell.cloud.google.com/cloudshell/editor?cloudshell_git_repo=https%3A%2F%2Fgithub.com%2Fdmdhrumilmistry%2Fpyhtools&ephemeral=false&show=terminal&cloudshell_print=./DISCLAIMER.md)\n\n## Package Tools and Features\n\n### Attackers\n\n- `For Networks`\n\n  - Network Scanner\n  - Mac changer\n  - ARP Spoofing\n  - DNS spoofing\n  - Downloads Replacer\n  - Network Jammer\n  - Pkt Sniffer\n  - Code Injector\n\n- `For Websites`\n\n  - Login Guesser (Login Bruteforcer)\n  - Web Spider\n  - Web crawler (detects dirs | subdomains)\n  - Web Vulnerablity Scanner\n\n- `For Android`\n  - mitm\n    - Custom Certificate Pinner\n\n### Detectors\n\n- ARP Spoof Detector\n\n### Malwares/Trojans/Payloads/Ransomwares/Worms\n\n- Email Sender (reporter)\n- Downloader\n- Wireless Password Harvester\n- Credential Harvester\n- Keylogger (dlogs)\n- Reverse Backdoors\n  - TCP\n  - HTTP\n- Download and Execute\n- Telegram Data Harvester\n- DMSecRansomware\n- Telegram Remote Code Executor\n- DirCloner\n\n> **NOTE:** Do not upload/send/report malwares to anti virus services such as `VirusTotal`. This will make program detectable\n\n## Project Updates\n\n- [View](https://github.com/users/dmdhrumilmistry/projects/2/views/1)\n\n## How to Package a Evil Files\n\n- [Example Script](./examples/EvilFiles)\n- [View How to create a Trojan](./HowTo/Malwares/CreateTrojanPackage.md)\n- [Generator Script](./examples/EvilFiles/generatorScript.py)\n\n## Have any Ideas 💡 or issue\n\n- Create an issue\n- Fork the repo, update script and create a Pull Request\n\n## Contributing\n\nRefer [CONTRIBUTIONS.md](/.github/CONTRIBUTING.md) for contributing to the project.\n\n## LICENSE\n\nPyHTools is distributed under `MIT` License. Refer [License](/LICENSE) for more information.\n\n## Connect With Me\n\n|                                                                                                                       |                                                       Platforms                                                       |                                                                                                                                        |\n| :-------------------------------------------------------------------------------------------------------------------: | :-------------------------------------------------------------------------------------------------------------------: | :------------------------------------------------------------------------------------------------------------------------------------: |\n|       [![GitHub](https://img.shields.io/badge/Github-dmdhrumilmistry-333)](https://github.com/dmdhrumilmistry)        | [![LinkedIn](https://img.shields.io/badge/LinkedIn-Dhrumil%20Mistry-4078c0)](https://linkedin.com/in/dmdhrumilmistry) |             [![Twitter](https://img.shields.io/badge/Twitter-dmdhrumilmistry-4078c0)](https://twitter.com/dmdhrumilmistry)             |\n| [![Instagram](https://img.shields.io/badge/Instagram-dmdhrumilmistry-833ab4)](https://instagram.com/dmdhrumilmistry/) |     [![Blog](https://img.shields.io/badge/Blog-Dhrumil%20Mistry-bd2c00)](https://dmdhrumilmistry.github.io/blog)      | [![Youtube](https://img.shields.io/badge/YouTube-Dhrumil%20Mistry-critical)](https://www.youtube.com/channel/UChbjrRvbzgY3BIomUI55XDQ) |\n",
    'author': 'Dhrumil Mistry',
    'author_email': 'contact@dmdhrumilmistry.tech',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
