# RUN Project

<br/>

```
$ sudo apt update; sudo apt install make build-essential libssl-dev zlib1g-dev \
libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm \
libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev
```

<br/>

pyenv already installed

```
$ pyenv --version
pyenv 2.3.11
```

<br/>

```
$ pyenv install 3.10
$ pyenv global 3.10
```

<br/>

```
$ cd chapter03_project/
$ python -m venv venv
$ source venv/bin/activate
```

<br/>

```
$ pip install -r ./requirements.txt
```

<br/>

```
$ cd ../
$ uvicorn chapter03_project.app:app
```

<br/>

```
http://127.0.0.1:8000/docs
```
