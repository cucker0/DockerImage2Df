#!/usr/bin/env python
#
"""
author: Song yanlin
mail: hanxiao2100@qq.com
date: 2021-06-25
"""

import docker
from docker.errors import ImageNotFound

from sys import argv
import re, os

class DF(object):
    def __init__(self):
        super(DF, self).__init__()
        if not os.path.exists("/var/run/docker.sock"):
            self.help_msg()
            exit(1)
        self.client = docker.DockerClient(base_url='unix://var/run/docker.sock')
        # image name or image id
        self.image = argv[1]
        self.history_msg = []
        self.dockerfile = []

    def _print_dockerfile(self):
        if len(self.history_msg) == 0:
            return
        self.dockerfile.reverse()
        print()
        print("#", " Dockerfile ".center(32, "="))
        for i in self.dockerfile:
            print(i)

    def _expose_format(self, row:str) -> str:
        """比较新的版本的 docker 获取到的 docker image history 中 EXPOSE 字段的信息格式发生了变化。但 Dockerfile 不支持这种格式
        例如 docker 23.0.5 新格式为
        "EXPOSE map[3306/tcp:{} 53/tcp:{} 53/udp:{} 80/tcp:{} 8000/tcp:{}]"
        Dockerfile 中只支持：
        EXPOSE 3306/tcp 53/tcp 53/udp 80/tcp 8000/tcp

        新的格式：
        $ curl --unix-socket /var/run/docker.sock http://localhost/v1.43/images/cucker/dns:all-2.2/history

        [
            {
                "Comment": "buildkit.dockerfile.v0",
                "Created": 1683453195,
                "CreatedBy": "EXPOSE map[3306/tcp:{} 53/tcp:{} 53/udp:{} 80/tcp:{} 8000/tcp:{}]",
                "Id": "<missing>",
                "Size": 0,
                "Tags": null
            },
            ...
        ]

        :param row: 一条 image history CreatedBy 数据
        :return: 过滤处理后的 image history CreatedBy 数据
        """
        if row.startswith('EXPOSE map['):
            return row.replace('map[', '').replace(']', '').replace(':{}', '')
        return row

    def _row_format(self, row):
        _row = re.sub(r"/bin/(ba)?sh -c", 'RUN',
                      row)  # replace "/bin/sh -c" or "/bin/bash -c" to "RUN" for RUN instruction
        _row = re.sub(r"^RUN #\(nop\)", "", _row)  # replace "RUN #(nop)" to none("") for ENV,LABEL... instructions
        # pretty print multi command lines following Docker best practices --start
        _row = re.sub(r";[ ]*\t+", r"; \t", _row)  # replace "; *\t+" to "; \t"
        _row = re.sub(r"(\t+)", r"\\\n\1", _row)  # replace "\t+" to "\\n\t+"
        _row = re.sub(r";[ ]{4,}", r";    ", _row)  # replace ";[ ]{4,}" to ";    " (4+ blank space)
        _row = re.sub(r"([ ]{4,})", r"\\\n\1", _row)  # replace "[ ]{4,}" to "\\n[ ]{4,}"
        # _row = _row.replace("&&", "\\\n    &&")  # replace "&&" to "\\n    &&"
        # _row = re.sub(r"(?!(?:;;))(;)", "; \\\n", _row)  # replace ";;" or ";" to "; \\n"
        # pretty print multi command lines following Docker best practices --end
        _row = _row.strip(' ')

        # docker history <IMAGE> 显示的CMD多个参数之间没有"," 分隔. ENTRYPOINT也是同样的情况。
        # 当前测试的 docker 版本：docker 20.10.6
        # 示例：
        # CMD ["nginx" "-g" "daemon off;"]
        # ENTRYPOINT ["/usr/sbin/nginx" "-g" "daemon off"]
        if _row.startswith("CMD [") or _row.startswith("ENTRYPOINT ["):
            _row = _row.replace('" "', '", "')
        _row = self._expose_format(_row)
        self.dockerfile.append(_row)

    def _get_history_msg(self):
        try:
            image = self.client.images.get(self.image)
            if isinstance(image, docker.models.images.Image):
                self.history_msg = image.history()
        except ImageNotFound as e:
            print(e)

    def _parse_history_msg(self):
        """parse image history json data

        An example for image history json data with docker api http, it will be a list, if docker API SDK python
        $ curl --unix-socket /var/run/docker.sock http://localhost/v1.41/images/hanxiao/mynginx:4.1/history
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
            // The following information is FROM BASIC_IMAGE
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
        :return:
        """
        if len(self.history_msg) == 0:
            return
        tags = None  # The last "Not null Tags" of image history json data. It may not be the third from the back of json data(or List, if python SDK)
        tags_not_null_count = 0
        length = len(self.history_msg)

        # Ignore the information from BASIC_IMAGE
        if self.history_msg[-1]['Created'] == self.history_msg[-2]['Created'] \
                and self.history_msg[-1]["Id"] == '<missing>' \
                and self.history_msg[-2]["Id"] == '<missing>' \
                and re.search(r"#\(nop\) ADD file:\w{64} in /", self.history_msg[-1]['CreatedBy']) \
                and re.search(r'#\(nop\)[ ]+CMD \["bash"\]', self.history_msg[-2]['CreatedBy']):
            length -= 2

        for i in range(length):
            layer = self.history_msg[i]
            if layer['Tags']:
                tags_not_null_count += 1
                tags = layer['Tags']
                if tags_not_null_count >= 2:
                    break
            self._row_format(layer['CreatedBy'])

        # add FROM instruction
        self.dockerfile.append("FROM {}".format(tags[0]))

    def help_msg(self):
        _MSG = """Usage:
# Command alias
echo "alias image2df='docker run --rm -v /var/run/docker.sock:/var/run/docker.sock cucker/image2df'" >> ~/.bashrc
. ~/.bashrc

# Excute command
image2df <IMAGE>
"""
        print(_MSG)

    def start(self):
        self._get_history_msg()
        self._parse_history_msg()
        self._print_dockerfile()


if __name__ == '__main__':
    df = DF()
    if len(argv) < 2 or argv[1] in ("--help", "-h"):
        df.help_msg()
        exit(1)
    ret = df.start()
