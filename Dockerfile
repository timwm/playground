FROM ubuntu:latest

RUN apt-get update && \
    apt-get install -y p7zip httrack

COPY your-script.sh /app/

RUN pwd
RUN ls -al

RUN chmod +x /app/your-script.sh

WORKDIR /app

CMD ["./your-script.sh"]

RUN git config --global user.email "actions@github.com"
RUN git config --global user.name "GitHub Actions"
RUN git init
RUN git add .
RUN git commit -m "Add result file"
RUN git remote add origin https://timwm@github.com/playground.git
RUN git push -f origin master