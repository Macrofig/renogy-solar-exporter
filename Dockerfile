FROM python:3.9

RUN pip install pipenv

# Install Renogy Bluetooth library
RUN git clone git@github.com:macrofig/renogy-bt.git
ADD renogy-bt/renogybt renogybt

# Install dependencies
RUN pipenv install

# Start server
CMD ["pipenv", "run", "python3", "./solar-cli.py"]
