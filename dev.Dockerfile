FROM python:3.10

WORKDIR /app/

COPY ./dist ./dist

COPY .env .

COPY requirements.txt .

RUN pip install ./dist/cv_parsing-0.0.1.tar.gz

COPY . .

ENTRYPOINT [ "streamlit", "run", "app.py", "--server.port", "7860"]