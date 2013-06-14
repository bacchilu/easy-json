#!/usr/bin/python
# -*- coding: utf-8 -*-

import decimal


class JsonParserException(Exception):

    pass


class Tokenizer(object):

    def __init__(self, s):
        self.content = (c for c in s if not c.isspace())
        self.current = None

    def assertValues(self, values):
        if self.current not in values:
            raise JsonParserException(u'%s not in %s' % (self.current,
                    values))

    def isEnd(self):
        if self.current is not None:
            raise JsonParserException('Wrong character at EOF')

    def next(self):
        try:
            self.current = self.content.next()
        except StopIteration:
            self.current = None
        return self.current


class JsonParser(object):

    def __init__(self, s):
        self.tokenizer = Tokenizer(s)

    def parse(self):
        self.tokenizer.next()
        ft = {u'{': self.parseObject, u'[': self.parseArray}
        try:
            ret = ft[self.tokenizer.current]()
            self.tokenizer.isEnd()
            return ret
        except KeyError:
            raise JsonParserException(u'Parsing error')

    def parseObject(self):
        ret = {}
        self.tokenizer.assertValues(u'{')
        if self.tokenizer.next() == u'"':
            while True:
                k = self.parseString()
                self.tokenizer.assertValues(u':')
                self.tokenizer.next()
                v = self.parseValue()
                ret[k] = v
                if self.tokenizer.current == u',':
                    self.tokenizer.next()
                    continue
                else:
                    break
        self.tokenizer.assertValues(u'}')
        self.tokenizer.next()
        return ret

    def parseArray(self):
        ret = []
        self.tokenizer.assertValues(u'[')
        if self.tokenizer.next() != u']':
            while True:
                ret.append(self.parseValue())
                if self.tokenizer.current == u',':
                    self.tokenizer.next()
                    continue
                else:
                    break
        self.tokenizer.assertValues(u']')
        self.tokenizer.next()
        return ret

    def parseString(self):
        ret = u''
        self.tokenizer.assertValues(u'"')
        while True:
            self.tokenizer.next()
            if self.tokenizer.current == u'"':
                break
            elif self.tokenizer.current == u'\\':
                self.tokenizer.next()
                if self.tokenizer.current == u'u':
                    exValue = 0
                    for i in range(4):
                        self.tokenizer.next()
                        self.tokenizer.assertValues(u'0123456789abcdefABCDEF'
                                )
                        exValue *= 16
                        exValue += int(self.tokenizer.current, 16)
                    ret += unichr(exValue)
                else:
                    c = {
                        u'"': u'"',
                        u'\\': u'\\',
                        u'/': u'/',
                        u'b': u'\b',
                        u'f': u'\f',
                        u'n': u'\n',
                        u'r': u'\r',
                        u't': u'\t',
                        }
                    try:
                        ret += c[self.tokenizer.current]
                    except KeyError:
                        raise JsonParserException(u'Wrong control character'
                                )
            elif ord(self.tokenizer.current) >= 32:
                ret += self.tokenizer.current
            else:
                raise JsonParserException(u'Wrong character in string')
        self.tokenizer.assertValues(u'"')
        self.tokenizer.next()
        return ret

    def parseValue(self):
        if self.tokenizer.current.isdigit():
            return self.parseNumber()
        d = {
            u'-': self.parseNumber,
            u'"': self.parseString,
            u'{': self.parseObject,
            u'[': self.parseArray,
            u't': self.parseTrue,
            u'f': self.parseFalse,
            u'n': self.parseNull,
            }
        try:
            return d[self.tokenizer.current]()
        except KeyError:
            raise JsonParserException(u'Wrong character in value')

    def parseTrue(self):
        self.tokenizer.assertValues(u't')
        self.tokenizer.next()
        self.tokenizer.assertValues(u'r')
        self.tokenizer.next()
        self.tokenizer.assertValues(u'u')
        self.tokenizer.next()
        self.tokenizer.assertValues(u'e')
        self.tokenizer.next()
        return True

    def parseFalse(self):
        self.tokenizer.assertValues(u'f')
        self.tokenizer.next()
        self.tokenizer.assertValues(u'a')
        self.tokenizer.next()
        self.tokenizer.assertValues(u'l')
        self.tokenizer.next()
        self.tokenizer.assertValues(u's')
        self.tokenizer.next()
        self.tokenizer.assertValues(u'e')
        self.tokenizer.next()
        return False

    def parseNull(self):
        self.tokenizer.assertValues(u'n')
        self.tokenizer.next()
        self.tokenizer.assertValues(u'u')
        self.tokenizer.next()
        self.tokenizer.assertValues(u'l')
        self.tokenizer.next()
        self.tokenizer.assertValues(u'l')
        self.tokenizer.next()
        return None

    def parseNumber(self):
        ret = decimal.Decimal(0)
        sign = 1
        self.tokenizer.assertValues(u'-0123456789')
        if self.tokenizer.current == u'-':
            sign = -1
            self.tokenizer.next()
        if self.tokenizer.current == u'0':
            self.tokenizer.next()
        else:
            self.tokenizer.assertValues(u'123456789')
            ret = decimal.Decimal(int(self.tokenizer.current))
            while self.tokenizer.next().isdigit():
                ret *= 10
                ret += int(self.tokenizer.current)
        assert not self.tokenizer.current.isdigit()
        if self.tokenizer.current == u'.':
            self.tokenizer.next()
            self.tokenizer.assertValues(u'0123456789')
            fraction = decimal.Decimal(10)
            while self.tokenizer.current.isdigit():
                ret += decimal.Decimal(self.tokenizer.current) \
                    / fraction
                fraction *= 10
                self.tokenizer.next()
        if self.tokenizer.current in (u'e', u'E'):
            eSign = 1
            self.tokenizer.next()
            if self.tokenizer.current == u'+':
                eSign = 1
                self.tokenizer.next()
            elif self.tokenizer.current == u'-':
                eSign = -1
                self.tokenizer.next()
            self.tokenizer.assertValues(u'0123456789')
            exp = decimal.Decimal(int(self.tokenizer.current))
            while self.tokenizer.next().isdigit():
                exp *= 10
                exp += int(self.tokenizer.current)
            ret = ret * 10 ** (exp * eSign)
        return ret * sign


