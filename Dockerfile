FROM alpine

WORKDIR /app

COPY bin/pot /app/pot

RUN chmod +x /app/pot

ENTRYPOINT ["/app/pot"]
