FROM alpine

WORKDIR /app

COPY pot-exe .

RUN chmod +x /app/pot-exe

ENTRYPOINT ["/app/pot-exe"]
