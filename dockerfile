FROM python:3-slim
COPY . /app
WORKDIR /app
EXPOSE 8501
RUN bash bash_scripts/install_stuff.sh