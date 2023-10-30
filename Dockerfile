FROM python:3.10.6
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
#RUN python manage.py makemigrations --no-input

CMD python manage.py makemigrations
CMD python manage.py migrate
COPY . /app
