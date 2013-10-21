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

# Date and Time management

JSON format doesn't have a date/time data format: you have to manage your particular situation by hand.
It could be useful to configure the parser in way that when dates or times are recognized, Python datetime values are returned.

Of course we are talking about "values". The meaning of "value" is that defined in json.org. So you could recognize a date/time value inside a "list" or in the right part of a key/value object.

For this porpouse we can pass to the "loads" function an optional argument, a callback to be called every time a "value" is recognized in the ast (abstract syntax tree). The callback function takes 2 arguments: the key (or None if value has been recognized inside a list) and the value itself. The value return by the callback is used.

Example:

    def dateParser(k, v):
        import datetime

        if k == u'compleanno':
            assert isinstance(v, decimal.Decimal)
            return datetime.datetime.fromtimestamp(int(v))

        if not isinstance(v, unicode):
            return v
        try:
            return datetime.datetime.strptime(v, u'%d/%m/%Y')
        except ValueError:
            return v


    loads(json, valueCb=dateParser)


In this example every value is passed to the dateParser callback.
If the key is "compleanno", we assume the json data contains a unix timestamp and we require this to be translate in a Python Datetime.
Also we check if a particular unicode value is in the form "day/month/year". Also in this case we result a Datetime value.
In every other case, the original value is returned: nothing is done.

# License

This software is distributed under the terms of the MIT license.