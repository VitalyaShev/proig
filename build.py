#   -*- coding: utf-8 -*-
from pybuilder.core import use_plugin, init, Author

use_plugin("python.core")
use_plugin("python.unittest")
use_plugin("python.flake8")
use_plugin("python.coverage")
use_plugin("python.distutils")
use_plugin("python.sphinx")


name = "proig"
version = "0.1"
description = """Offline player for playing your music"""
authors = [Author("Vitalii Shevtsov", "v.shevtsov@g.nsu.ru", "application development"),
           Author("Konstantin Troitskii", "k.troitskii@g.nsu.ru", "application development"),
           Author("Ivan Eshenko", "i.eshchenko@g.nsu.ru", "design & documentation")]
license = "None"
default_task = "publish"


@init
def set_properties(project):
    project.set_property("coverage_break_build", False)
