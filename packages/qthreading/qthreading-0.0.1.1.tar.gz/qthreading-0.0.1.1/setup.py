from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

with open('HISTORY.md') as history_file:
    HISTORY = history_file.read()

setup_args = dict(
    name='qthreading',
    version='0.0.1.1',
    description='balanced threadpool',
    long_description_content_type="text/markdown",
    long_description=README + '\n\n' + HISTORY,
    license='MIT',
    packages=find_packages(),
    author='laghmari khalil',
    author_email='laghmari.khalil@gmail.com',
    keywords=['thread', 'pool', 'balance'],
    #url='https://github.com/',
    #download_url='https://pypi.org/project/qthreading/'
)

install_requires = [
]

if __name__ == '__main__':
    setup(
		**setup_args, 
		install_requires=install_requires,
		include_package_data = True
	)