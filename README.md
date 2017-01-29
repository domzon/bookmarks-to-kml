# Export Google Maps Saved Places as KML

This is a neat little tool to export your saved places from Google Maps as KML. I myself (@heyarne) did almost nothing. All the credit goes to @endolith and @ngzhian. I just added a requirements.txt and used the most up to date version.

## Manual

1. Go to Google Bookmarks: https://www.google.com/bookmarks/
2. On the bottom left, click "Export bookmarks": https://www.google.com/bookmarks/bookmarks.html?hl=en
3. Install script dependencies `pip install -r requirements.txt`
4. After downloading the html file, run this script on it to generate a KML file per bookmark label: `python bookmarkstokml.py GoogleBookmarks.html` 

## Disclaimer

It's hacky and doesn't work on all of them, but it kinda works.  
Tested with bookmarks exported on January 29, 2017 and python version 3.5.2.
