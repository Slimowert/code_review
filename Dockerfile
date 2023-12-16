# FROM python:3.10.12

# RUN mkdir app
# COPY . /app
# RUN ls -l

# RUN pip install --upgrade pip

# # RUN pip install --user --no-cache-dir -r app/requirements.txt
# RUN pip install requests bs4 lxml sqlalchemy flask tqdm undetected_chromedriver Flask-SQLAlchemy


FROM python:latest


USER root
RUN apt-get update
RUN pip install --upgrade pip

RUN mkdir parser
COPY /app/. /parser

WORKDIR /parser

RUN pip install requests bs4 lxml sqlalchemy flask tqdm undetected_chromedriver Flask-SQLAlchemy docker

RUN wget --no-verbose -O /tmp/chrome.deb https://dl.google.com/linux/chrome/deb/pool/main/g/google-chrome-stable/google-chrome-stable_114.0.5735.198-1_amd64.deb \
  &&  apt install -y /tmp/chrome.deb \
  && rm /tmp/chrome.deb

# RUN pip3 install --force-reinstall 'requests<2.29.0' 'urllib3<2.0'