FROM python:3.9.6-alpine3.14
LABEL maintainer='Image to Dockerfile Docker Maintainers <hanxiao2100t@qq.com>'

COPY requirements.txt /usr/local/src/
COPY generate_dockerfile.py /
RUN pip install --no-cache-dir -r /usr/local/src/requirements.txt

ENTRYPOINT [ "python", "/generate_dockerfile.py" ]
CMD [ "--help" ]
