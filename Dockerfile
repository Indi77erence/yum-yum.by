FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /yum-yum
WORKDIR /yum-yum
COPY requirements.txt /yum-yum/
RUN pip install --upgrade pip && pip install -r requirements.txt
ADD . /yum-yum/