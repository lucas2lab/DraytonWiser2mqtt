FROM python:3-alpine

WORKDIR /code

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./src ./src

CMD [ "python", "src/mqtt.py" ]