FROM jupyter/datascience-notebook:latest
RUN pip install jupyter_http_over_ws
RUN jupyter server extension enable --py jupyter_http_over_ws
# RUN Rscript -e 'install.packages("psych", repos="https://cloud.r-project.org")'
