# DockerImage2Df

## What is DockerImage2Df
**DockerImage2Df** is tool for Generate Dockerfile from a image.

This tool is very useful when you only have docker image and need to generate a Dockerfile whit it.


## How to use this image
```bash
# Command alias
echo "alias image2df='docker run -v /var/run/docker.sock:/var/run/docker.sock --rm cucker/image2df'" >> ~/.bashrc
. ~/.bashrc

# Excute command
image2df <IMAGE>
```

* See help
    ```bash
    docker run --rm cucker/image2df --help
    ```

* For example
    ```bash
    $ echo "alias image2df='docker run -v /var/run/docker.sock:/var/run/docker.sock --rm cucker/image2df'" >> ~/.bashrc
    $ . ~/.bashrc
    $ docker pull mysql
    $ image2df mysql

    ========== Dockerfile ==========
    FROM mysql:latest
    RUN groupadd -r mysql && useradd -r -g mysql mysql
    RUN apt-get update && apt-get install -y --no-install-recommends gnupg dirmngr && rm -rf /var/lib/apt/lists/*
    ENV GOSU_VERSION=1.12
    RUN set -eux; \
        savedAptMark="$(apt-mark showmanual)"; \
        apt-get update; \
        apt-get install -y --no-install-recommends ca-certificates wget; \
        rm -rf /var/lib/apt/lists/*; \
        dpkgArch="$(dpkg --print-architecture | awk -F- '{ print $NF }')"; \
        wget -O /usr/local/bin/gosu "https://github.com/tianon/gosu/releases/download/$GOSU_VERSION/gosu-$dpkgArch"; \
        wget -O /usr/local/bin/gosu.asc "https://github.com/tianon/gosu/releases/download/$GOSU_VERSION/gosu-$dpkgArch.asc"; \
        export GNUPGHOME="$(mktemp -d)"; \
        gpg --batch --keyserver hkps://keys.openpgp.org --recv-keys B42F6819007F00F88E364FD4036A9C25BF357DD4; \
        gpg --batch --verify /usr/local/bin/gosu.asc /usr/local/bin/gosu; \
        gpgconf --kill all; \
        rm -rf "$GNUPGHOME" /usr/local/bin/gosu.asc; \
        apt-mark auto '.*' > /dev/null; \
        [ -z "$savedAptMark" ] || apt-mark manual $savedAptMark > /dev/null; \
        apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false; \
        chmod +x /usr/local/bin/gosu; \
        gosu --version; \
        gosu nobody true
    RUN mkdir /docker-entrypoint-initdb.d
    RUN apt-get update && apt-get install -y --no-install-recommends \
            pwgen \
            openssl \
            perl \
            xz-utils \
        && rm -rf /var/lib/apt/lists/*
    RUN set -ex; \
        key='A4A9406876FCBD3C456770C88C718D3B5072E1F5'; \
        export GNUPGHOME="$(mktemp -d)"; \
        gpg --batch --keyserver ha.pool.sks-keyservers.net --recv-keys "$key"; \
        gpg --batch --export "$key" > /etc/apt/trusted.gpg.d/mysql.gpg; \
        gpgconf --kill all; \
        rm -rf "$GNUPGHOME"; \
        apt-key list > /dev/null
    ENV MYSQL_MAJOR=8.0
    ENV MYSQL_VERSION=8.0.24-1debian10
    RUN echo 'deb http://repo.mysql.com/apt/debian/ buster mysql-8.0' > /etc/apt/sources.list.d/mysql.list
    RUN { \
            echo mysql-community-server mysql-community-server/data-dir select ''; \
        echo mysql-community-server mysql-community-server/root-pass password ''; \
        echo mysql-community-server mysql-community-server/re-root-pass password ''; \
        echo mysql-community-server mysql-community-server/remove-test-db select false; \
        } | debconf-set-selections \
        && apt-get update \
        && apt-get install -y \
            mysql-community-client="${MYSQL_VERSION}" \
            mysql-community-server-core="${MYSQL_VERSION}" \
        && rm -rf /var/lib/apt/lists/* \
        && rm -rf /var/lib/mysql && mkdir -p /var/lib/mysql /var/run/mysqld \
        && chown -R mysql:mysql /var/lib/mysql /var/run/mysqld \
        && chmod 1777 /var/run/mysqld /var/lib/mysql
    VOLUME [/var/lib/mysql]
    COPY dir:2e040acc386ebd23b8571951a51e6cb93647df091bc26159b8c757ef82b3fcda in /etc/mysql/
    COPY file:345a22fe55d3e6783a17075612415413487e7dba27fbf1000a67c7870364b739 in /usr/local/bin/
    RUN ln -s usr/local/bin/docker-entrypoint.sh /entrypoint.sh # backwards compat
    ENTRYPOINT ["docker-entrypoint.sh"]
    EXPOSE 3306 33060
    CMD ["mysqld"]
    ```

