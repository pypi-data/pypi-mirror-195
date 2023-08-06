#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import  setup

import setuptools

packages = ['cool']# 唯一的包名

setup(name='crmixc-automator',
      version='1.0',
      author='suxiaowei',
      packages=packages,
      package_dir={'requests': 'requests'},
              #python打包可通过pip安装的自定义库
      install_requires=["lxml", "PyHamcrest"]
)