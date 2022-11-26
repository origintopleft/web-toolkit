FROM python:3.11-alpine

# installing app
COPY app /app
WORKDIR /app

RUN pip install -r requirements.txt

CMD [ "python", "-m", "flask", "--app", "/app/web-toolkit.py", "run", "-h", "0.0.0.0", "-p", "1337" ]
EXPOSE 1337