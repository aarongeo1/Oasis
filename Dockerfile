FROM python:3.8-slim-buster

WORKDIR /app

COPY data .
RUN pip3 install uvicorn[standard]
RUN pip3 install fastapi
EXPOSE 8000
#CMD ["cd", "data"]
CMD [ "python3", "-m" , "uvicorn", "app:app"]
