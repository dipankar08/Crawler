"""Collect command-line options in a dictionary"""
import parser
import sys
import pdb
from colors import *
from timeit import timeit
def getopts(argv):
    argv = [x.strip() for x in ' '.join(argv[1:]).split('--') if x.strip()]
    opts = {}
    for p in argv:
        token = p.split(' ')
        key = token[0]
        value = ' '.join(token[1:])
        if key in opts:
            opts[key].append(value)
        else:
            opts[key] = [value]
        argv = argv[1:]
    return opts

# Example:
# python main.py --key1 value1 --key2 value2 --key2 value3
# {'key2': ['value2', 'value3'], 'key1': ['value1']}
sys.stdout.write(RESET)
def desc():
    print """
    ***************************************************************
    Welcome to Crawler! Which makes your life simple for crawling.

    --pxurl <url>          : Spaciify your url which is used is a cetegories page
    --pxselector <selector to a> : Spaiciy the selector which is to select the urls for next level

    --url : place the data url when you just have  a data (detail) url.
    --data "<title> <selector>:<type>" indicates the data at the detail page
    --dataselector <selecotor> -> when data page conains a group of information, this indiacte the LCA selector.
    --datacommon "<title> <selector>:<type>" -> Some common data in page having multiple entry and need to copy in all the entryes.

    --datalimit <int> -> indidicates how many data entry to be in result ( default = 10)
    --pxlimit <int>   -> indicates how many navigation url to be consider in categories page (default = 3)
    --thread <int>    -> how many parallel thread to be run.(default: 1)
    --debug           -> If you wnat to see the debug logs(default: false)
    --action <save|print> indicate if you want to save or print (default: print)

    Notes:
    1. You can have multiple pxurl and pxselctor to explore multiple levels.
    2. 

    Let's go though some of the exmaples.

    Example 1: This example show find some data or a list of data from a website.

    python main.py \
    --url http://mio.to/ \
    --data heading .heading h1:text

    Example 2: How to retrive a list of grouped data from url. Like how can you
    retrive a list of strudent data from an page? In that case you need to use
    --dataselector to indiactes the group and then use --data to indivisal item
    in the group.

    python main.py \
    --url http://mio.to/ \
    --dataselector "#genres-list a" \
    --data name a:text --data link a:href

    You could use --datalimit to restric the outpit.
    $ python main.py \
    --url http://mio.to/ \
    --dataselector "#genres-list a" \
    --data name a:text \
    --data link a:href \
    --datalimit 5

    Example 3: In this example, I will show to to parse a serach page and then
    retrive data from each detail page. For Example, we want to enlist all the
    books in goodreads mystery class then go to each book page to retrive book
    title and rating. Here is how we can do it

    python main.py \
    --pxurl https://www.goodreads.com/genres/mystery \
    --pxselector .bigBoxBody .coverWrapper a \
    --data "title #bookTitle:text" \
    --data "rating span.rating:text" \
    --datalimit 100 \
    --pxlimit 50 \
    --debug


    Example 3: careercup has multiple pages and each page has list of question
    preview and in each question we have Question, Answer and number of coments
    Vote info. Can you find all the votes along with id.
    python main.py --pxurl https://www.careercup.com/page --pxselector a.pageNumber --pxselector '#question_preview li .entry >  a' --data id .votesCountQuestion:id --data vote .commentCount:text --debug

    Exmaple 4: How would you grab all mobile data from flipkert ?
    python main.py \
    --url https://www.flipkart.com/mobiles-new-pinch-sales-store  \
    --dataselector ._2kSfQ4  \
    --data name .iUmrbN:text \
    --data price ._3o3r66:text \
    --datalimit 100

    Example 3: How can I get debug logs the script:
    use --debug at the end.

    Example #5: Let's see some uses of data common 
    python main.py \
    --url http://mio.to/album/Sree+Sai+Dev/Tea+Kadai+Bench+%282018%29 \
    --dataselector ".track-list tr" \
    --datacommon "image .album img:src" \
    --datacommon "almum .heading .title:text" \
    --data number .track-number .number:text \
    --data title .track-details .link:text \
    --datalimit 5

    Example 6: We can see multple depth is listed as well.
    python main.py \
    --pxurl http://mio.to/Bengali \
    --pxselector "#genres-list a" \
    --pxselector "#albums-decades a" \
    --data "heading   h1:text" \
    --pxlimit 100 \
    --datalimit 100

    Example 7: We can also nevate categories page thogh NEXT page 

    python main.py \
    --pxurl http://mio.to/Bengali/Movie+Songs/albums/A \
    --pxselector ".block-cover .img-cover-175,next:.pagination a.next-page" \
    --data title h1:text \
    --pxlimit 1000 \
    --datalimit 10000 

    Example 8: We can combine mutiple selector in categioes page and as well as have a pointer to the next page.

    python main.py \
    --pxurl http://mio.to/Bengali \
    --pxselector "#genres-list a" \
    --pxselector "#albums-decades a,.alpha-list a,.nav-artists .alpha-list a" \
    --pxselector ".block-cover .img-cover-175,next:.pagination a.next-page" \
    --data albumtitle h1:text \
    --pxlimit 1000000 \
    --datalimit 10000000 \
    --threads 100


    """
