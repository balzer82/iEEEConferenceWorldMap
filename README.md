# iEEE Conferences World Map
Crawling the iEEE Conference Search and displays a map

## What is it for?

You can [http://www.ieee.org/conferences_events/conferences/search/index.html?KEYWORDS=&CONF_SRCH_RDO=conf_date&RANGE_FROM_DATE=2014-01-01&RANGE_TO_DATE=2014-12-31&REGION=ALL&COUNTRY=ALL&STATE=ALL&CITY=ALL&SPONSOR=ALL&RowsPerPage=1000&PageLinkNum=10&ActivePage=1&SORTORDER=desc&SORTFIELD=start_date](search the IEEE) (Institute of Electrical and Electronics Engineers) Conference Database, but it is a list. I think it is much more interesting to see a map, where conferences happening.



## How to use it?

   python iEEECrawler.py

## What is it doin'?

1 search iEEE Conference Database
2 extract all infos from every conference
3 ask Google for location of the adress (Geoencoding)
4 save .kml file (for Google Earth)
5 create World map and Europe Map
