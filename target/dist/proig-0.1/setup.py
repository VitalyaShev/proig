#!/usr/bin/env python
#   -*- coding: utf-8 -*-

from setuptools import setup
from setuptools.command.install import install as _install

class install(_install):
    def pre_install_script(self):
        pass

    def post_install_script(self):
        pass

    def run(self):
        self.pre_install_script()

        _install.run(self)

        self.post_install_script()

if __name__ == '__main__':
    setup(
        name = 'proig',
        version = '0.1',
        description = '',
        long_description = 'Offline player for playing your music',
        long_description_content_type = None,
        classifiers = [
            'Development Status :: 3 - Alpha',
            'Programming Language :: Python'
        ],
        keywords = '',

        author = 'Vitalii Shevtsov, Konstantin Troitskii, Ivan Eshenko',
        author_email = 'v.shevtsov@g.nsu.ru, k.troitskii@g.nsu.ru, i.eshchenko@g.nsu.ru',
        maintainer = '',
        maintainer_email = '',

        license = 'None',

        url = '',
        project_urls = {},

        scripts = [],
        packages = [],
        namespace_packages = [],
        py_modules = ['main'],
        entry_points = {},
        data_files = [],
        package_data = {},
        install_requires = [],
        dependency_links = [],
        zip_safe = True,
        cmdclass = {'install': install},
        python_requires = '',
        obsoletes = [],
    )
