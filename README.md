# SOFTWARE_VI_BACKUP

## Clonar repositorio con github-cli (si es posible)

Pasos para arrancar entorno de desarrollo en linux

```
gh repo clone jtvans/SOFTWARE_VI_BACKUP

cd SOFTWARE_VI_BACKUP

python -m venv env

source env/bin/activate

pip install -r requirements.txt

copy .env_sample .env

# rellena las variables de entorno del .env

python manage.py runserver

```
