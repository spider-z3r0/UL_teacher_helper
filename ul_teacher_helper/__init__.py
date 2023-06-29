#!/usr/bin/env python
# -*- coding: utf-8 -*-

##Import all functions from the submodules

# The Module class (which is funny because it's a module called Module)
from .Module import Module

# The Assessment class
from .Assessment import Assessment


__all__ = [
    'Module',
    'Assessment'
]