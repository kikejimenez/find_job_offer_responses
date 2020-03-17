FROM jupyter/minimal-notebook

COPY ./requirements.txt requirements.txt

RUN pip install --upgrade jupyterlab

RUN pip install -r requirements.txt

#RUN python -m pip install jupytext --upgrade --user

RUN jupyter lab build

RUN jupyter serverextension enable jupytext