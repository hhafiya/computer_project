FROM python:3.9-alpine

ADD . .

RUN pip install networkx pyvis

EXPOSE 8000

CMD ["python", "main.py"]