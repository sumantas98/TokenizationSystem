FROM python:3.8-slim
RUN mkdir /app
ADD . /app
WORKDIR /app
RUN pip install --upgrade pip \
  && pip install -r requirement.txt 
CMD ["python", "Tokenization.py"]