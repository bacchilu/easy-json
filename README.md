# EasyJson.py

I implemented, as an exercise a simple JSON parser: given a JSON unicode string, a Python data structure (object or list) is returned. According to json.org. The input JSON is expected to be a unicode string.

It runs on Python 2.4 or newer.

Usage:


    import easyjson
    
    
    json = \
        u'{"Luca\\n": "A\\u1234B", "luca": {}, "a": true, "False": false, "null": null, "lica": ["Luca", {}], "1": 12.4e-2}'
    
    print easyjson.loads(json)

It is also possible using the "loads" function with a file object. In this case you have to pass an encoding argument. The default is utf-8.

    with open('stream.json') as fp:
        print easyjson.loads(fp, 'utf-8')

Also a "dumps" function has been implemented: a Python dict or list is required as an argument. All values (see json.org for the meaning of value) are intended to be unicode types. See the utility "pyDecode" if you need to convert a Python dict or list to correct format.
Al decimal.Decimal, float and int types are interpreted as JSON number type.

The "pyEncode" utility is useful to encode all unicode strings in the returned data structure (also keys in the dicts) in byte strings in the desired encoding

	d = {u'Hello World': [1, u'due', {u'tre': null}]}
    print easyjson.pyEncode(d, 'utf-8')

"pyDecode" usage:

    d = {'Luca': [2, 'Bacchi']}
    print easyjson.pyDecode(d, 'utf-8')
    
    > {u'Luca': [2, u'Bacchi']}