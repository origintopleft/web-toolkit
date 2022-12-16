FROM python:3.11-alpine

# install rust environment (for rant)
ENV RUSTUP_HOME=/usr/local/rustup CARGO_HOME=/usr/local/cargo PATH=/usr/local/cargo/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin RUST_VERSION=1.61.0
RUN apk add --no-cache rustup gcc musl-dev
RUN rustup-init -y

# install rant
RUN cargo install --color=never rant --version 4.0.0-alpha.33 --root / --features cli

# prereqs
COPY app/requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

# installing app
COPY app /app
WORKDIR /app

RUN mkdir -p /lib/wordlist
COPY ext/imsky/wordlists /lib/wordlist

COPY lib/rantify_wordlists.py /lib/rantify_wordlists.py
RUN python /lib/rantify_wordlists.py

CMD [ "python", "web-toolkit.py" ]
EXPOSE 1337