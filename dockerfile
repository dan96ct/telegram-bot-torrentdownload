FROM python:3
WORKDIR /user/src/app
COPY ./app /user/src/app
RUN pip install python-telegram-bot -U --pre
RUN pip install python-qbittorrent
CMD [ "python", "./main.py" ]