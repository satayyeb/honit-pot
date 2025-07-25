FROM alpine

WORKDIR /app

COPY pot /app/pot

RUN chmod +x /app/pot

ENTRYPOINT ["/app/pot"]
