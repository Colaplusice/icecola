## fjl的 python 工具包

### 安装 setuptools wheel， 安装twine

- python3 -m pip install --user --upgrade setuptools wheel
- python3 -m pip install --user --upgrade twine

### 打包发布

- python3 setup.py sdist bdist_wheel
- 测试服 python3 -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*
- pypi: python3 -m twine upload dist/*

## 运行后生成

python_utils.egg-info
build
dist

## 安装方法

- pip install -i https://test.pypi.org/simple/ icecola

## 使用

- import crawler_utils

