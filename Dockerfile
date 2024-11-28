FROM python:3.11-slim

WORKDIR /app

COPY . /app/

RUN pip install argparse 

EXPOSE 80 443 

CMD ["python", "utils.py"]
