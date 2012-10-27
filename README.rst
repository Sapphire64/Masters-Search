Masters-Search
==============
Search system for *DonNTU* masters with cool Bootstrap interface which counts number of found results for provided keywords in search systems.

Is used in *Donetsk National Technical University* to track changes in masters' theses popularity.

Each student adds up to 25 keywords into form and then this app makes table with the results. Up to 25 search keywords per day for each IP.

Requirements
==============
- Python 2.7 with Twisted
- MongoDB and pymongo
- Update project patterns in `App/core/PagesDownloader.py` for your search systems and engines

Problems
==============
1. Legal problems - not all search systems allows you to parse their search results. In case of Yandex we are using Yandex XML service with their api.
2. Search patterns can become outdated too soon, so you should verify them more often.

Project Status
==============
This project was written in May 2012 and mostly not maintained anymore, but I accept patches and I can help with any questions. 

I moved this project to GitHub so DonNTU masters can use it at localhost for their Master project website ("Internet-technologies" course on the 5th year of education). 

Also visit my page on `DonNTU Master's website <http://masters.donntu.edu.ua/2012/fknt/vlasenko/ind/index.htm>`_ for additional useful scripts if you are studying in DonNTU.