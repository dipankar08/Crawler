"""Collect command-line options in a dictionary"""
import parser
import sys
import pdb
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
def desc():
    print """
    Welcome to Crawler! Which makes your life simple for crawling.
    --pxurl <url>          : Spaciify your url which is used is a cetegories page
    --pxselector <selector to a> : Spaiciy the selector which is to select the urls for next level

    

    --url : place the data url when you just have  a data (detail) url.
    --data "<title> <selector>:<type>" indicates the data at the detail page
    --dataselector <selecotor> -> when data page conains a group of information, this indiacte the LCA selector.

    --datalimit <int> -> indidicates how many data entry to be in result ( default = 10)
    --pxlimit <int>   -> indicates how many navigation url to be consider in categories page
    --thread <int>    -> how many parallel thread to be run.
    --debug           -> If you wnat to see the debug logs

    Notes:
    1. You can have multiple pxurl and pxselctor to explore multiple levels.
    2. 

    This script can crawl any site in a easyer way in commd line
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

    """
if __name__ == '__main__':
    from sys import argv
    myargs = getopts(argv)

    url = myargs.get('url', None)
    pxurl = myargs.get('pxurl', None)

    pxselctor = myargs.get('pxselector')
    pxlimit = myargs.get('pxlimit', [3])
    pxscrolllimit = myargs.get('pxscrolllimit', [0])

    data = myargs.get('data')
    dataselector = myargs.get('dataselector',[None])
    datascrolllimit = myargs.get('datascrolllimit', [0])
    datalimit = myargs.get('datalimit',[10])

    if pxscrolllimit: pxscrolllimit = [int(x) for x in pxscrolllimit]
    if datascrolllimit: datascrolllimit = [int(x) for x in datascrolllimit]
    if datalimit: datalimit = [int(x) for x in datalimit]


    debug = myargs.get('debug', False)
    threads = myargs.get('threads', 1)
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
            ans = parser.getData(debug, url[0], data, dataselector[0], datalimit[0],datascrolllimit[0], threads)
    elif pxurl:
            assert(pxselctor is not None)
            ans = parser.getPXData(debug, pxurl[0], pxselctor, pxlimit[0], pxscrolllimit[0],data, dataselector[0], datalimit[0], datascrolllimit[0], threads)
    if action == 'print':
        print 'Total entry found:', len(ans)
        #print ans
        from tabulate import tabulate
        print tabulate([x.values() for x in ans], headers=ans[0].keys(), tablefmt='fancy_grid')
    elif action =='save':
        print 'Saveing file...'
        import pickle
        pickle_out = open("data.pickle","wb")
        pickle.dump(ans, pickle_out)
        pickle_out.close()
    else:
        print 'No action required'
        pass
