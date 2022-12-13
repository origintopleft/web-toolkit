FROM python:3.11-alpine

# prereqs
COPY app/requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

# installing app
COPY app /app
WORKDIR /app

RUN mkdir -p /lib/wordlist
COPY ext/imsky/worklists /lib/wordlist

CMD [ "python", "web-toolkit.py" ]
EXPOSE 1337