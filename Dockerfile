FROM python:3.9.17
WORKDIR /app
COPY pyproject.toml .
RUN pip install -e .
COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
#CMD ["python3", "./main.py"]
