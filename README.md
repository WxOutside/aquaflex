# Aquaflex

This is standalone code for the Aquaflex sensor. For an example of how it can integrate with CouchDB or other recording options, please see the software WxOutside repository.

Requirements
============
This will work on a Raspberry Pi A+, 2 or 3 and is coupled with a USB SDI-12 adaptor, such as this one: https://liudr.wordpress.com/gadget/sdi-12-usb-adapter/

This code is designed to work on either Python 2.x or Python 3.x

Setup
=====
There is a config.py with settings for the sensor version and SDI standard. By default, the sensor version is 130 and the SDI standard is 1.3.
You shouldn't have to change these, but you can if your sensor requires it.

Usage
========
You can change the address and soil type, and make measurement requests.

Make measurement request:

```bash
~/aquaflex.py
```

Change address:
```bash
~/aquaflex.py --address [aA-zZ]
```

Change soil type:
```bash
~/aquaflex.py --soil [clay|sand]
```

When the address or soil type is changed, a confirmation will be presented and the script will exit.

A few sanity checks are run before each reading:
- If the sensor does not return an acknowledgement on the address it reports on, then the script exits.
- If the sensor version is not the same as what is in the config file, then the script exits.
- If the sensor returns an error message, then the script will not proceed with a measurement.

Limitations
===========
Because this is standalone code, all it does it output the various measurements directly onto the screen. This code can easily be customised to redirect output to email, a database or a file, it's up to you.

