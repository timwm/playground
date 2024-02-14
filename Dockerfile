FROM ubuntu:latest

RUN apt-get update && \
    apt-get install -y 7z httrack

COPY your-script.sh /app/your-script.sh

WORKDIR /app

CMD ["./your-script.sh"]
