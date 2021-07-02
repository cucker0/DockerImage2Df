* mysql image
    ```bash
    curl --unix-socket /var/run/docker.sock http://localhost/v1.41/images/mysql/history
    ```
    result
    ```json
    [
        {
            "Comment": "",
            "Created": 1618858607,
            "CreatedBy": "/bin/sh -c #(nop)  CMD [\"mysqld\"]",
            "Id": "sha256:0627ec6901db4b2aed6ca7ab35e43e19838ba079fffe8fe1be66b6feaad694de",
            "Size": 0,
            "Tags": [
                "mysql:latest"
            ]
        },
        {
            "Comment": "",
            "Created": 1618858607,
            "CreatedBy": "/bin/sh -c #(nop)  EXPOSE 3306 33060",
            "Id": "<missing>",
            "Size": 0,
            "Tags": null
        },
        {
            "Comment": "",
            "Created": 1618858607,
            "CreatedBy": "/bin/sh -c #(nop)  ENTRYPOINT [\"docker-entrypoint.sh\"]",
            "Id": "<missing>",
            "Size": 0,
            "Tags": null
        },
        {
            "Comment": "",
            "Created": 1618858606,
            "CreatedBy": "/bin/sh -c ln -s usr/local/bin/docker-entrypoint.sh /entrypoint.sh # backwards compat",
            "Id": "<missing>",
            "Size": 34,
            "Tags": null
        },
        {
            "Comment": "",
            "Created": 1618858605,
            "CreatedBy": "/bin/sh -c #(nop) COPY file:345a22fe55d3e6783a17075612415413487e7dba27fbf1000a67c7870364b739 in /usr/local/bin/ ",
            "Id": "<missing>",
            "Size": 14542,
            "Tags": null
        },
        {
            "Comment": "",
            "Created": 1618858605,
            "CreatedBy": "/bin/sh -c #(nop) COPY dir:2e040acc386ebd23b8571951a51e6cb93647df091bc26159b8c757ef82b3fcda in /etc/mysql/ ",
            "Id": "<missing>",
            "Size": 1123,
            "Tags": null
        },
        {
            "Comment": "",
            "Created": 1618858605,
            "CreatedBy": "/bin/sh -c #(nop)  VOLUME [/var/lib/mysql]",
            "Id": "<missing>",
            "Size": 0,
            "Tags": null
        },
        {
            "Comment": "",
            "Created": 1618858604,
            "CreatedBy": "/bin/sh -c { \t\techo mysql-community-server mysql-community-server/data-dir select ''; \t\techo mysql-community-server mysql-community-server/root-pass password ''; \t\techo mysql-community-server mysql-community-server/re-root-pass password ''; \t\techo mysql-community-server mysql-community-server/remove-test-db select false; \t} | debconf-set-selections \t&& apt-get update \t&& apt-get install -y \t\tmysql-community-client=\"${MYSQL_VERSION}\" \t\tmysql-community-server-core=\"${MYSQL_VERSION}\" \t&& rm -rf /var/lib/apt/lists/* \t&& rm -rf /var/lib/mysql && mkdir -p /var/lib/mysql /var/run/mysqld \t&& chown -R mysql:mysql /var/lib/mysql /var/run/mysqld \t&& chmod 1777 /var/run/mysqld /var/lib/mysql",
            "Id": "<missing>",
            "Size": 420345479,
            "Tags": null
        },
        {
            "Comment": "",
            "Created": 1618858591,
            "CreatedBy": "/bin/sh -c echo 'deb http://repo.mysql.com/apt/debian/ buster mysql-8.0' > /etc/apt/sources.list.d/mysql.list",
            "Id": "<missing>",
            "Size": 55,
            "Tags": null
        },
        {
            "Comment": "",
            "Created": 1618858590,
            "CreatedBy": "/bin/sh -c #(nop)  ENV MYSQL_VERSION=8.0.24-1debian10",
            "Id": "<missing>",
            "Size": 0,
            "Tags": null
        },
        {
            "Comment": "",
            "Created": 1618039334,
            "CreatedBy": "/bin/sh -c #(nop)  ENV MYSQL_MAJOR=8.0",
            "Id": "<missing>",
            "Size": 0,
            "Tags": null
        },
        {
            "Comment": "",
            "Created": 1618039334,
            "CreatedBy": "/bin/sh -c set -ex; \tkey='A4A9406876FCBD3C456770C88C718D3B5072E1F5'; \texport GNUPGHOME=\"$(mktemp -d)\"; \tgpg --batch --keyserver ha.pool.sks-keyservers.net --recv-keys \"$key\"; \tgpg --batch --export \"$key\" > /etc/apt/trusted.gpg.d/mysql.gpg; \tgpgconf --kill all; \trm -rf \"$GNUPGHOME\"; \tapt-key list > /dev/null",
            "Id": "<missing>",
            "Size": 2611,
            "Tags": null
        },
        {
            "Comment": "",
            "Created": 1618039332,
            "CreatedBy": "/bin/sh -c apt-get update && apt-get install -y --no-install-recommends \t\tpwgen \t\topenssl \t\tperl \t\txz-utils \t&& rm -rf /var/lib/apt/lists/*",
            "Id": "<missing>",
            "Size": 52242133,
            "Tags": null
        },
        {
            "Comment": "",
            "Created": 1618039323,
            "CreatedBy": "/bin/sh -c mkdir /docker-entrypoint-initdb.d",
            "Id": "<missing>",
            "Size": 0,
            "Tags": null
        },
        {
            "Comment": "",
            "Created": 1618039322,
            "CreatedBy": "/bin/sh -c set -eux; \tsavedAptMark=\"$(apt-mark showmanual)\"; \tapt-get update; \tapt-get install -y --no-install-recommends ca-certificates wget; \trm -rf /var/lib/apt/lists/*; \tdpkgArch=\"$(dpkg --print-architecture | awk -F- '{ print $NF }')\"; \twget -O /usr/local/bin/gosu \"https://github.com/tianon/gosu/releases/download/$GOSU_VERSION/gosu-$dpkgArch\"; \twget -O /usr/local/bin/gosu.asc \"https://github.com/tianon/gosu/releases/download/$GOSU_VERSION/gosu-$dpkgArch.asc\"; \texport GNUPGHOME=\"$(mktemp -d)\"; \tgpg --batch --keyserver hkps://keys.openpgp.org --recv-keys B42F6819007F00F88E364FD4036A9C25BF357DD4; \tgpg --batch --verify /usr/local/bin/gosu.asc /usr/local/bin/gosu; \tgpgconf --kill all; \trm -rf \"$GNUPGHOME\" /usr/local/bin/gosu.asc; \tapt-mark auto '.*' > /dev/null; \t[ -z \"$savedAptMark\" ] || apt-mark manual $savedAptMark > /dev/null; \tapt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false; \tchmod +x /usr/local/bin/gosu; \tgosu --version; \tgosu nobody true",
            "Id": "<missing>",
            "Size": 4170918,
            "Tags": null
        },
        {
            "Comment": "",
            "Created": 1618039310,
            "CreatedBy": "/bin/sh -c #(nop)  ENV GOSU_VERSION=1.12",
            "Id": "<missing>",
            "Size": 0,
            "Tags": null
        },
        {
            "Comment": "",
            "Created": 1618039310,
            "CreatedBy": "/bin/sh -c apt-get update && apt-get install -y --no-install-recommends gnupg dirmngr && rm -rf /var/lib/apt/lists/*",
            "Id": "<missing>",
            "Size": 9342868,
            "Tags": null
        },
        {
            "Comment": "",
            "Created": 1618039302,
            "CreatedBy": "/bin/sh -c groupadd -r mysql && useradd -r -g mysql mysql",
            "Id": "<missing>",
            "Size": 328574,
            "Tags": null
        },
        {
            "Comment": "",
            "Created": 1618017622,
            "CreatedBy": "/bin/sh -c #(nop)  CMD [\"bash\"]",
            "Id": "<missing>",
            "Size": 0,
            "Tags": null
        },
        {
            "Comment": "",
            "Created": 1618017622,
            "CreatedBy": "/bin/sh -c #(nop) ADD file:c855b3c65f5ba94d548d7d2659094eeb63fbf7f8419ac8e07712c3320c38b62c in / ",
            "Id": "<missing>",
            "Size": 69251205,
            "Tags": null
        }
    ]
    ```

