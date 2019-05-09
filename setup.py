from setuptools import setup

setup(
    name='planforge-server',
    version='0.1',
    description='',
    url='http://github.com/planforge/planforge-python-server',
    author='Hunter Clarke',
    author_email='hunter@planforge.io',
    license='MIT',
    packages=['planforge'],
    install_requires=[
        'requests',
    ],
    zip_safe=False
)
