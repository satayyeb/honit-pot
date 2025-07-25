FROM debian:bullseye-slim

WORKDIR /app

COPY pot-exe .

RUN chmod +x /app/pot-exe

RUN file /app/pot-exe

ENTRYPOINT ["/app/pot-exe"]
