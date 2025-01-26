# FROM docker.io/python:3.9-slim
FROM docker.io/python:3.9-slim
LABEL mainatainer="CPA <cpa@uem.br>"
LABEL br.uem.cpa.sistema.backend.author="Arthur Ueda"
# LABEL br.uem.cpa.sistema.backend.version="v010"
WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

ENTRYPOINT ["python","-u", "app.py"]
