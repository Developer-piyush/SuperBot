FROM python:3
FROM gorialis/discord.py

RUN mkdir -p /usr/src/bot
WORKDIR /usr/src/bot

COPY . .

RUN python3 -m pip install discord.py
RUN python3 -m pip install -U py-cord --pre
RUN python3 -m pip install PycordUtils

CMD [ "python3", "bot.py" ]