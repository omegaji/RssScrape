from bs4 import BeautifulSoup as bs4
import requests
import feedparser
import urllib.parse
from io import BytesIO

def findfeed(site):
    raw = requests.get(site).text
    result = []
    possible_feeds = []
    html = bs4(raw)
    feed_urls = html.findAll("link", rel="alternate")
    if len(feed_urls) > 1:
        for f in feed_urls:
            t = f.get("type",None)
            if t:
                if "rss" in t or "xml" in t or "rdf" in t or "atom" in t :
                  
                    href = f.get("href",None)
                    if href:
                        if href[0]=='/' and href[1]=='/':
                            href="http:"+href

                    # (feed_url.indexOf("//") == 0)
                    # feed_url = "http:" + feed_url;
                # // If feed's url starts with "/"
                        elif href[0]=="/":
                            href=site.split("/")[0]+'//'+site.split('/')[2]+href
                            # (feed_url.startsWith('/'))
                            # feed_url = url.split('/')[0] + '//' + url.split('/')[2] + feed_url;
                        # // If feed's url starts with http or https
                        elif href[:4]=="http":
                            href=href
                        #  (/^(http|https):\/\//i.test(feed_url))
                        #     feed_url = feed_url;
                        # // If feed's has no slash
                        elif "/" not in href:
                            lastindex=site.rfind("/")
                            href= site[0:lastindex]+"/"+href
                            # feed_url = url.substr(0, url.lastIndexOf("/")) + '/' + feed_url;
                        else:
                            if href[0]=='/':
                                href=href[1:]
                            href=site+"/"+href
                        possible_feeds.append(href)
    parsed_url = urllib.parse.urlparse(site)
    base = parsed_url.scheme+"://"+parsed_url.hostname
    atags = html.findAll("a")

    tests = ['/feed', '/rss', '/rss.xml', '/feed.xml']
    for t in tests:
        try:
            f=feedparser.parse(base+t)
            if len(f.entries)>0:
                possible_feeds.append(base+t)
        except:
            print("Exception in secondary")

    for a in atags:
        href = a.get("href",None)
        if href:
            if "xml" in href or "rss" in href or "feed" in href:
                
                # // If feed's url starts with "//"
                if href[0]=='/' and href[1]=='/':
                    href="http:"+href

                    # (feed_url.indexOf("//") == 0)
                    # feed_url = "http:" + feed_url;
                # // If feed's url starts with "/"
                elif href[0]=="/":
                    href=site.split("/")[0]+'//'+site.split('/')[2]+href
                    # (feed_url.startsWith('/'))
                    # feed_url = url.split('/')[0] + '//' + url.split('/')[2] + feed_url;
                # // If feed's url starts with http or https
                elif href[:4]=="http":
                    href=href
                #  (/^(http|https):\/\//i.test(feed_url))
                #     feed_url = feed_url;
                # // If feed's has no slash
                elif "/" not in href:
                    lastindex=site.rfind("/")
                    href= site[0:lastindex]+"/"+href
                    # feed_url = url.substr(0, url.lastIndexOf("/")) + '/' + feed_url;
                else:
                    if href[0]=='/':
                        href=href[1:]
                    href=site+"/"+href                   
                    # feed_url = url + "/" + feed_url.replace(/^\//g, '');
                possible_feeds.append(href)
    for url in list(set(possible_feeds)):
        print(url)
        try:
            resp = requests.get(url, timeout=30.0)
            content = BytesIO(resp.content)
            f = feedparser.parse(content)
            print("in feedparser trys")
            if len(f.entries) > 0:
                if url not in result:
                    result.append(url)


        except requests.ReadTimeout:
            print("timeout")
  
        except:
            print("couldnt parse this url")
            print(url)
            
    return(result)


class TheBigScrape():
    def __init__(self):
        self.RssCount=0
        self.RssList=[]
        self.url=""
        self.DataDict={
            "title":[],
            "author":[],
            "content":[],
            "large_content":[],
            "published":[],
            "contenturl":[]
        }
    def StoreUrl(self,url):
        self.url=url
    def FetchRssList(self):
        try:
            self.RssList=findfeed(self.url)
            self.RssCount=len(self.RssList)
        except Exception as e:
            if "url" in str(e):
                print("silly exception still storing--->",self.url)
  
    def FetchRssData(self):
        for rss in self.RssList:
            feed=feedparser.parse(rss)
            for entry in feed.entries:
                try:
                    self.DataDict["title"].append(entry.title)
                except:
                    self.DataDict["title"].append("none")
                try:
                    self.DataDict["author"].append(entry.author)
                except:
                    self.DataDict["author"].append("none")
                try:
                    self.DataDict["content"].append(entry.summary)
                except:
                    self.DataDict["content"].append("none")
                try:
                    self.DataDict["large_content"].append(entry.content[0])
                except:
                    self.DataDict["large_content"].append("none")
                try:
                    self.DataDict["published"].append(entry.published)
                except:
                    self.DataDict["published"].append("none")
                try:
                    self.DataDict["contenturl"].append(entry.link)
                except:
                    self.DataDict["contenturl"].append("none")
                
                

        



        