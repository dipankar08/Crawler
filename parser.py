#! /usr/bin/python
import requests
import sys
from bs4 import BeautifulSoup
from timeit import timeit
import pdb
import infyScrollFetch
import concurrent.futures
from colors import *
sys.stdout.write(RED)
debug = True
baseurl = ""
import re
from operator import itemgetter

def cleartest(s):
    return re.sub("\s\s+" , " ", s)

def unique_by_key(elements, key=None):
    if key is None:
        # no key: the whole element must be unique
        key = lambda e: e
    return {key(el): el for el in elements}.values()

#join two dict
def join(a,b):
    for k,v in b.items():
        a[k] = v
    return a

def myassert(cond, msg):
    if not cond:
        print msg
        if debug: pdb.set_trace()
        sys.exit(0)

def getSoup(url, pxscrolllimit=None):
    try:
        # pdb.set_trace()
        if debug: print '\n************Fetching*****************\n ', url, '...'
        sys.stdout.write('.')
        sys.stdout.flush()
        if pxscrolllimit is None or pxscrolllimit is 0:
            html_doc = requests.get(url).text
        else:
            html_doc = infyScrollFetch.get(url)
        soup = BeautifulSoup(html_doc, 'html.parser')
        return soup
    except Exception, e:
        print 'While Retriving URL...',url
        pdb.set_trace()
    

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
def getDataInternalRef(a):
    return getDataInternal(*a)
def getDataInternal(predata, url, data, dataselector, datacommon,  datascrolllimit, threads):
    #pdb.set_trace()
    soup = getSoup(url, datascrolllimit)
    if not soup:
        print '[ERROR] getDataInternal: Not able to get the soup for data url:',url
        return []
    datacommonresult = elemetryData(soup, datacommon)
    datacommonresult = join(datacommonresult, predata)
    datacommonresult['_url'] = url

    if dataselector:
        datasets = soup.select(dataselector)
        return [join(elemetryData(soup1, data), datacommonresult) for soup1 in datasets]
    else:
        return [join(elemetryData(soup, data),datacommonresult)]

def getData(predata, debug1, url, data, dataselector, datacommon, datalimit, datascrolllimit, threads):
    pre(debug1, url)
    if debug: print ('Get Data called with:',url,data,dataselector,datacommon, datalimit, datascrolllimit,threads)
    data= getDataInternal(predata, url, data, dataselector, datacommon, datascrolllimit, threads)
    return data[:datalimit]

def fetchCategoriesRef(args):
    return fetchCategories(*args)

def fetchCategories(depth, curl, pi, pxscrolllimit, pxselector):
    soup = getSoup(curl, pxscrolllimit)
    if not soup:
        print '[ERROR] fetchCategories: Not able to get the soup for data url:',url
        return []
    endsets1 = []
    curselectors = pxselector[depth]['selector']
    nextselector = pxselector[depth]['next']
    while True:
        for cs in curselectors:
            if len(soup.select(cs)) == 0:
                print '[Possible Error] Not able to find any categories for ->',cs,' in url =>',curl
            for x in soup.select(cs):
                if x.get('href') and x.get('href').strip() != '#':
                    url = abs(base,x.get('href'))
                    pre1 = pi.copy()
                    pre1['depth'+str(depth)] = x.text
                    endsets1.append((url, pre1))
        #Do you have next page
        if nextselector:
            pagenext = soup.select(nextselector)
            if pagenext:
                #pdb.set_trace()
                if pagenext[0].get('href') and pagenext[0].get('href').strip() != '#':
                    curl = abs(base,pagenext[0].get('href'))
                    soup = getSoup(curl, pxscrolllimit)
                    if soup:
                        if debug: print 'Moving to next page ...'
                        continue
            print '[Possible Error] Not able to find next page ->',nextselector,' in url =>',curl
        break
    return endsets1


def getPXData(predata, debug1, pxurl, pxselector, pxlimit, pxscrolllimit, data, dataselector,datacommon, datalimit, datascrolllimit, threads):
    #pdb.set_trace()
    pre(debug1, pxurl)
    # Verify.
    depth = len(pxselector)
    pxlimit = int(pxlimit)
    pxscrolllimit = int(pxscrolllimit)
    datalimit = int(datalimit)
    datascrolllimit =int(datascrolllimit)

    startsets = [(pxurl,{})]
    endsets = []
    for d in range(depth):
        if debug:
            print('Featching for depth'+str(d+1))
            print 'Staring url set', startsets
        curselectors = pxselector[d]

        #Parallel processing ..
        endsets = []
        inps = [(d, url, pi, pxscrolllimit, pxselector) for url,pi in startsets]
        if threads > 1:
            with concurrent.futures.ProcessPoolExecutor(max_workers=threads) as pool:
                outs = [a for a in pool.map(fetchCategoriesRef,inps)]
            for o in outs:
                endsets += o
        else:
            outs = [ fetchCategoriesRef(ii) for ii in inps] 
            for o in outs:
                endsets += o
        
        #Just keep uniquue.
        print '[INFO] Complete the exploring depth:',(d+1)
        #pdb.set_trace()
        a_len = len(endsets)
        endsets = unique_by_key(endsets, key=itemgetter(0))
        b_len = len(endsets)
        print '[DEBUG] Duplicate found: ',(a_len - b_len) 
        print '[INFO] Total uninique link found :', len(endsets)

        #trim down endsets
        endsets = endsets[:pxlimit]
        myassert(len(endsets) > 0,"Some how we dont have any url at depth "+str(d))

        #flip
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
    # multiprocessing ... 
    inps = [(p, url, data, dataselector, datacommon, datascrolllimit, threads) for url, p in durls]
    if threads > 1:
        with concurrent.futures.ProcessPoolExecutor(max_workers=threads) as pool:
            out = [ a for a in pool.map(getDataInternalRef,inps)]
        result = []
        for o in out:
           result += o 
    else:
        result = [ getDataInternalRef(ii) for ii in inps] 
    #pdb.set_trace()
    return result[:datalimit]
    