* hanxiao/mynginx:4.1 image
    ```bash
    curl --unix-socket /var/run/docker.sock http://localhost/v1.41/images/hanxiao/mynginx:4.1/history
    ```
    result
    ```json
    [
        {
            "Comment": "",
            "Created": 1623297136,
            "CreatedBy": "/bin/sh -c #(nop)  ENTRYPOINT [\"/usr/sbin/nginx\"]",
            "Id": "sha256:7ff1fe56a3b6586340dcf6334b7070db86bcd1b8949076a7e271d3462e20da4c",
            "Size": 0,
            "Tags": [
                "hanxiao/mynginx:4.1"
            ]
        },
        {
            "Comment": "",
            "Created": 1623297136,
            "CreatedBy": "/bin/sh -c #(nop)  CMD [\"-g\" \"daemon off;\"]",
            "Id": "sha256:e7ab9548a07051518fd9dd64a629d094eb52cee469432a22cdc37502f6e9abe4",
            "Size": 0,
            "Tags": null
        },
        {
            "Comment": "",
            "Created": 1623297136,
            "CreatedBy": "/bin/sh -c #(nop)  EXPOSE 80",
            "Id": "sha256:759878630589acaefb33c401315925b0f4392731db70df9b68f4f684a2a863b8",
            "Size": 0,
            "Tags": null
        },
        {
            "Comment": "",
            "Created": 1623297136,
            "CreatedBy": "/bin/sh -c echo \"Nginx Web: CMD defining default arguments for an ENTRYPOINT\" > /usr/share/nginx/html/index.html",
            "Id": "sha256:df66d73420f54aeb0763ed3baa1ba38a50e3431cbb191c390554d4c2ac6cafb7",
            "Size": 60,
            "Tags": null
        },
        {
            "Comment": "",
            "Created": 1623297135,
            "CreatedBy": "/bin/sh -c yum install -y nginx",
            "Id": "sha256:868708ae954cd1026022deb763c9450282f7351ac72c735fc719854eecc9c01c",
            "Size": 103856780,
            "Tags": null
        },
        {
            "Comment": "",
            "Created": 1623297120,
            "CreatedBy": "/bin/sh -c #(nop)  LABEL maintainer=NGINX Docker Maintainers <docker-maint@nginx.com>",
            "Id": "sha256:8bbd34571cf3d75400d5934ce063fc0bed63933baa677cb3ac522576032c703b",
            "Size": 0,
            "Tags": null
        },
        {
            "Comment": "",
            "Created": 1607386973,
            "CreatedBy": "/bin/sh -c #(nop)  CMD [\"/bin/bash\"]",
            "Id": "sha256:300e315adb2f96afe5f0b2780b87f28ae95231fe3bdd1e16b9ba606307728f55",
            "Size": 0,
            "Tags": [
                "centos:8",
                "centos:latest"
            ]
        },
        {
            "Comment": "",
            "Created": 1607386972,
            "CreatedBy": "/bin/sh -c #(nop)  LABEL org.label-schema.schema-version=1.0 org.label-schema.name=CentOS Base Image org.label-schema.vendor=CentOS org.label-schema.license=GPLv2 org.label-schema.build-date=20201204",
            "Id": "<missing>",
            "Size": 0,
            "Tags": null
        },
        {
            "Comment": "",
            "Created": 1607386972,
            "CreatedBy": "/bin/sh -c #(nop) ADD file:bd7a2aed6ede423b719ceb2f723e4ecdfa662b28639c8429731c878e86fb138b in / ",
            "Id": "<missing>",
            "Size": 209348104,
            "Tags": null
        }
    ]
    ```