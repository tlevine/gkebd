from distutils.core import setup

setup(name='gkebd',
      author='Thomas Levine',
      author_email='_@thomaslevine.com',
      description='Look for (illegal) third-party trackers on Swedish government websites.',
      url='https://dada.pink/gkebd/',
      packages=['gkebd'],
      install_requires = [],
      version='0.0.2',
      license='AGPL',
      entry_points = {'console_scripts': ['gkebd = gkebd.main:cli']},
)
