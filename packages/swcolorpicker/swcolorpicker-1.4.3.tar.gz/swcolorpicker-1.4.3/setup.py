from setuptools import setup

setup(
    name='swcolorpicker',
    version='1.4.3',
    description='Color picker component of smartwheel-core',
    long_description='Forked from https://github.com/nlfmt/pyqt-colorpicker',
    url='https://github.com/enaix/smartwheel-colorpicker',
    author='enaix',
    author_email='eanix@protonmail.com',
    license='MIT',
    packages=['swcolorpicker'],
    install_requires=['pyqt6'],
    keywords=["python", "color", "gui", "colorpicker", "visual"],

    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
)
