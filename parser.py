#! /usr/bin/python
import requests
from bs4 import BeautifulSoup
from timeit import timeit
import pdb

debug = True
baseurl = ""
def getSoup(url):
    if debug: print 'Fetching ', url, '...'
    html_doc = requests.get(url).text
    soup = BeautifulSoup(html_doc, 'html.parser')
    return soup

def abs(base, url):
    if '/' == url[0]:
        return baseurl+url
    else:
        return url
def base(url):
     # pdb.set_trace()
    return url[:url[9:].find('/')+9]

def parseXPath(data):
    if not data: return []
    data1 = []
    for d in data:
        if ' ' not in d or ':' not in d:
            if debug: print 'Error in xpath and will be ignored =>',d
            continue
        name = d[:d.find(' ')]
        value =d[d.find(' ')+1:d.rfind(':')]
        attr = d[d.rfind(":")+1:]
        data1.append((name,value,attr))
    return data1

def select(soup,selector, type, nolist = True ):
    sl = soup.select(selector)
    sl1 =[]
    for s in sl:
        if type == 'text':
            sl1.append(s.text)
        elif type == 'href':
            sl1.append({s.text: abs(base, s.get(type))})
        else:
            sl1.append(s.get(type))
    if debug: print 'Select Returns:', sl1

    if nolist:
        return ', '.join(sl1)
    return sl1

def pre(debug1, url):
    global debug
    debug = debug1
    global baseurl
    baseurl = base(url)
    if debug:
        print '>>> Running in debug mode ...'
def elemetryData(soup,data):
    result = {}
    data = parseXPath(data)
    if debug: print '>>> parsed data:', data
    for d in data:
        result[d[0]] = select(soup, d[1], d[2])
    return result
@timeit
def getData(debug1, url, dataselector, data, threads):
    pre(debug1, url)
    soup = getSoup(url)
    if dataselector:
        datasets = soup.select(dataselector)
        return [elemetryData(soup1, data) for soup1 in datasets]
    else:
        return elemetryData(soup, data)

@timeit
def getPData(debug1, purl, pselctor, plimit,dataselector, data, threads):
    pre(debug1, purl)

    soup = getSoup(purl)
    urls = [ abs(base,x.get('href')) for x in soup.select(pselctor) if x.get('href') and x.get('href').strip() != '#']
    if debug: print 'Urls getting after exploring parents', urls

    result = []
    for url in urls[:plimit]:
        res = getData(debug1, url,dataselector, data, threads)
        if isinstance(res, dict):
            result.append(res)
        elif isinstance(res, list):
            result += res
    return result

@timeit
def getPPData(debug1, ppurl, ppselctor, pplimit, pselctor, plimit,dataselector, data, threads):
    pre(debug1, ppurl)

    soup = getSoup(ppurl)
    if debug: print ppselctor
    #pdb.set_trace()
    purls = [ abs(base,x.get('href')) for x in soup.select(ppselctor) if x.get('href') and x.get('href').strip() != '#']
    if debug: print 'Urls getting after exploring parents', purls

    result = []
    for purl in purls[:plimit]:
        res = getPData(debug1, purl, pselctor, plimit, dataselector, data, threads)
        if res:
            result = result + res
    return result
