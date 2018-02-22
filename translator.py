from bs4 import BeautifulSoup
import urllib.request
import urllib.parse
import re


def translate(word):
    url = "http://www.sanakirja.org/search.php?q=" + word + "&l=6&l2=17"

    req = urllib.request.Request(url)
    resp = urllib.request.urlopen(req)
    respdata = resp.read()
    soup = BeautifulSoup(respdata, "html.parser")
    header = soup.find("th", text="Käännös")
    
    try:
        table_str = str(header.find_parent("table"))
        trans_list = re.findall(">[a-zöäåùàìèòù]+[a-zöäåùàìèòù\s]*<", table_str)
        if len(trans_list) > 6:
            trans_list = trans_list[:6]
        words_string = ""
        
        for word in trans_list:
            word = re.sub("[<>]", "", word)
            words_string += word + ', '
        words_string = words_string[:-2]
        return words_string

    except:
        return "(Translation not found.)"

