apt-get update -q
apt-get -y --no-install-recommends install \
        python3-pip \
        python-dev \
        libssl-dev \
    python3-setuptools \
    build-essential \
    libssl-dev \
    libffi-dev \
    libxml2-dev \
    libxslt1-dev \
    zlib1g-dev \
    python3-dev \
    vim \
    fontconfig

pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple/ --upgrade pip
pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple/ scrapy
pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple/ requests
pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple/ selenium
pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple/ redis
pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple/ pymongo
