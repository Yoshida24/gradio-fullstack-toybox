# gradio-fullstack-toybox

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/Yoshida24/gradio-fullstack-toybox)

gradioを使って気軽に色々作ってみる。保守性を考えない。

> ref. https://www.gradio.app/


## 環境

- OS: Sonoma 14.4
- Python: 3.11
- pip: 24.0
- GNU Make: 3.81
- Machine: M1 Macbook Air


## 開発を始める

**セットアップ**

```bash
# Make virtual env
python -m venv .venv
. .venv/bin/activate

# install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# To use environment variables in .env file, run below script to create .env
if [ ! -f .env ]; then
    cp .env.sample .env
    echo 'Info: .env file has successfully created. Please rewrite .env file'
else
    echo 'Info: Skip to create .env file. Because it is already exists.'
fi
```

**`src/main.py`を開発モードで起動する**
> Note:
> 開発モードではホットリロードが有効になり、スクリプトの保存の都度、自動的にサーバーがリロードされます。

```bash
make dev
```

**`src/main.py`を起動する**

```bash
make run
```


## Useful Commands

**Use JupyterLab**

```bash
jupyter lab
```

**Activate `venv`**

```bash
source .venv/bin/activate
```

**Save requirements**

```bash
pip freeze > requirements.txt
```

**Deactivate venv**

```bash
deactivate
```
