FROM python:3.9
LABEL maintainer "Team VaxoScope from 2020-2021 INFOMDSS course"

WORKDIR /code

COPY requirements.txt /
RUN pip install -r /requirements.txt
COPY ./ ./

CMD ["python", "./index.py"]