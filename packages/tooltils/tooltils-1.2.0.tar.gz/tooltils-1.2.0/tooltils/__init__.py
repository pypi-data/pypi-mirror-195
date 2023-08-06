"""
# tooltils | v1.2.0
A lightweight python utility library built on standard modules

### Available classes:
- Errors (General errors for better information use)
- Files (Custom file method wrapper)
- JSON (Custom JSON method wrapper)
- Requests (Basic http access functions)
- Time (Time modifying and informative functions)
- Logging (Terminal modifiers)
- Wave (Custom WAVE file methods)
- String (Custom string modifying methods)
- Types (Custom type modifying and converting)
"""

__title__   : str = 'tooltils'
__author__  : str = 'feetbots'
__version__ : str = '1.2.0'
__license__ : str = 'MIT'

class bm:
    from datetime import datetime, timezone, timedelta
    from io import TextIOWrapper, UnsupportedOperation
    from time import time as ctime, localtime, sleep
    from json import dumps, load as jload, loads
    from urllib.request import urlopen, Request
    from json.decoder import JSONDecodeError
    from urllib.error import URLError
    from os.path import getsize
    from json import dumps
    from os import system


class errors:
    """
    General errors used for better information use
    
    ### Available Errors:
    - HTTPError > Unspecified http error
    - JSONDecoderError > Unable to parse JSON data
    """
    class HTTPError(Exception):
        """Unspecified http error"""
        def __init__(self, message=None, *args):
            self.message = message

        def __str__(self):
            if self.message:
                return self.message
            return 'HTTP connection failed'

    class JSONDecoderError(Exception):
        """Unable to decode JSON input"""
        def __init__(self, message=None, *args):
            self.message = message

        def __str__(self):
            if self.message:
                return self.message
            return 'Unable to decode JSON'

class files:
    """
    Custom file method wrapper
    
    ### Available Methods:
    - clear() > Clear a file while avoiding null character error
    """

    def clear(_file: bm.TextIOWrapper | str) -> None:
        """Clear a file using truncate"""

        if type(_file) is not bm.TextIOWrapper:
            with open(_file, 'r+') as _file:
                pass
        try:
            _file.seek(0)
            _file.truncate(0)
        except (bm.UnsupportedOperation, ValueError):
            raise bm.UnsupportedOperation('File is not writeable or has been closed')

class json:
    """
    Custom JSON method wrapper
    
    ### Available Methods:
    - sload() > Convert a string to valid JSON data
    - load() > Load JSON data from a file
    - set() > Set a key in a JSON file
    - add() > Add a key value pair to a JSON file
    - remove() > Remove a key value pair from a JSON file
    """

    def sload(_jdata: str) -> dict | list:
        """Convert a string to JSON data"""
        
        try:
            return bm.loads(str(_jdata))
        except bm.JSONDecodeError:
            raise errors.JSONDecoderError('JSON file was typed incorrectly or was dangerous')

    def load(_file: bm.TextIOWrapper) -> dict | list:
        """Load JSON data as a dictionary or list type"""

        if type(_file) is not bm.TextIOWrapper:
            with open(_file, 'r') as _file:
                pass
        elif _file.mode[0] == 'w':
            raise TypeError('Cannot read from file in write mode')
        try:
            return bm.jload(_file)
        except bm.JSONDecodeError:
            raise errors.JSONDecoderError('JSON file was typed incorrectly or was dangerous')

    def set(_file: bm.TextIOWrapper, _settings: dict) -> None:
        """Set a key value in a JSON file"""

        data: dict | list = json.load(_file)
        listdata: list = []

        if type(data) is dict:
            data.update(_settings)
            appljson: str = bm.dumps(data, indent=2)
        elif type(data) is list:
            for i in data:
                i.update(_settings)
                listdata.append(i)
            listdata.pop(-1)
            appljson: str = bm.dumps(listdata, indent=2)

        files.clear(_file)
        _file.write(appljson)
    
    def add(_file: bm.TextIOWrapper, _keys: dict) -> None:
        """Add a key value pair to a JSON file"""

        data: dict | list = json.load(_file)
        for i in _keys.keys():
            if type(data) is list:
                data.append({i: _keys[i]})
            else:
                data[i] = _keys[i]
        
        appljson: str = bm.dumps(data, indent=2)
        files.clear(_file)
        _file.write(appljson)

    def remove(_file: bm.TextIOWrapper, _key: str) -> None:
        """Remove a key value pair from a JSON file"""

        data: dict | list = json.load(_file)
        listdata: list = []
        if type(data) is dict:
            try:
                data.pop(_key)
            except KeyError:
                pass
            appljson = bm.dumps(data, indent=2)
        else:
            for i in data:
                try:
                    i.pop(_key)
                except KeyError:
                    pass
                listdata.append(i)
            appljson = bm.dumps(listdata, indent=2)
        files.clear(_file)
        _file.write(appljson)

