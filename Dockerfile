FROM python:3.9-alpine

ADD . .

RUN pip install networkx pyvis

CMD ["python", "main.py"]