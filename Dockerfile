FROM python:3.12-alpine
RUN apt update && apt install -y build-essential && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY requirements.txt .
RUN pip install --trusted-host pypi.python.org -r requirements.txt
COPY . .
ENTRYPOINT ["python", "app.py"]