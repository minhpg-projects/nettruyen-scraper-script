import requests
from multiprocessing.pool import ThreadPool
import os

def download(i):
    print(i)
    if not os.path.isfile(os.path.join(i["title"],i["chap"],i["url"].split("/")[-1])):
        if not "https" in i["url"]:
            i["url"] = i["url"].replace("//","https://")
        if "?" in i["url"]:
            i["url"] = i["url"].replace(i["url"][i["url"].find("?")::],"")
        response = requests.get(i["url"])
        open(os.path.join(i["title"],i["chap"],i["url"].split("/")[-1]),"wb").write(response.content)

def getImages(url):
    response = requests.get(url)
    lines = response.text.split("\n")
    image=[]
    for i in lines:
        if "id='page" in i:
            image.append(i)
    links=[]
    for i in image:
        p = i.split("'")
        for l in p:
            if "/" in l and "." in l:
                links.append(l)
    links = list(dict.fromkeys(links))
    return links

def treeUrl(url):
    components = url.split("/")
    manga_title = components[4]
    chap = components[5]
    if not os.path.isdir(manga_title):
        os.mkdir(manga_title)
    if not os.path.isdir(os.path.join(manga_title,chap)):
        os.mkdir(os.path.join(manga_title,chap))
    return {"title":manga_title,"chap":chap}

def singleChap(url):
    tree = treeUrl(url)
    images = getImages(url)
    links = []
    for i in images:
        meta = {"title":tree["title"],"chap":tree["chap"],"url":i}
        print(meta)
        links.append(meta)
    print(links)
    p = ThreadPool(20)
    p.map(download,links)

def extractTitle(url):
    titleWithId = url.split("/")[-1]
    comps = titleWithId.split("-")
    comps.remove(comps[-1])
    title = "-".join(comps)
    return(title)

def getChapter(url):
    response = requests.get(url)
    lines = response.text.split("\n")
    chaps = []
    for i in lines:
        if "Chapter" in i and extractTitle(url) in i:
            comps = i.split('"')
            chaps.append(comps[1])
    return chaps

url = "https://www.nettruyen.com/truyen-tranh/vo-dong-can-khon-4394"
chaps = getChapter(url)
for i in chaps:
    singleChap(i)

