FROM ubuntu:latest

RUN apt-get update && \
    apt-get install -y p7zip httrack git

COPY your-script.sh /app/

RUN pwd
RUN ls -al

RUN chmod +x /app/your-script.sh

WORKDIR /app

CMD ["./your-script.sh"]

# ENV GITHUB_TOKEN 
RUN git config --global user.email "timon.w.mesulam935xpacenuchra@gmail.com"
RUN git config --global user.name "timon w. mesulam"
RUN git init
RUN git add .
RUN git commit -m "Add result file"
RUN git remote add origin https://github.com/timwm/playground.git
RUN git push -u origin master