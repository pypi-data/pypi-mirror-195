import setuptools

requirements = ['aiotoolbox']

setuptools.setup(
	name = 'asyncio-proxy',

    packages = ['asyncio-proxy'],

	version = '1.2.0',

	author = 'Joongi Kim',
    
	license = 'apache2',

	author_email = 'me@daybreaker.info',

	description = 'Full-featured proxy connector for aiohttp',

	long_description = open('README.md').read(),

	long_description_content_type = 'text/markdown',

	url = 'https://github.com/Skactor/aiohttp-proxy',

	install_requires = requirements,

	classifiers=[
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'License :: OSI Approved :: Apache Software License'
	],

	python_requires='>=3.7, <=3.10',
)