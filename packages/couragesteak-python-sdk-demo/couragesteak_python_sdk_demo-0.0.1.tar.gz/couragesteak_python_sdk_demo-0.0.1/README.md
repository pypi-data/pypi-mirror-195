# dumb_menu

[![Downloads](https://static.pepy.tech/badge/dumb-menu)](https://pepy.tech/project/dumb-menu)

simple_term_menu don't support windows, so i made this.

this is not as powerful as simple_term_menu , but this is **THE GOOD OLD MEUN** .

dumb_menu is a **ligh weight** menu ,support **hot key**, for both **win** and **mac** .


## Installation

https://pypi.org/project/dumb-menu/

https://github.com/cornradio/dumb_menu (i want stars ⭐ uwu)

## Usage

```python
import dumb_menu
options = ["[1]Option 1", "[2]Option 2", "[3]Option 3","[q]quit"]
index = dumb_menu.get_menu_choice(options)
print(f"You selected option {index + 1}: {options[index]}")
```

![png](https://raw.githubusercontent.com/cornradio/imgs/main/20230214163952.png)

## 上传新版本

en: https://packaging.python.org/tutorials/packaging-projects/ 

zh: https://python-packaging-zh.readthedocs.io/zh_CN/latest/minimal.html#id2

1. change `setup.py`
2. testing `python setup.py develop`
3. `python3 setup.py sdist`
4. `twine upload dist/*`

python3 setup.py
本地测试：python setup.py develop
编译：python3 setup.py sdist
上传到pypi：twine upload dist/*

## 更新日志

`0.0.1` 基础版测试

