# Checks image: runs the test suite, the vault link checker and the bank lint.
#   docker compose run --rm checks
FROM python:3.9-slim

WORKDIR /app
COPY quiz/requirements.txt quiz/requirements.txt
RUN pip install --no-cache-dir -r quiz/requirements.txt

COPY quiz quiz
COPY tools tools
COPY vault vault
COPY checks/run.sh checks/run.sh

ENTRYPOINT ["bash", "checks/run.sh"]
