import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup_requires = [
    'pytest_runner',
    ]

install_requires = [
    'setuptools',
    ]

tests_require = [
    'pytest',
    'pytest-cov',
    ]

docs_require = [
    'Sphinx',
    'sphinx_rtd_theme',
    ]

setup(
    name="pyjamendo",
    version="0.2.dev0",
    author="Uli Fouquet",
    author_email="uli@gnufix.de",
    description=(
        "Build m3u lists for streaming jamando.com internet radio stations."),
    license="MIT",
    keywords="jamendo internetradio m3u extm3u",
    url="https://github.com/ulif/pyjamendo/",
    py_modules=['pyjamendo'],
    packages=[],
    namespace_packages=[],
    long_description=read('README.rst') + '\n\n\n' + read('CHANGES.rst'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
    include_package_data=True,
    zip_safe=False,
    setup_requires=setup_requires,
    install_requires=install_requires,
    tests_require=tests_require,
    extras_require=dict(
        tests=tests_require,
        docs=docs_require,
        ),
    entry_points={
    },
)