## How does it work
1. Get the image history data by Docker API of python SDK, the data format is a List (python).
    ```
    >>> import docker
    >>> client = docker.DockerClient(base_url='unix://var/run/docker.sock')
    >>> hist = client.images.get("image_name_or_id").history()
    >>> print(hist)
    >>> 
    >>> # for mysql 
    >>> hist = client.images.get("mysql").history()
    >>> print(hist)
    >>> [
    {
        'Comment': '',
        'Created': 1618858607,
        'CreatedBy': '/bin/sh-c#(nop)CMD[
            "mysqld"
        ]',
        'Id': 'sha256: 0627ec6901db4b2aed6ca7ab35e43e19838ba079fffe8fe1be66b6feaad694de',
        'Size': 0,
        'Tags': [
            'mysql: latest'
        ]
    },
    ...
    ]
    ```
2. Parse the history data by a python script--[generate_dockerfile.py](py/generate_dockerfile.py).

## How to make the docker image for DockerImage2Df 
* Prerequisites
    * [Install Docker Engine](https://docs.docker.com/engine/install/)
    * Python 3
    * [Docker SDK for Python](https://docker-py.readthedocs.io/en/stable/)
    

* prepare files
    ```text
    /mydocker/image2df/
    ├── Dockerfile
    ├── generate_dockerfile.py  // generate dockerfile script of python
    └── requirements.txt  // requirements for python module
    ```
    * [Dockerfile](docker/Dockerfile)
    * [generate_dockerfile.py](py/generate_dockerfile.py)
    * [requirements.txt](py/generate_dockerfile.py)

* Create repository
    
    login to https://hub.docker.com, Create a repository, format is `<ID>/repository-name`, for example: `cucker/image2df`
    
* Build image
    ```bash
    cd /mydocker/image2df/
    docker build -f ./Dockerfile -t cucker/image2df:1.0 .
    ```
* Tag image alias
    ```bash
    docker tag cucker/image2df:1.0 cucker/image2df:latest
    ```
* Push image to DockerHub
    * login in DockerHub
        ```bash
        $ docker login  
        Username:    // user_ID
        Password:    // password
        ```
    
    * push image
        ```bash
        docker push cucker/image2df:1.0
        docker push cucker/image2df:latest
        ```

## Generate Dockerfile from a image by python script
* Prerequisites
    * [Install Docker Engine](https://docs.docker.com/engine/install/)
    * Python 3
    * [Docker SDK for Python](https://docker-py.readthedocs.io/en/stable/)
        ```bash
        pip install docker six
        ```
* Copy [generate_dockerfile.py](py/generate_dockerfile.py) script to workdir
* Usage
    ```bash
    python ./generate_dockerfile.py <IMAGE>
    ```

## Other
* [Example whit docker API for http](doc/api_for_http_test.md)

    reference
    * https://docker-py.readthedocs.io/en/stable/
    * https://docker-py.readthedocs.io/en/stable/client.html#client-reference
    * https://docs.docker.com/engine/api/sdk/examples/
    * https://docs.docker.com/engine/api/v1.41/#operation/ImageHistory
    * https://docs.docker.com/engine/api/sdk/
    * [Docker API version with Docker version matrix](https://docs.docker.com/engine/api/#api-version-matrix)

