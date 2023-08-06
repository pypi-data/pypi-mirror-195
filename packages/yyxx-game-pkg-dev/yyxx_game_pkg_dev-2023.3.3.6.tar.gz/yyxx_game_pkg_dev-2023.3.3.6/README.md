# git-pypi-dev

## 安装poetry环境
本工程使用poetry进行包管理，首先部署poetry环境：

#### 安装poetry
- `curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python`

#### 配置虚拟环境并显式激活
- `poetry env use python3`
- `poetry shell`

## 构建发布包

#### 构建
- `poetry build`
#### 发布
- `poetry publish`

## 官方文档
[peotry](https://python-poetry.org/docs/)