FROM python:3.9

WORKDIR /app

# Installa le dipendenze
COPY Pipfile Pipfile.lock /app/
RUN pip install pipenv && pipenv install --system --deploy

# Copia il codice dell'applicazione
COPY . /app/

# Raccogli file statici
RUN python manage.py collectstatic --noinput

# Esponi la porta 8000
EXPOSE 8000

# Esegui le migrazioni e avvia il server
CMD python manage.py migrate && gunicorn backendzero.wsgi:application --bind 0.0.0.0:8000