class requests:
    """
    Basic http access functions
    
    ### Available Methods:
    - get() > Call a URL and return a class method
    - post() > POST JSON data to a URL and return a class method
    """

    def get(_url: str, _params: dict={}):
        """Call a URL and return a class method"""

        try:
            if not _url.startswith('https://') and not _url.startswith('http://'):
                _url = 'http://' + _url
            elif _url[-1] != '?':
                _url += '?'

            if _params != {}:
                for i in _params.keys():
                    if i + '=' not in _url:
                        _url += i + '=' + _params[i] + '&'

                data = bm.urlopen(_url[:-1])
            else:
                data = bm.urlopen(_url)
        except bm.URLError as err:
            raise errors.HTTPError(err)

        class response:
            code:   int = data.getcode()
            json:  dict = json.sload(data.read().decode())
            pretty: str = bm.dumps(json, indent=2)
            raw:  bytes = data.read()
            text:   str = data.read().decode()

        return response
    
    def post(_url: str, _params: dict={}):
        """Post dictionary data to a URL and return a class method"""

        if not _url.startswith('https://') and not _url.startswith('http://'):
            _url = 'http://' + _url
        
        try:
            req = bm.Request(_url, method='POST')
            if _params != {}:
                jdata: dict = bm.dumps(_params).encode()
                req.add_header('Content-Type', 'application/json')
                req.add_header('Content-Length', len(jdata))
            
            data = bm.urlopen(_url, data=jdata)
        except bm.URLError as err:
            raise errors.HTTPError(err)
        
        class response:
            code:   int = data.getcode()
            json:  dict = json.sload(data.read().decode())
            pretty: str = bm.dumps(json, indent=2)
            raw:  bytes = data.read()
            text:   str = data.read().decode()
        
        return response

class time:
    """
    Time modifying and informative functions
    
    ### Available Methods:
    - epoch() > Return epoch based off system clock
    - date() > Convert epoch to human readable date
    - sleep() > Block thread execution for specified time in ms
    """

    def epoch() -> float:
        """Return epoch based off system clock"""

        return bm.ctime()

    def date(_epoch: float | None=epoch(), _tz: str='local', _format: int=1) -> str:
        """
        Convert epoch to human formatted date
        
        ### Examples:
        - date() -> Local Timezone
        - date(_epoch=0) -> January 1st, 1970
        - date(_tz='-05:00') -> New York, USA
        - date(_tz='+11:00') -> Sydney, Australia
        """

        try:
            if _tz.lower() == 'local':
                sdate = bm.localtime(_epoch)
            elif _tz.startswith('+') or _tz.startswith('-'):
                try:
                    timezone = bm.timezone(bm.timedelta(
                            hours=int(_tz[:3]), minutes=int(_tz[4:])))
                    sdate = bm.datetime.fromtimestamp(_epoch, 
                            tz=timezone).timetuple()
                except (ValueError, IndexError):
                    raise TypeError('Timezone (\'{}\') not found'.format(_tz))
            else:
                raise TypeError('Timezone (\'{}\') not found'.format(_tz))
        except (OverflowError, TypeError) as err:
            if type(err) is OverflowError:
                raise TypeError('Epoch timestamp too large')
            else:
                raise TypeError('Unable to parse epoch timestamp')

        def fv(val: int) -> str:
            return val if val > 9 else f'0{val}'

        if _format == 1:
            return '{}-{}-{} {}:{}:{}'.format(sdate.tm_year,
                fv(sdate.tm_mon), fv(sdate.tm_mday), fv(sdate.tm_hour),
                fv(sdate.tm_min), fv(sdate.tm_sec))

        elif _format == 2:
            hour: int = sdate.tm_hour % 12 if sdate.tm_hour % 12 != 0 else 12
            mon: list = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
                        'August', 'September', 'October', 'November', 'December'][sdate.tm_mon - 1]
            end: list = ['th', 'st', 'nd', 'rd', 'th', 'th', 'th', 'th', 'th',
                        'th'][int(str(sdate.tm_mday)[-1])]
            if sdate.tm_mday in [11, 12, 13]:
                end: str = 'th'

            return '{}:{} {} on the {}{} of {}, {}'.format(hour, fv(sdate.tm_min), 
                   'PM' if sdate.tm_hour >= 12 else 'AM', sdate.tm_mday, end, mon, sdate.tm_year)
        else:
            raise TypeError('Format ({}) not found'.format(_format))

    def sleep(_ms: float) -> None:
        """Delay current thread execution for x amount of milliseconds"""

        bm.sleep(_ms / 1000)

