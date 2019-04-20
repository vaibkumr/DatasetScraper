import setuptools

# reqs = (line.strip() for line in open("requirements.txt"))
LONG_DESC = open('README.md').read()
setuptools.setup(
    name="datasetscraper",
    version="0.0.4",
    author="Time Traveller",
    author_email="time.traveller.san@gmail.com",
    keywords = ['dataset_scraper', 'machine learning', 'dataset', 'images', 'scrape',
                'yandex', 'google', 'bing', 'baidu'],
    description="Tool to create image datasets for machine learning problems\
by scraping search engines like Google, Bing and Baidu. ",
    long_description=LONG_DESC,
    long_description_content_type="text/markdown",
    url="https://github.com/TimeTraveller-San/datasetscraper",
    license="GPLv2",
    packages=setuptools.find_packages(),
    install_requires=[
                'pyppeteer>=0.0.25',
                'fastprogress>=0.1.21',
                'requests>=2.19.1',
    ],
    python_requires='>=3',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: POSIX :: Linux",
    ],
)
