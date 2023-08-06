from setuptools import find_packages, setup
setup(
    name='malsabbagh-checker-multiple-two',
    packages=find_packages(),
    version='0.2.0',
    description='Python links checker',
    author='Mohamed',
    license='MIT',
    # entry_points = {
    #     'console_scripts': [
    #         'command-name = checker.doc_as_code:main',
    #     ],              
    # },
    scripts=['scripts/doc-as-code']
    # install_requires=[],
    # setup_requires=['pytest-runner==6.0.0'],
    # tests_require=['pytest==7.2.1'],
    # test_suite='tests',
)
