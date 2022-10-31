FROM python:2.7-alpine as builder

RUN apk add --no-cache build-base postgresql-dev

COPY requirements*.txt /

RUN --mount=type=cache,target=/wheels \
    pip wheel -r /requirements_docker.txt --wheel-dir=/wheels

FROM python:2.7-alpine

RUN apk add --no-cache postgresql-libs

WORKDIR /app

# copy from builder to force buildkit to build previous stage
COPY --from=builder /requirements*.txt /app/

RUN --mount=type=cache,target=/wheels \
    pip install --find-links=/wheels -r /app/requirements_docker.txt \
 && rm -fr /root/.cache/pip/

COPY . .

CMD gunicorn -k gevent \
    --access-logfile - \
    --access-logformat '%(h)s %({X-Forwarded-For}i)s %(l)s %(u)s %(t)s \"%(r)s\" %(s)s %(b)s \"%(f)s\" \"%(a)s' \
    --capture-output \
    -b 0.0.0.0:8080 \
    wsgi:application
