FROM python:3.11-alpine

RUN apk add cargo
RUN cargo install rant --version 4.0.0-alpha.33 --root / --features cli

# prereqs
COPY app/requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

# installing app
COPY app /app
WORKDIR /app

RUN mkdir -p /lib/wordlist
COPY ext/imsky/worklists /lib/wordlist

COPY lib/rantify_wordlists.py /lib/rantify_wordlists.py
RUN python /lib/rantify_wordlists.py

CMD [ "python", "web-toolkit.py" ]
EXPOSE 1337