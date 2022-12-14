FROM tensorflow/tensorflow:2.9.1

COPY WindFlow /WindFlow
COPY requirements.txt /requirements.txt
COPY new_model.h5 /new_model.h5

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD uvicorn WindFlow.api.fast:app --host 0.0.0.0 --port $PORT
