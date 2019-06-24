from bs4 import BeautifulSoup
import requests
from pycookiecheat import chrome_cookies

# url of summaries web-page
url = "https://www.cl.cam.ac.uk/teaching/exams/reports/"


# This is an authentication protected resource, so I have logged in via a browser, and now need to
# use the authentication cookie (the session is active for a few hours so this is fine).
cookies = chrome_cookies(url)

# headers, in this case they were not required, cookie was sufficient to gain access to page, but here anyway
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,' +
              'application/signed-exchange;v=b3',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Host': 'www.cl.cam.ac.uk',
    'If-Modified-Since': 'Wed, 19 Jun 2019 14:02:45 GMT',
    'If-None-Match': '"3462-58badaf01ac3d-gzip"',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) ' +
                  'Chrome/75.0.3770.100 Safari/537.36'
}

# fetch http response (could have added headers=headers) it still works but turns out to be not necessary here
response = requests.get(url, cookies=cookies)

# extract the text data from the request
soup = BeautifulSoup(response.text, 'html.parser')


# now need to get all the list elements
links = [l['href'] for l in soup.find_all('a') if l.has_attr("href")]
for l in links:
    print(l)

# now extract only those links that are summaries
summary_links = [link for link in links if not link.find("summary")]

print(summary_links)

# now to download the content from all those links
for s_link in summary_links:
    # download the file
    response = requests.get(url + "/" + s_link, cookies=cookies)
    # write it into a new pdf file
    open("pdfs/" + s_link, 'wb').write(response.content)

# complete
print('done!')
