#!/usr/bin/env python

#import serial.tools.list_ports
import serial
import sys
import time

def get_device():
    device=serial.Serial("/dev/ttyUSB0",baudrate=9600,timeout=10)
    
    time.sleep(2.5) # delay for arduino bootloader and the 1 second delay of the adapter.
    
    return device

# Get the address of the provided device
def device_address(device):
    device.write(b'?!')
    if sys.version_info[0] < 3:
        response=bytes(device.readline().decode('utf-8'))[:-2]
    else:
        response=bytes(device.readline().decode('utf-8'), encoding='utf-8')[:-2]
    
    
    return response
    
# Change the address of the provided device
# NOTE: if successful, this will return the new address.
def change_device_address(device, address, new_address):
    device.write(address+b'A' + new_address + b'!')
    response=device.readline()[:-2]
    
    return response
    
# Get an acknowledgement that this is an active device
def device_acknowledgement(device, address):
    device.write(address+b'!')
    if sys.version_info[0] < 3:
        response=bytes(device.readline().decode('utf-8'))[:-2]
    else:
        response=bytes(device.readline().decode('utf-8'), encoding='utf-8')[:-2]
    
    
    return response

# Get the identification value for this device.
# returns allccccccccmmmmmmvvvxxx
# a - the sensor address
# ll - the SDI-12 version number, indicating SDI-12 version compatibility; for example, version 1.3 is encoded as 13
# cccccccc - an 8 character vendor identification, usually a company name or its abbreviation
# mmmmmm - 6 characters specifying the sensor model number
# vvv - 3 characters specifying the sensor version
# xxx . . . xx - an optional field, up to 13 characters, used for a serial number or other specific sensor information that is not relevant for operation of the data recorder
def device_identification(device, address):
    
    device.write(address+b'I!')
    response=device.readline().decode('utf-8')
    
    #id_address=response[0:1]
    sdi_version=int(response[1:3])
    vendor=response[3:11]
    model=response[11:17]
    version=int(response[17:20])
    
    return sdi_version, vendor, model, version
 
# Send a request to take a measurement.
# We will return the number of seconds we need to wait for, and how many data items to expect
def measurement_request(device, address):
    
    device.write(address+b'M!')
    response=device.readline()
    address=response[0:1]
    delay=float(response[1:4])
    num_data=int(response[4:5])
    
    return delay, num_data
   
# Get the data from the measurement request
# a is the sensor address.
# mm.mm is the volumetric soil moisture in %
# tt.t is the soil temperature in 0C
# bb.b is the battery voltage
# cc.cc and ll.ll are the raw readings from the soil moisture measurement
def get_data(device, address):
    device.write(address+b'D0!')
    response=device.readline().decode('utf-8').split('+')
    #address=response[0]
    soil_moisture=response[1]
    soil_temperature=response[2]
    battery_voltage=response[3]
    raw1=float(response[4])
    raw2=float(response[5])
    
    return soil_moisture, soil_temperature, battery_voltage, raw1, raw2
 
# Returns the current soil type. The soil type is used to engage the correct calibration equation in the sensor
# Will return asand or aclay
def query_soil_type(device, address):
    device.write(address + b'XS!')
    response=device.readline().decode('utf-8')[1:-2]
    
    return response

# Sets the current soil type. The soil type is used to engage the correct calibration equation in the sensor
# soil_type = 'sand' or 'clay'
def change_soil_type(device, address, soil_type):
    if sys.version_info[0] < 3:
        soil_type=bytes(soil_type)
    else:
        soil_type=bytes(soil_type, encoding="utf-8")
    device.write(address + b'XS=' + soil_type + b'!')
    response=device.readline().decode('utf-8')[1:-2]
    
    return response

