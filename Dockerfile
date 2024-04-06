FROM python:3.12.2-alpine3.18
WORKDIR /code
COPY requirements.txt /code
RUN pip install -r requirements.txt --no-cache-dir
COPY . /code
CMD python app.py
EXPOSE 5000