FROM python:3.9-slim-buster
COPY . .
WORKDIR /app
RUN python3 -m pip install -r ../requirements.txt
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]
