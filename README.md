# iEEE Conferences World Map
![IEEE Logo](http://www.ieee.org/ucm/groups/public/@ieee/@web/@org/@globals/documents/images/ieee_logo_mb_tagline.gif) Crawling the iEEE Conference Search and displays a map

## What is it for?

You can use the [iEEE Conference Search](http://www.ieee.org/conferences_events/conferences/search/index.html?KEYWORDS=&CONF_SRCH_RDO=conf_date&RANGE_FROM_DATE=2014-01-01&RANGE_TO_DATE=2014-12-31&REGION=ALL&COUNTRY=ALL&STATE=ALL&CITY=ALL&SPONSOR=ALL&RowsPerPage=1000&PageLinkNum=10&ActivePage=1&SORTORDER=desc&SORTFIELD=start_date) (Institute of Electrical and Electronics Engineers), but it is a list. I think it is much more interesting to see a map, where conferences happening.

![iEEE Conference World Map](https://github.com/balzer82/iEEEConferenceWorldMap/blob/master/iEEE-Conferences-2014-Worldmap.png?raw=true)


## How to use it?

``` python iEEECrawler.py ```

Probably it is better to use the .ipynb (iPython Notebook), because I am using it and probably I forgot to update the .py

## What is it doin'?

1. search iEEE Conference Database
2. extract all infos from website
3. ask Google for location of the adress (Geoencoding)
4. save [.kml file (for Google Earth)](https://raw.github.com/balzer82/iEEEConferenceWorldMap/master/iEEE-Conferences.kml)
5. create World map and Europe Map

![IEEE European Conferences](https://github.com/balzer82/iEEEConferenceWorldMap/blob/master/iEEE-Conferences-2014-Europe.png?raw=true)

## Dependencies

1. Matplotlib (for Rendering)
2. Basemap (for Map)
4. Requests (for URL requests)
5. BeatuifulSoup (for HTML parsing)
7. time (for timeout for Google API)
8. simplekml (for kml)
