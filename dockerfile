FROM python:3.10

COPY ./requirements.txt /app/requirements.txt

WORKDIR /OneButtonWebpage/app

RUN pip3 install -r requirements.txt

COPY app /app/

EXPOSE 8000

ENTRYPOINT [ "uvicorn" ]

CMD [ "--host", "0.0.0.0", "main:app" ]
