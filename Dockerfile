FROM python:3.10

WORKDIR /
COPY ./requirements.txt /requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

EXPOSE 8006

CMD [ "python", "./arrancar.py", "--host", "0.0.0.0", "--port", "8006", "--reload", "False" ]
