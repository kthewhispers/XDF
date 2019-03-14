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

def readxdf(filepath, data=None, markercharacter='@', listseparatormarker=','):
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
        lastlistsepposition = 0
        haslist = False
        propertyvaluelistbuffer = []

        if filepath is not None:
                try:
                        file = open(filepath, 'r')
                        data = file.read()
                        file.close()
                except PermissionError:
                        return False
                except OSError:
                        return False

        if len(data) == 0:
                return False
        if data[0] != markercharacter or _hasreadxdf or len(markercharacter) != 1:
                return False
        else:
                for character in data:
                        if isonproperty:
                                if propwasmarked == False:
                                        propertystartindex = position
                                        propwasmarked = True
                                elif character == listseparatormarker:
                                        return False
                                else:
                                        pass
                                        
                        if character == '=':
                                        isonpropertyvalue = True
                                        isonproperty = False
                                        propertyendindex = position
                                        propertyname = data[propertystartindex:propertyendindex].strip('\n')
                                        propertyvaluestartindex = position + 1

                        if isonpropertyvalue:
                                if character == markercharacter or position == len(data)-1 and not haslist:
                                        isonmarker = True
                                        propertyvalueendindex = position
                                        _parseddictionary[propertyname] = data[propertyvaluestartindex:propertyvalueendindex].strip('\n')
                                        propwasmarked = False

                                if position == len(data)-1 and not haslist:
                                        _parseddictionary[propertyname] = data[propertyvaluestartindex:propertyvalueendindex+1].strip('\n')

                                elif character == listseparatormarker and not haslist:
                                        haslist = True
                                        propertyvaluelistbuffer.append(data[propertyendindex+1:position].strip(F"{listseparatormarker}\n"))
                                        lastlistsepposition = position

                                elif character == listseparatormarker and haslist:
                                        propertyvaluelistbuffer.append(data[lastlistsepposition+1:position].strip(F"{listseparatormarker}\n"))
                                        lastlistsepposition = position

                                if haslist and position == len(data)-1:
                                        propertyvaluelistbuffer.append(data[lastlistsepposition+1:position+1].strip(F"{listseparatormarker}\n"))
                                        _parseddictionary[propertyname] = propertyvaluelistbuffer
                                        propertyvaluelistbuffer = []
                                        lastlistsepposition = 0
                                        haslist = False

                                if character == markercharacter and haslist:
                                        propertyvaluelistbuffer.append(data[lastlistsepposition+1:position].strip(F"{listseparatormarker}\n"))
                                        _parseddictionary[propertyname] = propertyvaluelistbuffer
                                        propertyvaluelistbuffer = []
                                        lastlistsepposition = 0
                                        haslist = False

                                else:
                                        pass

                        if isonmarker:
                                isonproperty = True
                                isonmarker = False
                        position += 1
                _hasreadxdf = True
                _tellcurrentparserdictionary()
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

def appendtoproperty(propertystring, propertyvalue):
        if propertystring in _parseddictionary:
                _parseddictionary[propertystring] += F",{propertyvalue}"
                return True
        else:
                return False

def writexdf(filepath, propertydictionary, markercharacter='@', listseparatormarker=','):
        if markercharacter == listseparatormarker:
                return False
        listelementcounter = 0
        try:
                file = open(filepath,'w')                        
                for key in propertydictionary:
                        if isinstance(propertydictionary[key], list):
                                file.write(markercharacter+key+'=')
                                for element in propertydictionary[key]:
                                        if listelementcounter != len(propertydictionary[key]) - 1:
                                                file.write(element+listseparatormarker)
                                        else:
                                                file.write(element+'\n')
                                        listelementcounter += 1
                                listelementcounter = 0
                        else:
                                file.write(markercharacter+key+'='+str(propertydictionary[key])+'\n')
                file.close()
                return True
        except PermissionError:
                return False
        except OSError:
                return False
        
def getcurrentdata():
        if len(_parseddictionary) < 1:
                return False
        else:
                return _parseddictionary
        
def _tellcurrentparserdictionary():
        print(F"Listing {len(_parseddictionary)} properties and values in memory: \n{_parseddictionary}")
