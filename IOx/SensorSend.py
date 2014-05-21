#!/usr/bin/env python

""" 
May 2014 - SensorReader 
"""

"""Copyright 2010 Phidgets Inc.
This work is licensed under the Creative Commons Attribution 2.5 Canada License. 
To view a copy of this license, visit http://creativecommons.org/licenses/by/2.5/ca/

Heavily modified by me.
"""

__author__ = 'Brett Kugler'
__version__ = '2.1.8'
__date__ = 'May 20 2010'


#Basic imports
from ctypes import *
import sys
import random
from time import sleep
#Phidget specific imports
from Phidgets.PhidgetException import PhidgetErrorCodes, PhidgetException
from Phidgets.Events.Events import AttachEventArgs, DetachEventArgs, ErrorEventArgs, InputChangeEventArgs, OutputChangeEventArgs, SensorChangeEventArgs
from Phidgets.Devices.InterfaceKit import InterfaceKit
from Phidgets.Phidget import PhidgetID
from Phidgets.Devices.TextLCD import TextLCD, TextLCD_ScreenSize

import requests

#Create an interfacekit object
try:
    interfaceKit = InterfaceKit()
except RuntimeError as e:
    print("InterfaceKit: Runtime Exception: %s" % e.details)
    print("Exiting....")
    exit(1)

#Create an TextLCD object
try:
    textLCD = TextLCD()
except RuntimeError as e:
    print("LCD: Runtime Exception: %s" % e.details)
    try:
        interfaceKit.closePhidget()
    except PhidgetException as e:
        print("InterfaceKit Close: Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)

print 'Setting sensors to 0'
sensor_port0 = 0
sensor_port1 = 0

#Information Display Function
def DisplayInterfaceKitDeviceInfo():
    print("|------------|----------------------------------|--------------|------------|")
    print("|- Attached -|-              Type              -|- Serial No. -|-  Version -|")
    print("|------------|----------------------------------|--------------|------------|")
    print("|- %8s -|- %30s -|- %10d -|- %8d -|" % (interfaceKit.isAttached(), interfaceKit.getDeviceName(), interfaceKit.getSerialNum(), interfaceKit.getDeviceVersion()))
    print("|------------|----------------------------------|--------------|------------|")
    print("Number of Digital Inputs: %i" % (interfaceKit.getInputCount()))
    print("Number of Digital Outputs: %i" % (interfaceKit.getOutputCount()))
    print("Number of Sensor Inputs: %i" % (interfaceKit.getSensorCount()))

#Event Handler Callback Functions
def interfaceKitAttached(e):
    attached = e.device
    print("InterfaceKit %i Attached!" % (attached.getSerialNum()))

def interfaceKitDetached(e):
    detached = e.device
    print("InterfaceKit %i Detached!" % (detached.getSerialNum()))

def interfaceKitError(e):
    try:
        source = e.device
        print("InterfaceKit %i: Phidget Error %i: %s" % (source.getSerialNum(), e.eCode, e.description))
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))

def interfaceKitInputChanged(e):
    source = e.device
    print("InterfaceKit %i: Input %i: %s" % (source.getSerialNum(), e.index, e.state))

def interfaceKitSensorChanged(e):
    global sensor_port0
    global sensor_port1
    #source = e.device
    #print e.device.getSensorValue(0)
    #print("InterfaceKit %i: Sensor %i: %i" % (source.getSerialNum(), e.index, e.value))
    if (e.index == 0):
        #sensor_port0 = e.value
        sensor_port0 = e.device.getSensorValue(0) #/ 4.095
        #print "SP0", sensor_port0
    elif (e.index == 1):
        sensor_port1 = e.value

def interfaceKitOutputChanged(e):
    source = e.device
    print("InterfaceKit %i: Output %i: %s" % (source.getSerialNum(), e.index, e.state))

#Information Display Function
def DisplayLCDDeviceInfo():
    try:
        isAttached = textLCD.isAttached()
        name = textLCD.getDeviceName()
        serialNo = textLCD.getSerialNum()
        version = textLCD.getDeviceVersion()
        rowCount = textLCD.getRowCount()
        columnCount = textLCD.getColumnCount()
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        return 1
    print("|------------|----------------------------------|--------------|------------|")
    print("|- Attached -|-              Type              -|- Serial No. -|-  Version -|")
    print("|------------|----------------------------------|--------------|------------|")
    print("|- %8s -|- %30s -|- %10d -|- %8d -|" % (isAttached, name, serialNo, version))
    print("|------------|----------------------------------|--------------|------------|")
    print("Number of Rows: %i -- Number of Columns: %i" % (rowCount, columnCount))

#Event Handler Callback Functions
def TextLCDAttached(e):
    attached = e.device
    print("TextLCD %i Attached!" % (attached.getSerialNum()))

