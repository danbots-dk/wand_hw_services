# Specification of battery service

## OS requirements

Raspberry PI Os lite:  2023-05-03-raspios-bullseye-armhf-lite

## Installation and uninstallation of service

How to install AND uninstall the services

...


## Service description

The service collect infromation from hw and provide the users whith the following information

- Main power connected (ON/OFF)
- Battery voltage
- Battery charge percent
- Estimate time for full recharge
- Estimatted time for discharge

## Configuration of service

The service is configurable with:

- Battery capacity
- Other battery specsparameters
- Wand estimated power consumption
- Wand estimated usage percent

The service is expected to be used with different hw (battery and electronics), but having a standard interface for user applications

## User interface

Description of how the user get the information from service

...

