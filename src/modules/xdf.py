'''
MIT License
Copyright (c) 2019 Keith Christopher Cronin
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

_parseddictionary = {}
_hasreadxdf = False
debug = False

def readxdf(data, markercharacter='@'):
        global _hasreadxdf
        isonproperty = False
        isonpropertyvalue = False
        isonequal = False
        isonmarker = True
        position = 0
        propertyvaluebuffer = []
        propertybuffer = []
        global _parseddictionary
        propertystartindex = 0
        propertyendindex = 0
        propertyvaluestartindex = 0
        propertyvalueendindex = 0
        propwasmarked = False
        propvaluewasmarked = False
        propertyname = ''
        if len(data) == 0:
                return False
        if data[0] != markercharacter or _hasreadxdf or len(markercharacter) > 1:
                return False
        else:
                for character in data:
                        if isonproperty:
                                if propwasmarked == False:
                                        propertystartindex = position
                                        propwasmarked = True
                                else:
                                        pass

                        if character == '=':
                                        isonpropertyvalue = True
                                        propertyendindex = position
                                        propertyname = data[propertystartindex:propertyendindex].strip('\n')
                                        propertyvaluestartindex = position + 1

                        if isonpropertyvalue:
                                if character == markercharacter or position == len(data)-1:
                                        isonmarker = True
                                        propertyvalueendindex = position
                                        _parseddictionary[propertyname] = data[propertyvaluestartindex:propertyvalueendindex].strip('\n')
                                        propwasmarked = False
                                else:
                                        pass

                        if isonmarker:
                                isonproperty = True
                                isonmarker = False
                        position += 1
                _hasreadxdf = True
                return True
                
def reset():
        global debug
        _hasreadxdf = False
        _parseddictionary.clear()
        if debug:
                _tellcurrentparserdictionary()
        return True
        
def getproperty(propertystring):
        if propertystring in _parseddictionary:
                return _parseddictionary[propertystring]
        else:
                return False

def setproperty(propertystring, propertyvalue):
        _parseddictionary[propertystring] = propertyvalue
        return True

def writexdf(filepath, propertydictionary, markercharacter='@'):
        try:
                file = open(filepath,'w')                        
                for key in propertydictionary:
                        file.write(markercharacter+key+'='+str(propertydictionary[key])+"\n")
                file.close()
                return True
        except PermissionError:
                return False
        except OSError:
                return False

def _tellcurrentparserdictionary():
        print(F"Listing {len(_parseddictionary)} properties and values in memory: \n{_parseddictionary}")
