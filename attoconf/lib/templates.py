#   Copyright 2013-2014 Ben Longbons <b.r.longbons@gmail.com>
#
#   This file is part of attoconf.
#
#   attoconf is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   attoconf is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with attoconf.  If not, see <http://www.gnu.org/licenses/>.



import os
import sys

from ..classy import ClassyProject


class TemplateHook(object):
    __slots__ = ('outfiles')
    def __init__(self, outfiles):
        self.outfiles = outfiles

    def __call__(self, build):
        build.vars['SRC_DIR'] = build.relative_source()
        unseen = set(build.project.order)
        if None in unseen:
            unseen.remove(None)
        for outfile in self.outfiles:
            infile = outfile + '.in'
            print('Generating %s from %s' % (outfile, infile))
            # by replacing all instances of @VARIABLE@ with the value

            with open(os.path.join(build.project.srcdir, infile), encoding="utf-8") as infile:
                slurpee = infile.read()
                for var in build.project.order:
                    if var is None:
                        continue
                    val = build.vars[var]
                    key = '@' + var + '@'
                    if key not in slurpee:
                        continue
                    if var in unseen:
                        unseen.remove(var)
                    slurpee = slurpee.replace(key, str(val))
                # Ensure that the parent directory of the output file exists
                outdir = os.path.dirname(os.path.join(build.builddir, outfile))
                if not os.path.exists(outdir):
                    os.makedirs(outdir)
                with open(os.path.join(build.builddir, outfile), 'w', encoding="utf-8") as out:
                    out.write(slurpee)
        if unseen:
            print('WARNING: variables not used:')
            print('  ' + '\n  '.join(unseen))
        # lone @s may legitimately appear in the makefile.
        # paired @s, which would be a forgotten subst, will be obvious.


class Templates(ClassyProject):
    ''' Post hook to generate output files from *.in templates
    '''
    __slots__ = ()
    _merge_slots_ = ('template_files')

    # this class didn't exist in attoconf < 0.7, no need for compatibility
    def __init__(self, template_files, **kwargs):
        super(Templates, self).__init__(**kwargs)
        self.template_files = template_files

    def post(self):
        super(Templates, self).post()
        if 'SRC_DIR' in self.order:
            sys.exit('ERROR: Incompatible generator hooks!')
        self.order.insert(0, 'SRC_DIR')
        self.checks.append(TemplateHook(self.template_files))