class logging:
    """
    Terminal modifiers
    
    ### Available Methods:
    - colours > List of supported terminal colours
    - cvalues > List of corresponding colour values
    - ctext() > Return text in the specified colour
    - log() > Log text to the terminal
    """

    colours: list = ['pink', 'green', 'blue', 'yellow',
                     'red', 'white', 'cyan', 'gray', '']
    cvalues: list = ['35', '32', '34', '33',
                     '31', '38', '36', '30', '0']

    def ctext(_text: str='', _colour: str='', _bold: bool=False) -> str:
        """Return text in specified colour"""

        try:
            cvalue = logging.cvalues[logging.colours.index(_colour)]
        except ValueError:
            cvalue = _colour

        bm.system('')
        return '\u001b[{0}{1}{2}\u001b[0m'.format(cvalue, ';1m' if _bold else 'm', _text)

    def log(_header: str, _details: str, _type: int=1) -> None:
        """Log text to the terminal as an info, warning or error type"""

        try:
            data = [[logging.ctext('INFO', 'blue', True), '     '],
                    [logging.ctext('WARNING', 'yellow', True), '  '],
                    [logging.ctext('ERROR', 'red', True), '    ']][_type - 1]
        except IndexError:
            raise IndexError('Unknown type ({})'.format(_type))

        bm.system('')
        print('{0} {1}{2}{3} {4}'.format(logging.ctext(time.getdate(), 'gray', True), data[0], data[1],
                                         logging.ctext(_header, 'pink'), _details))

class wave:
    """
    Custom WAVE file methods
    
    ### Available Methods:
    - length() > Get the length of a wave file in seconds
    """

    def length(_file: bm.TextIOWrapper | str) -> float:
        """Return the length of a wave file in seconds"""

        _file: str = _file.name if type(_file) is bm.TextIOWrapper else _file
        with open(_file, encoding='latin-1') as _f:
            _f.seek(28)
            sdata: str = _f.read(4)
        rate: int = 0
        for i in range(4):
            rate += ord(sdata[i]) * pow(256, i)

        return round((bm.getsize(_file) - 44) * 1000 / rate / 1000, 2)

class string:
    """
    Custom string modifying methods
    
    ### Available Methods:
    - cstrip() > Caveman regex replacement
    - mreplace() > Replace multiple keywords in a string using a dict
    - cipher() > A simple caeser cipher
    - halve() > Halve a string and return halves as a list
    """

    def cstrip(_text: str, _chars: str) -> str:
        """Strip a string using a character list as a filter"""

        return [_text.replace(i, '') for i in _chars]

    def mreplace(_text: str, _chars: dict) -> str:
        """Multi replace words in a string using a dictionary"""

        return [_text.replace(i, _chars[i]) for i in _chars.keys()]

    def cipher(_text: str, _shift: int) -> str:
        """A simple caeser cipher utilising place shifting"""

        return ''.join([chr((ord(i) + _shift - (65 if i.isupper() else 97)) % 26 + (65 if i.isupper() else 97)) for i in _text])

    def halve(_text: str) -> list:
        """Halve text and return both halves as a list"""

        i: int = len(_text)
        if i % 2 == 0:
            return [_text[0: i // 2], _text[i // 2:]]
        else:
            return [_text[0:(i // 2 + 1)], _text[(i // 2 + 1):]]

class types:
    """
    Custom type modifying and converting
    
    ### Available Methods:
    - list() > Convert a dict or tuple to a list
    - tuple() > Convert a dict or list to a tuple
    - dict() > Convert a tuple or list to a dict
    - bool() > Return a bool from most standard data types
    """

    class list():
        """Convert a dictionary or tuple to a list"""

        def __new__(self, _list: dict | tuple) -> list:
            nlist: list = []

            if type(_list) is dict:
                for i in _list.keys():
                    nlist.append(i)
                    nlist.append(_list[i])
            elif type(_list) is tuple:
                for i in _list:
                    nlist.append(i)

            return nlist
    
    class tuple():
        """Convert a dictionary or list to a tuple"""

        def __new__(self, _tuple: dict | list) -> tuple:
            ntuple: tuple = ()

            if type(_tuple) is dict:
                for i in _tuple.keys():
                    ntuple += (i, _tuple[i])
            elif type(_tuple) is list:
                for i in _tuple:
                    ntuple += (i, '')
                    ntuple = ntuple[:-1]

            return ntuple
    
    class dict():
        """Convert a list or tuple to a dictionary"""
        
        def __new__(self, _dict: list | tuple) -> dict:
            ndict: dict = {}

            try:
                for i, item in enumerate(_dict, 0):
                    ndict[item] = _dict[i + 1]
            except IndexError:
                if len(_dict) % 2 != 0:
                    raise IndexError('Odd number of items in list')
                return ndict
    
    class bool():
        """Convert a list, tuple, string, integer or dictionary to a boolean"""
        
        def __new__(self, _bool: list | tuple | str | int | dict) -> bool:
            if type(_bool) is list or type(_bool) is tuple or type(_bool) is dict:
                if len(_bool) != 0:
                    return True
            elif type(_bool) is str:
                if _bool.lower() == 'true':
                    return True
                elif _bool.lower() == 'false':
                    return False
                elif len(_bool) != 0:
                    return True
            elif type(_bool) is int:
                if _bool != 0:
                    return True
                else:
                    return False

            return True
