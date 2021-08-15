FROM python:3.9.6-alpine3.14
LABEL maintainer='Image to Dockerfile Docker Maintainers <hanxiao2100@qq.com>'

COPY requirements.txt /usr/local/src/
RUN pip install --no-cache-dir -r /usr/local/src/requirements.txt
COPY generate_dockerfile.py /

ENTRYPOINT [ "python", "/generate_dockerfile.py" ]
CMD [ "--help" ]
