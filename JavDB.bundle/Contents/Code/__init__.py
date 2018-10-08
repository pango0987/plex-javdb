LANGUAGES = [
             Locale.Language.English, Locale.Language.Czech, Locale.Language.Danish, Locale.Language.German,
             Locale.Language.Greek, Locale.Language.Spanish, Locale.Language.Finnish, Locale.Language.French,
             Locale.Language.Hebrew, Locale.Language.Croatian, Locale.Language.Hungarian, Locale.Language.Italian,
             Locale.Language.Latvian, Locale.Language.Lithuanian, Locale.Language.Dutch, Locale.Language.Norwegian,
             Locale.Language.Polish, Locale.Language.Portuguese, Locale.Language.Russian, Locale.Language.Slovak,
             Locale.Language.Swedish, Locale.Language.Thai, Locale.Language.Turkish, Locale.Language.Vietnamese,
             Locale.Language.Chinese, Locale.Language.Korean
            ]

####################################################################################################
def Start():
  pass

def AppendSearchResult(results, id, name=None, year=-1, score=0, lang=None):

  new_result = dict(id=str(id), name=name, year=int(year), score=score, lang=lang)

  if isinstance(results, list):

    results.append(new_result)

  else:

    results.Append(MetadataSearchResult(**new_result))


####################################################################################################
class JAVDbAgent(Agent.Movies):

  name = 'JAV DB'
  languages = LANGUAGES
  primary_provider = True
  fallback_agent = False
  accepts_from = None
  contributes_to = None

  def search(self, results, media, lang, manual):
      if isinstance(results, list):
          results.append(new_result)
      else:
          results.Append(MetadataSearchResult(**new_result))
      results.Append(dict(id="id", name=media.name, year=2018, score=100, lang=Locale.Language.English))

  def update(self, metadata, media, lang, force):
      for attr_name, attr_obj in metadata.attrs.iteritems():
          if attr_name is "studio":
              attr_obj.setcontent("Studio Test")
          if attr_name is "year":
              attr_obj.setcontent(2018)
          if attr_name is "title":
              attr_obj.setcontent("title Test")
          if attr_name is "summary":
              attr_obj.setcontent("summary...... Test")
          if attr_name is "original_title":
              attr_obj.setcontent("original_title Test")

####################################################################################################
