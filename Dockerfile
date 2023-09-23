FROM python:3.7-slim as base

# Install packages needed by renogy-bt
# TODO Check to make sure that renogy-bt needs these and not the example.py script
# sudo apt-get install python3-dbus
# pip3 install paho-mqtt gatt

RUN git clone git@github.com:cyrils/renogy-bt.git


RUN pip install pipenv

# Install dependencies

# Start server

