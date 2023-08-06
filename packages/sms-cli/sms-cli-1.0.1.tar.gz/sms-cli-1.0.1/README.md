# SMS-cli
> Command line tool for sending commands via serial port to GSM shield module.

## Description
Command line tool for sending AT (ATtention) commands via serial port to 
[GSM Shield module](https://www.arduino.cc/en/Guide/ArduinoGSMShield). This tool is written in `python3` and it is 
supported on any platform (Windows/Linux/MacOS). Before using tool you must have 
[GSM Shield module](https://www.arduino.cc/en/Guide/ArduinoGSMShield) connected to serial port and it must have 
proper SIM card inserted with enough credits to send SMS messages.

## Installation
Tool can be installed using `pip3` command:

```sh
pip3 install sms-cli
```

Or you can install it directly form this project source:

```sh
python3 build.py

pip3 install dist/sms-cli-{version}.tar.gz
```

After installation, tool will be added to system path and can be used to send messages and read inbox.

## Usage
### All commands
```sh
usage: sms-cli [-h] [-v] [-b BAUD] [-p PORT] {send,read,delete,check} ...

execute AT commands on GSM shield module via serial port

positional arguments:
  {send,read,delete,check}
    send                send SMS message to destination
    read                read all inbound SMS messages from inbox, or just one
                        using index
    delete              delete specific message from storage
    check               check connectivity with GSM shield module

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         print version number
  -b BAUD, --baud BAUD  specify baud rate
  -p PORT, --port PORT  specify port device type
```

### Check
```sh
usage: sms-cli check [-h] [-n NUMBER]

optional arguments:
  -h, --help            show this help message and exit
  -n NUMBER, --number NUMBER
                        number of iterations to check connection
```

### Send
```sh
usage: sms-cli send [-h] -d DESTINATION -m MESSAGE

optional arguments:
  -h, --help            show this help message and exit
  -d DESTINATION, --destination DESTINATION
                        destination MSISDN in full format (e.g. +38591234567)
  -m MESSAGE, --message MESSAGE
                        SMS message text with maximum of 160 characters (e.g.
                        "Some message text.")
```

### Read
```sh
usage: sms-cli read [-h] [-i INDEX] [-s STORAGE] [-u] [-d] [-f]

optional arguments:
  -h, --help            show this help message and exit
  -i INDEX, --index INDEX
                        read only message at this index from the top of inbox
  -s STORAGE, --storage STORAGE
                        specify the storage from which to read messages,
                        options: [SM | ME | MT | BM | SR]
  -u, --unread          read only currently unread messages (when not using
                        index)
  -d, --dry             dry read, not changing status of unread messages while
                        reading
  -f, --full            show full header information of red SMS messages
```

### Delete
```sh
usage: sms-cli delete [-h] -i INDEX [-s STORAGE]

optional arguments:
  -h, --help            show this help message and exit
  -i INDEX, --index INDEX
                        index of SMS message to delete
  -s STORAGE, --storage STORAGE
                        specify the storage from which to delete message,
                        options: [SM | ME | MT | BM | SR]
```

LICENSE
---
GNU General Public License