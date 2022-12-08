FROM python:3.8-slim

WORKDIR /usr/src/app
ENV TZ 'Europe/Moscow'
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
ENV PYTHONPATH "${PYTHONPATH}:/usr/src/app/"

COPY ./ ./

CMD ["python", "src/bot/bot.py"]

