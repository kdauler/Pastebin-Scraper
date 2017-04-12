Pastebin-Scraper (OSX fork)
================

Monitors pastebin.com for a specified set of keywords.

Usage
=====

Copy pastebin.py to the location of your choice. Make a file called 'keywords.txt' in the same directory. When a paste contains a word from the keyword.txt file, the paste will be saved in a 'Pastebin' folder within date sorted folders.
- pastebin.py
- keywords.txt
- Pastebin
	- Year
		- Month
			- Day
				- date_pasteID_matchedKeywords.txt
				- date_pasteID_matchedKeywords.txt
				- date_pasteID_matchedKeywords.txt

Dependencies
============

This was forked from https://github.com/cloughrm/Pastebin-Scraper which was developed to run on Windows 7. This version was modified to work on OSX and requires TOR (`brew install tor`) and pysocks ('pip install pysocks'). 

If brew automatically sets tor as a autorun service (check with `brew services list`) this could cause issues as tor initiated with this script will not be able to bind to :9050 because brew always beats it to the punch. You can fix this with `brew services stop tor`. 
