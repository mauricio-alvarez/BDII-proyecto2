from main import Spimi

spimi = Spimi()

dictWords = {}
dictDocs = {}
dictWords = spimi.loadDict("dictWord.txt","texto")
dictDocs = spimi.loadDict("dictDocs.txt","texto")

spimi.indexNewDocuments('arxiv-metadata-oai-snapshot.json',dictDocs, dictWords)
spimi.saveDict(dictWords, "dictWord.txt","texto")
spimi.saveDict(dictDocs, "dictDocs.txt","texto")