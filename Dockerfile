FROM python:3.9

RUN pip install pipenv

# Install dependencies
RUN pipenv install

# Start server
CMD ["pipenv", "run", "python3", "main.py"]
