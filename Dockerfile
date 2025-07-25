FROM ubuntu:24.04

WORKDIR /app

COPY pot-exe .

RUN chmod +x /app/pot-exe

ENTRYPOINT ["/app/pot-exe"]
