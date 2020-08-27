# PAPER PUBLISHED

A web scrapper against Google to determine if a given paper's title has been published aka returns positive
search result from google (the title matches).

Will publish results to STDOUT as commaa seperated file (CSV).

----
## Installation

The following steps are for one-time only setup to install & run the program.

Create new virtual environment inside the working directory

```
python3 -m venv env
```

Activate the environment

```
source env/bin/activate
```

Install libraries

```
pip3 install -r requirements.txt
```

Testing
All unit tests can be found in ./tests/ and are [pytest](https://docs.pytest.org/en/latest/)
```
pytest
```

Linting
```
flake8 pp.py
```

Isort
For import module sorting
```
isort pp.py
```

Black
Code formatting
```
black pp.py
```

----

## Usage
The following will configure the environment, execute the program and deactivate accordingly.


Activate the virtual environment
```
source env/bin/activate
```

Execute Script
```
python3 pp.py [<input-file>|<paper-title>]
#     - input-file: XLS or CVS of papers' corresponding titles to search
#     - title: individual paper title (string) to search on

# run script and outputs to csv, top 10 search results from google with direct and partial fuzzy match scores
python3 pp.py "Curing Cancer with Bleach"

Paper ID, Paper Title, Search Title, Direct Match, Partial Match, Link
NA,"Curing Cancer with Bleanch","'Miracle' Solution for Cancer is Actually Bleach - Healthline",46.00,65.00,https://www.healthline.com/health-news/no-this-miracle-solution-isnt-a-cure-for-cancer-autism-its-bleach
NA,"Curing Cancer with Bleanch","Drinking Bleach Won't Cure Autism or Cancer, F.D.A. Says ...",33.00,46.00,https://www.nytimes.com/2019/08/13/health/drinking-bleach-autism-cancer.html
NA,"Curing Cancer with Bleanch","No, Drinking Bleach Does Not Cure Cancer - Cancer Health",41.00,58.00,https://www.cancerhealth.com/article/drinking-bleach-cure-cancer
NA,"Curing Cancer with Bleanch","Drinking bleach will not cure cancer or autism, FDA warns",39.00,46.00,https://www.nbcnews.com/health/health-news/drinking-bleach-will-not-cure-cancer-or-autism-fda-warns-n1041636
NA,"Curing Cancer with Bleanch","Group to tout bleach-based 'miracle cure' at upstate New York ...",22.00,38.00,https://www.theguardian.com/us-news/2019/aug/16/bleach-based-miracle-cure-group-seminar-new-york
NA,"Curing Cancer with Bleanch","Miracle Mineral Supplement - Wikipedia",31.00,38.00,https://en.wikipedia.org/wiki/Miracle_Mineral_Supplement
NA,"Curing Cancer with Bleanch","'Miracle Solution' Marketed As Treatment For Cancer and ...",31.00,46.00,https://www.newsweek.com/miracle-solution-marketed-treatment-cancer-autism-same-drinking-bleach-fda-says-1454147
NA,"Curing Cancer with Bleanch","Stop using 'Miracle' solution as a cure for autism or cancer ...",36.00,42.00,https://www.cnn.com/2019/08/15/health/bleach-miracle-cure-fda-warning/index.html
NA,"Curing Cancer with Bleanch","FDA issues warning not to drink bleach to cure cancer, autism",34.00,54.00,https://www.usatoday.com/story/news/health/2019/08/14/fda-issues-warning-not-drink-bleach-cure-cancer-autism/2008005001/
```

Deactivate the environment
```
deactivate
```

