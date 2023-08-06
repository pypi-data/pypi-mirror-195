from setuptools import setup, find_packages

setup(
    name="couragesteak_python_sdk_demo",
    version="0.0.1",
    author="有勇气的牛排",
    author_email="warm7758@163.com",
    description="这是项目描述（简短版）",
    long_description="长描述文本",
    url='https://www.couragesteak.com/',
    packages=find_packages(),
    install_requires=[],
    # 搜索关键词
    keywords=['python', 'menu', 'dumb_menu', 'windows', 'mac', 'linux'],
    # 环境：python版本、支持系统...
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
