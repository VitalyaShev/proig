FROM python:latest

ADD . /app
WORKDIR /build


RUN ls
RUN pip install -r ../app/requirements.txt && \
    pip install pybuilder
RUN ls ../app
# USER sample
#RUN pyb --start-project
WORKDIR /app
RUN    pyb -v
CMD [ "python", "./src/main/python/main.py" ]
