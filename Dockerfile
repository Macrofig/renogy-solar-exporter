FROM python:3.9-bookworm

# TODO This is needed but not sure what we need from it
RUN apt update && apt install -y build-essential

# Installs dbus and GObject for gatt
RUN apt install -y libdbus-glib-1-dev libgirepository1.0-dev python3-gi python3-gi-cairo gir1.2-gtk-4.0

ADD ./src /solar-exporter/
COPY ./entrypoint.sh /solar-exporter/

# Install dependencies
RUN ["pip", "install", "-r", "solar-exporter/requirements.txt"]

# Start server
CMD ./solar-exporter/entrypoint.sh
