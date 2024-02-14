FROM ubuntu:latest

RUN apt-get update && \
    apt-get install -y p7zip httrack

COPY your-script.sh .

RUN chmod +x /app/your-script.sh

WORKDIR /app

CMD ["./your-script.sh"]
