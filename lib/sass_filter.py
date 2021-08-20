# -*- coding: utf-8 -*-
"""
Libsass output filter for flask-assets
"""

import sass
from webassets.filter import Filter


class LibSass(Filter):
    name = 'libsass-output'
    options = {
        'output_style': 'SASS_OUTPUT_STYLE'
    }

    def __init__(self, include_paths=[], *args, **kwargs):
        super(LibSass, self).__init__(*args, **kwargs)
        self.include_paths = include_paths

    def _apply_sass(self, src):
        return sass.compile(
            string=src,
            output_style='expanded',
            include_paths=getattr(self, 'include_paths', []))

    def output(self, _in, out, **kwargs):
        out.write(self._apply_sass(_in.read()))

    def input(self, _in, out, **kwargs):
        out.write(_in.read())
