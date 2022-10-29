FROM python:2.7-alpine as builder

RUN apk add --no-cache build-base postgresql-dev

COPY requirements.txt /

RUN --mount=type=cache,target=/wheels \
    pip wheel -r /requirements.txt --wheel-dir=/wheels

FROM python:2.7-alpine

RUN apk add --no-cache postgresql-libs

WORKDIR /app

# copy from builder to force buildkit to build previous stage
COPY --from=builder /requirements.txt /app/

RUN --mount=type=cache,target=/wheels \
    pip install --find-links=/wheels -r /app/requirements.txt \
 && rm -fr /root/.cache/pip/

COPY . .

ENTRYPOINT ["python", "-u", "/app/priberambot.py"]
