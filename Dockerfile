FROM python:3.12.4-slim

WORKDIR /app

COPY . .

RUN pip3 install --no-cache-dir -r requirements.txt

CMD ["python", "-m", "fazdb"]
