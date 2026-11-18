# Quiz runner in a container. Build once, run interactively:
#   docker compose run --rm quiz day1
# or without compose:
#   docker build -t learn-snowflake-quiz .
#   docker run --rm -it -v "$PWD/quiz/results:/app/quiz/results" learn-snowflake-quiz day1
FROM python:3.9-slim

WORKDIR /app
COPY quiz/requirements.txt quiz/requirements.txt
RUN pip install --no-cache-dir -r quiz/requirements.txt

COPY quiz quiz
COPY tools tools
COPY vault vault

# Progress lives here; mount it to keep scores between runs.
VOLUME ["/app/quiz/results"]

ENTRYPOINT ["python3", "quiz/quiz.py"]
CMD ["day1"]
