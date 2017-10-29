FROM python:3.6.3

WORKDIR /collector
COPY *.py requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "./run.py"]