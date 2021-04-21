FROM python:3.8
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip install wheel
RUN pip install -r requirements.txt
ADD . /code/
COPY . .
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app.wsgi"]