"""
libs.strings

By default, uses `en-gb.json` file inside the `strings` top-level folder.

If language changes, set `libs.strings.default_locale` and run `libs.strings.refresh()`.
"""
import json
from pathlib import Path

#now using this to handle all our error rresponse

default_locale = "en-gb"
cached_strings = {}


def refresh():
    global cached_strings
    try:
        relative = Path(f"api/strings/{default_locale}.json")
        json_file = relative.absolute()
        print("Refreshing...")
        
        with open(json_file) as f:
            cached_strings = json.load(f)
    except:
        print("Refreshing...")
        with open(f"strings/{default_locale}.json") as f:
            cached_strings = json.load(f)



def gettext(name):
    return cached_strings[name] 
    #this actually gets the name of stored in our json

#Cashing means temporarily storing a piece of data that is being used multiple times, so it doesn't need to be generated or retrieved many times

refresh() # the cached_strings wait for the refresh() to load the file before have it's json content
