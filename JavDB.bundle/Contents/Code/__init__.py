import sys, requests, json, os
from requests import Session
import re, types, traceback
import Queue

search_url = 'https://www.javbus.com/'

def Start():
    #HTTP.ClearCache()
    HTTP.CacheTime = CACHE_1WEEK
    HTTP.Headers['User-agent'] = 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.2; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0)'
    HTTP.Headers['Accept-Encoding'] = 'utf-8'

class Data18(Agent.Movies):
    name = 'JAVDB'
    languages = [Locale.Language.English]
    primary_provider = True
    accepts_from = None

    prev_search_provider = 0

    data = {}

    def search(self, results, media, lang, manual=False):
        genre = {}
        star = {}
        downloads = {}
        ID = media.name
        Log.Debug("**************search: "+ID)
        self.data["ID"] = ID.upper()
        self.data["URL"] = self.search_url+ID
        self.data["Samples"] = [""]
        self.data["Studio"] =""
        self.data["Label"]  =""
        self.data["Director"] =""
        self.data["Series"] =""
        self.data["Genres"] =[""]


        html = HTML.ElementFromURL(search_url+ID, sleep=0)
        info = html.find('div',"col-md-3 info")

        self.data["Title"] =html.find('h3').text[len(ID)+1:]
        self.data["Cover"] = html.find('a',"bigImage")['href']
        self.data["Thumb"] = "https://pics.javbus.com/thumb/"+data["Cover"].split('/')[-1].split('_')[0]+".jpg"
        ########## Date ###########
        d = info.find_all("p")[1].text[6:]
        self.data["Date"] = d
        # print("date: "+d)
        ######### Length###########
        l = info.find_all("p")[2].text[4:-2]
        self.data["Duration"] = int(l)*60000
        # print("Length: "+l)
        texts = info.find_all("a")
        for text in texts:
            link = text['href']
            string = text.text
            if link.find("studio") >=0:
                self.data["Studio"] = string
                self.data["StudioLink"] = link
                # print("Studio: "+string+ " : "+link)
            if link.find("label") >=0:
                self.data["Label"] = string
                self.data["LabelLink"] = link
                # print("Label: "+string+ " : "+link)
            if link.find("director") >=0:
                self.data["Director"] = string
                self.data["DirectorLink"] = link
                # print("Director: "+string+ " : "+link)
            if link.find("series") >=0:
                self.data["Series"] = string
                self.data["SeriesLink"] = link
                # print("Series: "+string+ " : "+link)
            if link.find("genre") >=0:
                genre[string] = link
        self.data["Genres"] = genre

        st = html.find_all('a',"avatar-box")
        if st is not None and len(st) >0:
            for s in st:
                link = s['href']
                starhtml = HTML.ElementFromURL(link, sleep=0)
                info = starhtml.find('div','avatar-box')
                details = {}
                details["Link"] = link
                details["Avatar"] =info.find('img')["src"]
                texts = info.find_all("p")
                for text in texts:
                    details[text.text.split(':')[0]] = text.text.split(':')[1]
                name = s.text.strip()
                star[name] = details

        self.data["Stars"] = star

        samples = html.find_all('a',"sample-box")
        if samples is not None and len(samples) >0:
            for s in samples:
                self.data["Samples"].append(s['href'])
        results.Append(MetadataSearchResult(id = media.name, name  = media.name, score = '100', lang = Locale.Language.English))

    def update(self, metadata, media, lang, force=False):
        Log.Debug("**************update: "+ID)
        metadata.title = self.data["Title"]
        metadata.genres = self.data["Genres"]
        metadata.tags = self.data["Genres"]
        metadata.collections = self.data["Series"]
        metadata.duration = self.data["Duration"]
        metadata.rating = 10.0
        metadata.original_title = self.data["Title"]
        metadata.year = 2018
        metadata.originally_available_at = Datetime.ParseDate(self.data["Date"]).date()
        metadata.studio = self.data["Studio"]
        metadata.tagline = self.data["URL"]
        metadata.summary = self.data["Title"]
        metadata.trivia = "trivia...."
        metadata.content_rating = "R18"
        metadata.content_rating_age = "18"
        metadata.writers = ["writer"]
        metadata.directors = [self.data["Director"]]
        metadata.producers = [self.data["Label"]]
        metadata.countries = ["Japan"]
        #meta_role = metadata.roles.new()
        #meta_role.role = "rolerole"
        #meta_role.name = "rolename"
        #meta_role.photo = "https://pics.javbus.com/actress/ntx_a.jpg"
        metadata.posters = Proxy.Preview(HTTP.Request(self.data["Cover"]).content)
        #metadata.art = Proxy.Preview(HTTP.Request(self.data["Samples"][0]).content)
