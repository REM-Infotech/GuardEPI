FROM python:3

COPY . /GuardEPI
WORKDIR /GuardEPI

RUN pip install -r requirements.txt

CMD python main.py
