FROM python:3.10

COPY ./requirements.txt /OneButtonWebpage/app/requirements.txt

WORKDIR /OneButtonWebpage/app

RUN pip3 install -r requirements.txt

COPY app /OneButtonWebpage/app/

EXPOSE 8000

ENTRYPOINT [ "uvicorn" ]

CMD [ "--host", "0.0.0.0", "main:app" ]
