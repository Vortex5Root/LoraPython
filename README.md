LoRa Driver Documentation
Introduction

This is the documentation of the LoRa_E5() class which is a driver for the LoRa module using the Ebyte E22 chip. This module is based on the SX1262 chip and can be used to send data over long-range with low power consumption. The LoRa_E5() class allows interaction with the module using the Serial communication protocol.
Usage
Example usage

python

from lora_driver import LoRa_E5

# initialize the driver
driver = LoRa_E5()

# select the serial port
driver.select()

# connect to the selected port
driver.connect()

# get the version of the module
version = driver.version()

print(version)

Class
LoRa_E5()

The main class of the driver that provides an interface to interact with the LoRa module. The class has the following methods and properties:
Properties

    all_serials: a list of all available serial ports
    tag: a string representing the prefix to all AT commands to the module
    errors: a dictionary with error codes and their corresponding error message
    out_put: a list containing the outputs from the module
    get: a boolean flag indicating if the module is ready to receive commands

Methods

    __init__(): Constructor method that initializes the class with the properties.
    select(): Method to select the serial port to use. It prompts the user to select the port to use from the available serial ports.
    connect(): Method to connect to the selected serial port.
    get_return(): Method to get the output from the module. It returns either the output or the error message in case an error occurred.
    get_out(): Method to get the output from the module.
    get_error(): Method to get the error message from the error code.
    teste(): Method to test the connection with the module.
    version(): Method to get the version of the module.
    identifier(id_type="",set_to=""): Method to get or set the identifier of the module. It takes two optional arguments, id_type and set_to. If id_type is not provided, it returns a list containing the DevAddr, DevEui and AppEui of the module. If id_type is provided and set_to is not provided, it returns the current value of the identifier of the provided type. If both id_type and set_to are provided, it sets the value of the identifier of the provided type to the provided value.
    send_msg(message): Method to send a message to the module using the MSG command. It takes one argument, message, which is the message to send.
    send_cmsg(message): Method to send a message to the module using the CMSG command. It takes one argument, message, which is the message to send.
    send_pmsg(message): Method to send a message to the module using the PMSG command. It takes one argument, message, which is the message to send.
    send_pmsghex(message): Method to send a message to the module using the PMSGHEX command. It takes one argument, message, which is the message to send.
    set_conn(port): Method to set the connection parameters of the module. It takes one argument, port, which is the port to use for the connection.

Parameters

    port: The serial port to use for the connection. This should be a string representing the name of the
