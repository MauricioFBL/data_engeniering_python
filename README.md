# data_engeniering_python

## Description

This is a Data engineering pipeline prototype to extract data from notice 
sites then, tranform and aggregate different sources and finally load data
in a Bd
## Data Sources

The project consumes different notices sites at this moment scrape:
- https://elpais.com
- http://www.eluniversal.com.mx


## Development

Parameters needed for configuration are in the file config.yaml this file 
contains:

* **news_sites:**
  sitename:
    url: 
    queries:
      homepage_article_links: 
      article_body:
      article_title:


### Requirements and Installation

directories and file structure:
```
    LH4_AMPPS_DASH/
    |---extract/
          |---common.py
          |---config.yaml
          |---main.py
          |---news_page_objects.py
    |---transform/
          |---main.py
    |---load/
          |---article.py
          |---base.py
          |---main.py
    |---.gitignore
    |---README.md
    |---newspaper.db
    |---pipeline.py
```

It requires Python 3.6 or higher, check your Python version first.

The [requirements.txt](requirements.txt) should list and install all the required Python 
libraries that the pipeline depend on

`pip install -r requirements.txt`

To start scrapping the sitess, you have to execute [pipeline.py](pipeline.py) file:

`python pipeline.py `

This will run the ETL process, and write the output to the specified output
location.
