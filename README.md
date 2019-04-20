# DatasetScraper
Tool to create image datasets for machine learning problems by scraping search engines like Google, Bing and Baidu.

# Features:
- **Search engine support**: Google, Bing, Baidu. (in-production): Yahoo, Yandex, Duckduckgo
- **Image format support**: jpg, png, svg, gif, jpeg
- Fast multiprocessing enabled scraper
- Very fast multithreaded downloader
- Data verification after download for assertion of image files

# Installation
`pip install datasetscraper`
Alternatively, you can clone this repository:


# About
- `Scraper.Scraper()`
  - creates a scraper object which can be used to scrape URLs from search engines and later download them.
  - `Scraper.Scraper(logLevel = logging.WARNING, headless=True)` are the defaults.
      - headless: If False then you can see the actual pypeeter browser
      - logLevel: Simple python logger level

- `fetch_urls()`
  - To fetch image URLs
  - `fetch_urls(query, engine='google', maxlist=[200])`
      - query: Search query
      - engine: search engine or list of search engines
      - maxlist: Maximum number of images to download. If multiple search engines exist then this needs to be a list specifying maximum number of images to fetch from each engine.

- download
  - To download the fetched URLs into a directory
  - download(urls, directory='images/',
                formats=['jpg', 'png', 'jpeg'], default='jpg',
                nworkers=10, timeout=30)
      - urls: List of urls
      - directory: Place on disk where downloaded images are stored
      - formats: List of file formats to dwonload
      - nworkers: Number of threads for multithreaded download
      - timeout: maximum time before which the download is cancelled

# Usage:
- Import
`from datasetscraper import Scraper`

- Defaults
```python
obj = Scraper.Scraper()
urls = obj.fetch_urls('kiniro mosaic')
obj.download(urls, directory='kiniro_mosaic/')
```

- Specify a search engine
```python
obj = Scraper.Scraper()
urls = obj.fetch_urls('kiniro mosaic', engine=['google'])
obj.download(urls, directory='kiniro_mosaic/')
```

- Specify a list of search engines
```python
obj = Scraper.Scraper()
urls = obj.fetch_urls('kiniro mosaic', engine=['google', 'bing'])
obj.download(urls, directory='kiniro_mosaic/')
```

- Specify max images (default was 200)
```python
obj = Scraper.Scraper()
urls = obj.fetch_urls('kiniro mosaic', engine=['google', 'bing'], maxlist=[500, 300])
obj.download(urls, directory='kiniro_mosaic/')
```

# FAQs
- Why aren't yandex, yahoo, duckduckgo and other search engines supported?
They are hard to scrape, I am working on them and will update as soon as I can.

- I set maxlist=[500] why are only (x<500) images downloaded?
There can be several reasons for this:
    - Search ran out: This happens very often, google/bing might not have enough images for your query
    - Slow internet: Increase the timeout (default is 60 seconds) as follows: ```obj.download(urls, directory='kiniro_mosaic/', timeout=100)```

- How to debug?
You can change the logging level while making the scraper object : `obj = Scraper(logger.INFO)`

# TODO:
- More search engines
- Better debug
- Write documentation
- Text data? Audio data?

# Blach hole chan kawaii
![](https://i.imgur.com/6OIxoup.jpg)
