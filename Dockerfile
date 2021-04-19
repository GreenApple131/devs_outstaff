FROM python:3.8
RUN mkdir /code
WORKDIR /code
COPY requirements.txt .
RUN pip install wheel
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app.wsgi"]