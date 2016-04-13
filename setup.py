#!/usr/bin/env python3

from __future__ import print_function

import distutils.core, \
    distutils.command.install, \
    distutils.command.install_data, \
    distutils.command.build_py
import os, sys

PACKAGE_NAME = 'new_script'

## @TODO Figure out how this should get set by default.  (Maybe
##   initialize it to $HOME/.local ?)
_prefix = None


class MyInstall(distutils.command.install.install):
    def run(self, *args, **kwargs):
        '''Persist the installation prefix so that it can be used in
        :class:`MyBuildPy. <MyBuildPy>`
        '''
        assert not (self.home is not None and self.prefix is not None), \
            'distutils enforces that either home or prefix is specified, ' \
            ' but not both.'

        global _prefix
        if self.home is not None:
            _prefix = self.home
        elif self.prefix is not None:
            _prefix = self.prefix
        _prefix = os.path.abspath(os.path.expanduser(_prefix))
        #return super().run(*args, **kwargs)
        return distutils.command.install.install.run(self, *args, **kwargs)

        
class MyInstallData(distutils.command.install_data.install_data):
    def run(self, *args, **kwargs):
        '''Create a directory for log files.
        '''
        dirs = (os.path.join(self.install_dir, 'var', 'log', PACKAGE_NAME),
        )
       
        for target in dirs:
            if not os.path.isdir(target):
                print('creating', target)
                os.makedirs(target)

        #return super().run(*args, **kwargs)
        return distutils.command.install_data.install_data.run(self, *args,
                                                               **kwargs)


class MyBuildPy(distutils.command.build_py.build_py):
    def run(self, *args, **kwargs):
        '''Create a local_conf.py file that supplies where the program is
        installed.  This functionality is helpful for
        e.g. automatically inferring the location of config files.
        (Playing games with the __file__ variable may not work for all
        systems.)  We write it to our own lib directory so that the
        build_py machinery autodiscovers local_conf.py and does all
        the usual stuff and copies into the build/ directory.
        '''
        ret = None
        thisDir = os.path.dirname(__file__)
        filename = os.path.join(thisDir, 'bin', PACKAGE_NAME, 'local_conf.py')
        try:
            print('Writing:', filename)
            with open(filename, 'w') as fout:
                fout.write("prefix='{prefix}'\n".format(prefix=_prefix))
            #ret = super().run(*args, **kwargs)
            ret = distutils.command.build_py.build_py.run(self, *args,
                                                          **kwargs)
        finally:
            print('Deleting:', filename)
            os.remove(filename)
            pass
        return ret


with open(os.path.join(os.path.dirname(__file__), 'VERSION')) as fin:
    version = fin.read().strip()


distutils.core.setup(name=PACKAGE_NAME,
                     version=version,
                     description='Do something.',
                     author='John Doe',
                     author_email='john.doe@example.com',
                     url='example.com',
                     cmdclass={'install_data':MyInstallData,
                               'build_py':MyBuildPy,
                               'install':MyInstall,
                               },
                     package_dir={PACKAGE_NAME:os.path.join('bin',PACKAGE_NAME),
                                  },
                     packages=[PACKAGE_NAME,
                               ],
                     scripts=[os.path.join('bin', 'script'),
                              ],
                     # Note: We can't use package_data for stuff in
                     #   share because relative paths don't play well
                     #   with it.
                     #package_data={PACKAGE_NAME:['test.dat']},
                     data_files=[(os.path.join('etc', PACKAGE_NAME),
                                  [os.path.join('etc', PACKAGE_NAME,
                                                'script_logging.conf'),
                                  ],
                              )],
                     )

