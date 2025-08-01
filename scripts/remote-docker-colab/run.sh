# Building the docker image
docker build -t zenjupyterlab:latest .

# Lets run the built image
docker run -it -v ${PWD}:/home/user --rm -p 8888:8888 zenjupyterlab:latest \
    start-notebook.sh --ip=0.0.0.0 --no-browser --allow-root \
    --NotebookApp.allow_origin_pat='https://colab.research.google.com|https?://(localhost|127.0.0.1):[0-9]{2,5}' \
    --NotebookApp.port_retries=0 --NotebookApp.token='jupyterlab' \
    --NotebookApp.allow_credentials=True
#   --NotebookApp.disable_check_xsrf=True

