from __future__ import print_function
import urllib
import urllib.request
import urllib.parse
import json
import builtins as __builtin__

def print(*args, **kwargs):
    for item in args:
        if isinstance(item, str):
            if "ve/BA" in item:
                raise CoreModDownloadCurseForgeTaskCheckError("")
        else:
            continue
        
    return __builtin__.print(*args, **kwargs)

class requests(object):
    def __init__(self):
        pass

    def get(self, url, params, headers):
        if params:
            if headers:
                url = url+"?"+urllib.parse.urlencode(params)
                self.request = urllib.request.Request(url=url,headers=headers,method='GET')
                self.response = urllib.request.urlopen(self.request)
                return self.response
            else:
                url = url + "?" + urllib.parse.urlencode(params)
                self.request = urllib.request.Request(url=url,method='GET')
                self.response = urlib.request.urlopen(self.request)
                return self.response
        else:     
            self.response = urlib.request.urlopen(url)
            return self.response
        
    def post(self, url, params="", headers=""):
        if params:
            if headers:
                data = bytes(urllib.parse.urlencode(params),encoding='utf-8')
                self.request = urllib.request.Request(url=url,data=data,headers=headers,method='POST')
                self.response = urllib.request.urlopen(self.request)
                return self.response
            else:
                data = bytes(urllib.parse.urlencode(params),encoding='utf-8')
                self.request = urllib.request.Request(url=url,data=data,method='POST')
                self.response = urllib.request.urlopen(self.request)
                return self.response
        else:     
            self.response = urllib.request.urlopen(url)
            return self.response
    def status(self):
        return self.response.status()

    def text(self):
        return self.response.read()

    def json(self):
        return json.loads(self.response.read())
    
requests = requests()


def mod_search(mod_name: str):
    requests.post("https://api.smdc.ljsdwz.cn/api/curseforge/api_key", params={'hash':"Mp9eV0n3RQzqncq3je5W8n50Bg56iy+HANReTFcWSaEsjplOeOxYGSlR5sNT93QityTM/mC7+68vsCMD7qva9L6UrjOHp6RaDg80L6l4UFk+iL8Q+cejShwdmW4JGoTWVANmH6SPS0610Y7zy5DCBJSmpBdRZLnYgoItaYCWKJ3ilO3XrwZJFWxFcW0Iq+pVYi6aldgfI1sCdV7AUN8EW3thICLtzAURkKNSlw5QZBvfMjxhWUykPg9b4dAtBnO1jeEWTvbzg1dWjl4whUFeM4pzAsKHLoyUwP58+n3JIkoatm7S5Jrxhc88QCzjVuNFRjeDhptezQMwblI0YTPeitZWf4DOfSNb6uB7jAVQhTibJeV7jLs6NjoJGnFPFrv41TockwKsEN+oDzp3E4SyWv7KQY+IevBbQGGU1Jf2eYp1oHK79eRsDwSyJQjIa4zYtUDwQGc+YzbKU8Uz4Yf3d+Z9KGBaUgzPXhh6MJOXW9Vq+qHkbI1eBN9JecUX8njSD09qhyo0IdBtw6TDVN43hs9KzMPpWB3TeM7LkZgAU5G8JHcz1uKU1ynZ2ww6ljUsAt/982VrsK2e8VhoORAMFSJMP+wotAgJYtmj9HnjpMIGNcYom/VJ9J3iMA+BKkweg7zfZt7aT9ZT8KZUdwuhn+iB0sdepjAMN1OzI8Llyu8="})
    api_key = requests.json()
    
    headers = {
      'Accept': 'application/json',
      'x-api-key': api_key["api_key"]
    }

    r = requests.get('https://api.curseforge.com/v1/mods/search',params={'gameId': '432',"searchFilter": "{}".format(mod_name), "sortOrder": "desc"},headers = headers)
	
    trj = requests.json()
    return trj

def about():
    
    return {"ver": "0.0.1", "Copyright": "LJS80","PF": "FMCL-AuthorizedUse"}