def TextLCDDetached(e):
    detached = e.device
    print("TextLCD %i Detached!" % (detached.getSerialNum()))

def TextLCDError(e):
    try:
        source = e.device
        print("TextLCD %i: Phidget Error %i: %s" % (source.getSerialNum(), e.eCode, e.description))
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))

#Main Program Code
try:
    interfaceKit.setOnAttachHandler(interfaceKitAttached)
    interfaceKit.setOnDetachHandler(interfaceKitDetached)
#    interfaceKit.setOnErrorhandler(interfaceKitError)
    interfaceKit.setOnInputChangeHandler(interfaceKitInputChanged)
    interfaceKit.setOnOutputChangeHandler(interfaceKitOutputChanged)
    interfaceKit.setOnSensorChangeHandler(interfaceKitSensorChanged)
except PhidgetException as e:
    print("InterfaceKit AttachHandler: Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)

print("Opening phidget interfaceKit object....")

try:
    interfaceKit.openPhidget()
except PhidgetException as e:
    print("InterfaceKit Open: Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)

print("Waiting for Interface Kit attach....")

try:
    interfaceKit.waitForAttach(10000)
except PhidgetException as e:
    print("InterfaceKit Attach: Phidget Exception %i: %s" % (e.code, e.details))
    try:
        interfaceKit.closePhidget()
    except PhidgetException as e:
        print("InterfaceKit Close: Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)
else:
    DisplayLCDDeviceInfo()

# Once InterfaceKit is attached, TextLCD should also be attached...
try:
    textLCD.setOnAttachHandler(TextLCDAttached)
    textLCD.setOnDetachHandler(TextLCDDetached)
    textLCD.setOnErrorhandler(TextLCDError)
except PhidgetException as e:
    print("LCD AttachHandler: Phidget Exception %i: %s" % (e.code, e.details))
    try:
        interfaceKit.closePhidget()
    except PhidgetException as e:
        print("InterfaceKit Close: Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)

print("Opening phidget TextLCD object....")

try:
    textLCD.openPhidget()
except PhidgetException as e:
    print("LCD Open: Phidget Exception %i: %s" % (e.code, e.details))
    try:
        interfaceKit.closePhidget()
    except PhidgetException as e:
        print("InterfaceKit Close: Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)

print("Waiting for LCD attach....")

try:
    textLCD.waitForAttach(10000)
except PhidgetException as e:
    print("LCD Attach: Phidget Exception %i: %s" % (e.code, e.details))
    try:
        interfaceKit.closePhidget()
    except PhidgetException as e:
        print("InterfaceKit Close: Phidget Exception %i: %s" % (e.code, e.details))
    try:
        textLCD.closePhidget()
    except PhidgetException as e:
        print("LCD Close: Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)
else:
    DisplayInterfaceKitDeviceInfo()


print("Setting the data rate for each sensor index to 128ms....")
for i in range(interfaceKit.getSensorCount()):
    try:
        interfaceKit.setDataRate(i, 128)
    except PhidgetException as e:
        print("InterfaceKit SetDataRate: Phidget Exception %i: %s" % (e.code, e.details))

while (1):
    try:
        if textLCD.getDeviceID()==PhidgetID.PHIDID_TEXTLCD_ADAPTER:
            textLCD.setScreenIndex(0)
            textLCD.setScreenSize(TextLCD_ScreenSize.PHIDGET_TEXTLCD_SCREEN_2x8)
            
        textLCD.setBacklight(True)
            
#         print("Writing to first row....")
#         textLCD.setDisplayString(0, "  Cisco Live 2014   ")
#        sleep(2)

#         print("Writing to second row....")
#         textLCD.setDisplayString(1, "   IOX Sample App   ")
#        sleep(2)

        headers={'Accept':'application/json'}
        data={'value':sensor_port0}
        r=requests.post("http://10.10.30.235:8080/rumble", data=data, headers=headers, verify=False)

        # if r.status_code == requests.codes.ok:
        #     print "success sending"
        # else:
        #     print "fail sending"

        textLCD.setDisplayString(0, "Quake reading:%6i" % sensor_port0)
        textLCD.setDisplayString(1, "")
#        sleep(2)
        
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        print("Exiting....")
        exit(1)


print("Closing...")

textLCD.setDisplayString(0, "")
textLCD.setDisplayString(1, "")

try:
    textLCD.closePhidget()
except PhidgetException as e:
    print("LCD Close: Phidget Exception %i: %s" % (e.code, e.details))

try:
    interfaceKit.closePhidget()
except PhidgetException as e:
    print("InterfaceKit Close: Phidget Exception %i: %s" % (e.code, e.details))

print("Done.")
exit(0)
