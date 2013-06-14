import requests
import BeautifulSoup
import urllib
import time

#constants
DRAWING_URL = 'http://zionpermits.nps.gov/lastminutedrawingapply.cfm'
ZION_NARROWS_RESOURCE_ID = '30035000'
PROXY_DICT = urllib.getproxies()
POLL_DURATION_SECONDS = 60 * 10

def extract_form_fields(html):
    form = dict()
    form['ResourceID'] = ZION_NARROWS_RESOURCE_ID

    #parse html and get the ZEPToken value
    soup = BeautifulSoup.BeautifulSoup(html)
    inputTags = soup.findAll('input')
    for tag in inputTags:
        if tag.get('name') == 'ZEPToken':
            form['ZEPToken'] = tag.get('value')
        if tag.get('name') == 'as_fid':
            form['as_fid'] = tag.get('value')

    return form

def extract_dates(html):
    dates = list()
    soup = BeautifulSoup.BeautifulSoup(html)
    results = soup.findAll('input')
    for tag in results:
        if tag.get('name') == 'FirstDate':
            dates.append(tag.get('value'))
    return dates

def get_zion_narrows_dates(proxyDict):
    #make initial request
    r = requests.get(DRAWING_URL)
    cookiejar = r.cookies
    post_params = extract_form_fields(r.text)

    #post request to get drawing dates for narrows
    r = requests.post(DRAWING_URL, post_params, proxies=proxyDict, cookies=cookiejar)
    dates = extract_dates(r.text)
    return dates

def return_added_items(old_list, new_list):
        old_set, new_set = [set(old_list), set(new_list)]
        return new_set - new_set.intersection(old_set)

lastdates = get_zion_narrows_dates(PROXY_DICT)
print "Initial dates: ", lastdates
while True:
    time.sleep(POLL_DURATION_SECONDS)
    newdates = get_zion_narrows_dates(PROXY_DICT)
    addedSet = return_added_items(lastdates, newdates)
    if len(addedSet) > 0:
        print time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), " - Added: ", addedSet
        break;
    else:
        print time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), " - Nothing added"
    lastdates = newdates


"""
Output:

Initial dates:  [u'06/16/2013', u'06/17/2013', u'06/18/2013', u'06/19/2013', u'06/20/2013']
2013-06-13 20:04:09  - Nothing added
2013-06-13 20:14:10  - Nothing added
2013-06-13 20:24:11  - Nothing added
2013-06-13 20:34:12  - Nothing added
2013-06-13 20:44:13  - Nothing added
2013-06-13 20:54:14  - Nothing added
2013-06-13 21:04:15  - Nothing added
2013-06-13 21:14:16  - Nothing added
2013-06-13 21:24:18  - Nothing added
2013-06-13 21:34:19  - Nothing added
2013-06-13 21:44:20  - Nothing added
2013-06-13 21:54:21  - Nothing added
2013-06-13 22:04:22  - Nothing added
2013-06-13 22:14:23  - Nothing added
2013-06-13 22:24:24  - Nothing added
2013-06-13 22:34:25  - Nothing added
2013-06-13 22:44:26  - Nothing added
2013-06-13 22:54:27  - Nothing added
2013-06-13 23:04:28  - Nothing added
2013-06-13 23:14:29  - Nothing added
2013-06-13 23:24:31  - Nothing added
2013-06-13 23:34:32  - Nothing added
2013-06-13 23:44:33  - Nothing added
2013-06-13 23:54:34  - Nothing added
2013-06-14 00:04:35  - Nothing added
2013-06-14 00:14:37  - Nothing added
2013-06-14 00:24:38  - Nothing added
2013-06-14 00:34:39  - Nothing added
2013-06-14 00:44:40  - Nothing added
2013-06-14 00:54:41  - Nothing added
2013-06-14 01:04:42  - Nothing added
2013-06-14 01:14:43  - Nothing added
2013-06-14 01:24:44  - Nothing added
2013-06-14 01:34:45  - Nothing added
2013-06-14 01:44:46  - Nothing added
2013-06-14 01:54:47  - Nothing added
2013-06-14 02:04:49  - Added:  set([u'06/21/2013'])
"""