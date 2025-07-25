FROM alpine

WORKDIR /app

COPY pot /app/pot

ENTRYPOINT ["/app/pot/pot"]
