SEARCH_URL = 'https://www.javbus.com/'

def Start():
    #HTTP.ClearCache()
    HTTP.CacheTime = CACHE_1WEEK
    HTTP.Headers['User-agent'] = 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.2; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0)'
    HTTP.Headers['Accept-Encoding'] = 'utf-8'

class JAVDB(Agent.Movies):
    name = 'the JAVDB'
    languages = [Locale.Language.English]
    primary_provider = True
    accepts_from = None
    prev_search_provider = 0

    def search(self, results, media, lang, manual=False):
        Log.Debug("**************search: "+media.filename)
        results.Append(MetadataSearchResult(id = media.filename, name  = media.filename, score = 100, lang = Locale.Language.English))

    def update(self, metadata, media, lang, force=False):
        Log.Debug("**************update: "+"IPX-128")
        data = {}
        genre = {}
        star = {}
        downloads = {}
        ID = "IPX-128"
        data["ID"] = ID.upper()
        data["URL"] = SEARCH_URL+ID
        data["Samples"] = [""]
        data["Studio"] =""
        data["Label"]  =""
        data["Director"] =""
        data["Series"] =""
        data["Genres"] =[""]

        html = HTML.ElementFromURL(SEARCH_URL+ID, sleep=0)

        data["Title"] =html.xpath('/html/body/div[5]/h3')[0].text
        Log.Debug('*********Title: '+data["Title"])
        data["Cover"] = html.xpath('/html/body/div[5]/div[1]/div[1]/a/@href')[0]
        Log.Debug('*********Cover: '+data["Cover"])
        data["Thumb"] = "https://pics.javbus.com/thumb/"+data["Cover"].split('/')[-1].split('_')[0]+".jpg"
        Log.Debug('*********Thumb: '+data["Thumb"])
        data["Date"] = html.xpath('/html/body/div[5]/div[1]/div[2]/p[2]/text()')[0]
        Log.Debug('*********Date: '+data["Date"])
        l = html.xpath('/html/body/div[5]/div[1]/div[2]/p[3]/text()')[0][:-2]
        data["Duration"] = int(l)*60000
        Log.Debug('*********Duration: '+str(data["Duration"]))

        texts = html.xpath('/html/body/div[5]/div[1]/div[2]//a')
        for text in texts:
            link = text.xpath('@href')[0]
            string = text.text
            if "studio" in link:
                data["Studio"] = string
                data["StudioLink"] = link
                Log.Debug('*********Studio: '+data["Studio"])
            if "label" in link:
                data["Label"] = string
                data["LabelLink"] = link
                Log.Debug('*********Label: '+data["Label"])
            if "director" in link:
                data["Director"] = string
                data["DirectorLink"] = link
                Log.Debug('*********Director: '+data["Director"])
            if "series" in link:
                data["Series"] = string
                data["SeriesLink"] = link
                Log.Debug('*********Series: '+data["Series"])
            if "genre" in link:
                genre[string] = link
                Log.Debug('*********Genre: '+string)
        data["Genres"] = genre

        st = html.xpath('//*[@id="avatar-waterfall"]/a')
        if st is not None and len(st) >0:
            for s in st:
                link = s.xpath('@href')[0]
                name = s.text
#                 avatar = s.xpath('/div/img@src')
#                 star[name] = avatar
#                 Log.Debug('*********Star: '+name)
#         data["Stars"] = star

#         samples = html.xpath('//*[@id="sample-waterfall"]/a')
#         if samples is not None and len(samples) >0:
#             for s in samples:
#                 data["Samples"].append(s.xpath['@href'][0])
#                 Log.Debug('*********Smaple: '+s.xpath['@href'][0])

        metadata.title = "Title Test"
#         metadata.genres = data["Genres"]
#         metadata.tags = data["Genres"]
        metadata.collections = data["Series"]
        metadata.duration = data["Duration"]
        metadata.rating = 10.0
        metadata.original_title = data["Title"]
        metadata.year = 2018
        metadata.originally_available_at = Datetime.ParseDate(data["Date"]).date()
        metadata.studio = data["Studio"]
        metadata.tagline = data["URL"]
        metadata.summary = data["Title"]
        metadata.trivia = "trivia...."
        metadata.content_rating = "R18"
        metadata.content_rating_age = "18"
        metadata.writers = ["writer"]
        metadata.directors = [data["Director"]]
        metadata.producers = [data["Label"]]
        metadata.countries = ["Japan"]
        #meta_role = metadata.roles.new()
        #meta_role.role = "rolerole"
        #meta_role.name = "rolename"
        #meta_role.photo = "https://pics.javbus.com/actress/ntx_a.jpg"
        metadata.posters[data["Cover"]] = Proxy.Preview(HTTP.Request("https://pics.javbus.com/cover/66oh_b.jpg").content)
        #metadata.art = Proxy.Preview(HTTP.Request(self.data["Samples"][0]).content)
