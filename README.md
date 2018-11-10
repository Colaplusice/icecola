## fjl的 python 工具包

### 打包发布
python3 -m pip install --user --upgrade setuptools wheel
python3 -m pip install --user --upgrade twine

python3 setup.py sdist bdist_wheel

twine upload --repository-url https://test.pypi.org/legacy/ dist/*

## 运行后生成的三个文件夹

python_utils.egg-info
build
dist

## 安装方法

python setup.py install
