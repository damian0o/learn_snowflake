# Quiz runner image: Python plus the question bank, nothing else.
#   docker compose run --rm quiz day1
# or:
#   docker build -t learn-snowflake-quiz . && docker run --rm -it -v "$PWD/quiz/results:/app/quiz/results" learn-snowflake-quiz day1
# Content and code checks (lint, link checker, tests) live in checks/, not here.
FROM python:3.9-slim

WORKDIR /app
COPY quiz/requirements.txt quiz/requirements.txt
RUN pip install --no-cache-dir -r quiz/requirements.txt

COPY quiz/quiz.py quiz/quiz.py
COPY quiz/quizlib quiz/quizlib
COPY quiz/bank quiz/bank

# Progress lives here; mount it to keep scores between runs.
VOLUME ["/app/quiz/results"]

ENTRYPOINT ["python3", "quiz/quiz.py"]
CMD ["day1"]