@timeit
def main():
    from sys import argv
    myargs = getopts(argv)

    url = myargs.get('url', None)
    pxurl = myargs.get('pxurl', None)

    _pxselctor = myargs.get('pxselector')
    pxlimit = myargs.get('pxlimit', [3])
    pxscrolllimit = myargs.get('pxscrolllimit', [0])

    data = myargs.get('data')
    dataselector = myargs.get('dataselector',[None])
    datacommon = myargs.get('datacommon',[])
    #pdb.set_trace()
    datascrolllimit = myargs.get('datascrolllimit', [0])
    datalimit = myargs.get('datalimit',[10])
    threads = myargs.get('threads', [10])

    if pxscrolllimit: pxscrolllimit = [int(x) for x in pxscrolllimit]
    if datascrolllimit: datascrolllimit = [int(x) for x in datascrolllimit]
    if datalimit: datalimit = [int(x) for x in datalimit]
    if threads: threads = [int(x) for x in threads]

    debug = myargs.get('debug', False)

    # We are maing pxselector as more powerful
    # --pxselctor div1.a,div2.a,next:div3.a
    pxselctor =[]
    for p in _pxselctor:
        now ={'selector':[],'next':None}
        d = [ x.strip() for x in p.split(',') if x.strip()]
        for d1 in d:
            if 'next:' in d1:
                now['next'] = d1.replace('next:','')
            else:
                now['selector'].append(d1)
        pxselctor.append(now)
    print pxselctor

    
    #pdb.set_trace()
    action = myargs.get('action', ['print'])[0]

    ans = 'Not able to get Ans'
    if not url and not pxurl:
        print '\n\n    Error: You must have --url or --pxurl'
        desc()
        sys.exit(0)
    elif not data:
        print 'Error: You must have --data or we just print the urls'
        desc()
        #sys.exit(0)
    if url:
            ans = parser.getData({}, debug, url[0], data, dataselector[0], datacommon, datalimit[0],datascrolllimit[0], threads[0])
    elif pxurl:
            assert(pxselctor is not None)
            ans = parser.getPXData({}, debug, pxurl[0], pxselctor, pxlimit[0], pxscrolllimit[0],data, dataselector[0],datacommon, datalimit[0], datascrolllimit[0], threads[0])
    if action == 'print':
        sys.stdout.write(RESET)
        #print ans
        from tabulate import tabulate
        print tabulate([x.values() for x in ans], headers=ans[0].keys(), tablefmt='fancy_grid')
        print 'Total entry found:', len(ans)
    elif action =='save':
        print 'Saveing file...'
        import pickle
        pickle_out = open("data.pickle","wb")
        pickle.dump(ans, pickle_out)
        pickle_out.close()
    else:
        print 'No action required'
        pass
if __name__ == '__main__':
    main()

