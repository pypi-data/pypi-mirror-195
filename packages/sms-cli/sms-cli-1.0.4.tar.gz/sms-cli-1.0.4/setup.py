from setuptools import setup
from setuptools import find_packages

desc = "Command-line interface for sending AT (ATtention) commands via serial port to GSM shield module."

verstrline = open('./cli/__init__.py', "rt").readline()
version = verstrline.split('=')[-1].strip().replace('\'', '')

setup(name="sms-cli",
      version=version,
      author="luka",
      author_email="lukamatosevic5@gmail.com",
      url="https://github.com/lmatosevic/sms-cli",
      download_url=f"https://github.com/lmatosevic/sms-cli/archive/refs/tags/{version}.tar.gz",
      packages=find_packages(),
      install_requires=["pyserial", "argparse"],
      python_requires=">=3.6",
      entry_points={
          "console_scripts": [
              "sms-cli = cli.main:main"
          ]
      },
      keywords=["sms", "cli", "messaging", "gsm"],
      description=desc)
