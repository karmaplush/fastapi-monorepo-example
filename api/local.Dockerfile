FROM python:3.11-slim

WORKDIR /workdir

COPY ./requirements.txt /workdir/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /workdir/requirements.txt

COPY ./app /workdir/app

CMD ["uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]
