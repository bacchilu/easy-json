# Overview

I implemented, as an exercise a simple JSON parser: given a JSON unicode string, a Python data structure (object or list) is returned. According to json.org. The input JSON is expected to be a unicode string.

Usage:


    import easyjson
    
    
    json = \
        u'{"Luca\\n": "A\\u1234B", "luca": {}, "a": true, "False": false, "null": null, "lica": ["Luca", {}], "1": 12.4e-2}'
    
    print easyjson.loads(json)

The "pyEncode" utility is useful to encode all unicode strings in the returned data structure (also keys in the dicts) in byte strings in the desired encoding

	d = {u'Hello World': [1, u'due', {u'tre': null}]}
    print easyjson.pyEncode(d, 'utf-8')