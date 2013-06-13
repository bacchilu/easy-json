# Overview

I implemented, as an exercise a simple JSON parser: given a JSON string, a Python data structure (object or list) is returned. According to json.org.

Usage:


    import easyjson
    
    
    json = \
        u'{"Luca\\n": "A\\u1234B", "luca": {}, "a": true, "False": false, "null": null, "lica": ["Luca", {}], "1": 12.4e-2}'
    
    print loads(json)