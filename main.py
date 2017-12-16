"""Collect command-line options in a dictionary"""
import parser
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
    Welcome to Crawler!

    This script can crawl any site in a easyer way in commd line
    Example 1: Get the heading from a site
    python main.py --url http://mio.to/ --data heading .heading h1:text

    Example 2: get all type and it's url:
    python main.py --url http://mio.to/ --data type .group a:href --data text .group a:text --debug

    Example 3: careercup has multiple pages and each page has list of question
    preview and in each question we have Question, Answer and number of coments
    Vote info. Can you find all the votes along with id.
    python main.py --ppurl https://www.careercup.com/page --ppselector a.pageNumber --pselector '#question_preview li .entry >  a' --data id .votesCountQuestion:id --data vote .commentCount:text --debug

    Exmaple 4: How would you grab all mobile data from flipkert ?
    python main.py --url https://www.flipkart.com/mobiles-new-pinch-sales-store  --dataselector ._2kSfQ4  --data name .iUmrbN:text --data price ._3o3r66:text

    Example 3: How can I get debug logs the script:
    use --debug at the end.

    E

    """
if __name__ == '__main__':
    from sys import argv
    myargs = getopts(argv)
    url = myargs.get('url', None)

    purl = myargs.get('purl', None)
    pselctor = myargs.get('pselector')
    plimit = myargs.get('plimit', 2)

    ppurl = myargs.get('ppurl')
    ppselctor = myargs.get('ppselector')
    pplimit = myargs.get('pplimit', 2)

    dataselector = myargs.get('dataselector')
    data = myargs.get('data')

    debug = myargs.get('debug', False)
    threads = myargs.get('threads', 1)
    action = myargs.get('action', 'print')
    ans = 'Not able to get Ans'
    if not url and not purl and not ppurl:
        print '\n\n    Error: You must have --url or --purl or --ppurl'
        desc()
    elif not data:
        print 'Error: You must have --data or --datalist'
        desc()
    else:
        if url:
            ans = parser.getData(debug, url[0], dataselector[0], data, threads)
        elif purl:
            assert(pselctor is not None)
            ans = parser.getPData(debug, purl[0],pselctor[0],plimit,dataselector[0], data, threads)
        elif ppurl:
            assert(ppselctor is not None)
            ans = parser.getPPData(debug, ppurl[0],ppselctor[0],pplimit,pselctor[0],plimit,dataselector, data, threads)

    if action == 'print':
        print 'Total entry found:', len(ans)
        from tabulate import tabulate
        print tabulate([x.values() for x in ans], headers=ans[0].keys(), tablefmt='fancy_grid')
