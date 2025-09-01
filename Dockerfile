FROM rocker/r-ver:4.3.2
RUN R -e "install.packages(c('plumber','jsonlite','forecast'))"
WORKDIR /app
COPY plumber.R .
ENV R_PORT=8000
EXPOSE 8000
CMD ["R", "-e", "pr <- plumber::plumb('plumber.R'); pr$run(host='0.0.0.0', port=as.integer(Sys.getenv('R_PORT','8000')))"]
