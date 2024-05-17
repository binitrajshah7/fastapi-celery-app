FROM logitrack-base
WORKDIR /code
COPY app.py /code/app.py
COPY .env /code/.env
COPY lib /code/lib
COPY requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8888
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8888"]