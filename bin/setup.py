# -*- coding: cp1251 -*-
# setup.py
from distutils.core import setup
import py2exe

setup(name="impexp",
      version="0.5",
      description="Automated robot for working with GMS OfficeTools Import/Export",
      author="Andrew Kornilov",
      author_email="andy@eva.dp.ua",
      url="http://www.eva.dp.ua/~andy",
      scripts=["kernel.py"],
)
