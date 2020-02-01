FROM python:3.6

RUN pip install requests slackclient

ADD src/ /

CMD ["python", "./coronabot.py"]
