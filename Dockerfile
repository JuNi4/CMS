FROM python:3

WORKDIR .

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN python server.py -gcf

COPY . .

CMD ["python", "./server.py"]
