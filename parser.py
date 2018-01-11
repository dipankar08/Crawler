#! /usr/bin/python
import requests
import sys
from bs4 import BeautifulSoup
from timeit import timeit
import pdb
import infyScrollFetch

debug = True
baseurl = ""
import re

def cleartest(s):
    return re.sub("\s\s+" , " ", s)

def myassert(cond, msg):
    if not cond:
        print msg
        if debug: pdb.set_trace()
        sys.exit(0)

def getSoup(url, pxscrolllimit=None):
    # pdb.set_trace()
    if debug: print '************Fetching*****************\n ', url, '...'
    if pxscrolllimit is None or pxscrolllimit is 0:
        html_doc = requests.get(url).text
    else:
        html_doc = infyScrollFetch.get(url)
    soup = BeautifulSoup(html_doc, 'html.parser')
    return soup

def abs(base, url):
    if not url:
        print '[ERROR] Missing Url in abs()'
        if debug: pdb.set_trace()
        return
    if '/' == url[0]:
        return baseurl+url
    else:
        return url
def base(url):
    if not url:
        print '[ERROR] Misisng url'
        return
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

def fixSelect(soup,sel):
    if soup and sel:
        soup1 = BeautifulSoup('<div>'+str(soup)+'</div>',"html.parser")
        return soup1.select(sel)
    else:
        return []

def select(soup,selector, types, nolist = True ):
    if not soup:
        if debug: pdb.set_trace()
        print('Sout is null')
        return ''
    # print selector,types,nolist
    #Fix as soup is not considering outer..
    sl = fixSelect(soup, selector)
    sl1 =[]
    #print sl
    for s in sl:
        if types == 'text':
            sl1.append(cleartest(s.text))
        elif types == 'href':
            sl1.append(abs(base, s.get(types)))
        else:
            if s.get(types):
                sl1.append(s.get(types))
            else:
                print '>>>>>Error Missing fields: '+types
    if debug: print 'Select Returns:', sl1
    if nolist and sl1 is not None:
        return ','.join(sl1)
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

def getDataInternal(url, data, dataselector, datacommon,  datascrolllimit, threads):
    # pdb.set_trace()
    soup = getSoup(url, datascrolllimit)
    datacommonresult = elemetryData(soup, datacommon)

    if dataselector:
        datasets = soup.select(dataselector)
        return [join(elemetryData(soup1, data), datacommonresult) for soup1 in datasets]
    else:
        return [join(elemetryData(soup, data),datacommonresult)]

@timeit
def getData(debug1, url, data, dataselector, datacommon, datalimit, datascrolllimit, threads):
    pre(debug1, url)
    if debug: print ('Get Data called with:',url,data,dataselector,datacommon, datalimit, datascrolllimit,threads)
    data= getDataInternal(url, data, dataselector, datacommon, datascrolllimit, threads)
    return data[:datalimit]

@timeit
def getPXData(debug1, pxurl, pxselector, pxlimit, pxscrolllimit, data, dataselector,datacommon, datalimit, datascrolllimit, threads):
    pre(debug1, pxurl)
    # Verify.
    depth = len(pxselector)
    pxlimit = int(pxlimit)
    pxscrolllimit = int(pxscrolllimit)
    datalimit = int(datalimit)
    datascrolllimit =int(datascrolllimit)

    startsets = [pxurl]
    endsets = []
    for d in range(depth):
        if debug:
            print('Featching for depth'+str(d+1))
            print 'Staring url set',startsets
        for url in startsets:
            soup = getSoup(url, pxscrolllimit)
            # pdb.set_trace()
            endsets += [ abs(base,x.get('href')) for x in soup.select(pxselector[d]) if x.get('href') and x.get('href').strip() != '#']
            if len(endsets) > pxlimit:
                endsets = endsets[:pxlimit]
                break
        myassert(len(endsets) > 0,"Some how we dont have any url at depth "+str(d))
        startsets = endsets
        endsets = []
    if debug: print 'All depth parse complete and count of dataurl is :', len(endsets)
    #pdb.set_trace()
    if not data:
        print 'All Data use found is:',len(startsets)
        print 'Please use -data options to get the data'
        print startsets
        return
    durls = startsets
    result = []
    for url in durls:
        res = getDataInternal(url, data, dataselector, datacommon, datascrolllimit, threads)
        if res:
            result = result + res
            if len(result) == datalimit:
                break
    return result
