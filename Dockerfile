FROM python:3.9

WORKDIR /

LABEL version="0.1"

RUN pip install --upgrade pip \
&& pip install pipenv

COPY . .
RUN pipenv install --deploy

EXPOSE 5006/tcp
CMD ["pipenv", "run", "panel", "serve", "src/app.py"]