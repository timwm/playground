FROM ubuntu:latest

RUN apt-get update && \
    apt-get install -y p7zip httrack

COPY your-script.sh .

RUN pwd

RUN chmod +x ./your-script.sh

WORKDIR /app

CMD ["./your-script.sh"]