def loads(json):
    return JsonParser(json).parse()


def pyEncode(elem, encoding):
    if isinstance(elem, dict):
        return dict((pyEncode(k, encoding), pyEncode(v, encoding))
                    for (k, v) in elem.iteritems())
    if isinstance(elem, list):
        return [pyEncode(e, encoding) for e in elem]
    if isinstance(elem, unicode):
        return elem.encode(encoding)
    return elem


class JsonVisitor(object):

    def __init__(self):
        self.resultString = u''

    def dumps(self, pyJson):
        if isinstance(pyJson, dict):
            return self.dumpDict(pyJson)
        if isinstance(pyJson, list):
            return self.dumpList(pyJson)
        raise JsonParserException('Wrong Python argument')

    def dumpDict(self, pyJson):
        assert isinstance(pyJson, dict)
        resultString = u'{'
        for (k, v) in pyJson.iteritems():
            resultString += u', '.join(self.dumpString(k) + u': '
                    + self.dumpValue(v) for (k, v) in
                    pyJson.iteritems())
        resultString += u'}'
        return resultString

    def dumpList(self, pyJson):
        assert isinstance(pyJson, list)
        resultString = u'['
        resultString += u', '.join(self.dumpValue(e) for e in pyJson)
        resultString += u']'
        return resultString

    def dumpString(self, pyJson):
        assert isinstance(pyJson, unicode)
        resultString = u'"'
        for c in pyJson:
            if c == u'"':
                resultString += u'\\"'
            elif c == u'\\':
                resultString += u'\\\\'
            elif c == u'/':
                resultString += u'\\/'
            else:
                resultString += c
        resultString += u'"'
        return resultString

    def dumpValue(self, pyJson):
        return u'value'


if __name__ == '__main__':
    json = \
        u'{"Luca\\n": "A\\u1234B", "luca": {}, "a": true, "False": false, "null": null, "lica": ["Luca", {}], "1": 12.4e-2}'

    pyJson = loads(json)

    import pprint

    pprint.pprint(pyJson)

    pprint.pprint(pyEncode(pyJson, 'utf-8'))

    print JsonVisitor().dumps(pyJson)
