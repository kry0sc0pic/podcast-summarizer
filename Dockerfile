FROM python:3.11
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOST 8080
CMD ["streamlit", "run", "main.py","--server.port","8080","--server.address","0.0.0.0"]
