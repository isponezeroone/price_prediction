FROM python:3.7

RUN python -m pip install flask flask-cors gunicorn numpy scikit-learn pillow requests pandas beautifulsoup4 fastapi uvicorn[standart]


WORKDIR /app_fast


COPY ./app_fast /app_fast
#ADD columns_name.json columns_name.json
#ADD templates templates
#ADD parser.py parser.py
#ADD model.py model.py
#ADD preproccessing.py preproccessing.py
#ADD app.py app.py
#ADD model.pickle model.pickle
#ADD scaler.pickle scaler.pickle

EXPOSE 7000:7000

CMD [ "uvicorn",  "app_fast:app", "--host", "0.0.0.0", "--port", "7000"]
