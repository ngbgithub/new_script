#!/usr/bin/env python3

import distutils.core, \
    distutils.command.install_scripts, \
    distutils.command.install_data
import os, sys


class MyInstallData(distutils.command.install_data.install_data):
    def run(self, *args, **kwargs):
        '''Create a directory for log files.
        '''
        os.makedirs(os.path.join(self.install_dir, 'var', 'log'),
                    exist_ok=True)

        return super().run(*args, **kwargs)


class MyInstallScripts(distutils.command.install_scripts.install_scripts):
    def run(self, *args, **kwargs):
        '''Change the main script's name after installation.
        '''
        import os.path

        rc = super().run(*args, **kwargs)

        fnames = [('new_script.py', 'new_script'),]
        for script in self.get_outputs():
            for srcbase,targetbase in fnames:
                dir,basename = os.path.split(script)
                if basename==srcbase:
                    target=os.path.join(dir, targetbase)
                    print('renaming {script} to {target}'
                          ''.format(script=script, target=target))
                    os.rename(script, target)

        return rc


distutils.core.setup(name='new_script',
                     version='000.000.001',
                     description='This script does X',
                     author='John Doe',
                     author_email='john.doe@example.com',
                     url='example.com',
                     cmdclass={'install_scripts': MyInstallScripts,
                               'install_data': MyInstallData,
                               },
                     package_dir={'new_script':'bin/new_script',
                                  },
                     packages=['new_script',
                               ],
                     scripts=['bin/new_script.py'],
                     # Note: We can't use package_data for stuff in
                     #   share because relative paths don't play well
                     #   with it.
                     #package_data={'new_script':['test.dat']},
                     data_files=[('etc/new_script',
                                  ['etc/new_script/logging.conf']
                                  ),
                                 ],
                     )

