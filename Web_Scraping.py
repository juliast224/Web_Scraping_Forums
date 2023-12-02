import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import re
import string
from time import sleep
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from textblob_de import TextBlobDE
from collections import Counter

URL = '' 
"""
insert URL to be scraped https://www.motor-talk.de/forum/vw-id-familie-b1085.html?page= (ID3), https://www.motor-talk.de/forum/vw-golf-7-golf-sportsvan-b848.html?page=“ (Golf 7), https://www.motor-talk.de/forum/tesla-model-3-und-model-y-b1068.html?page=“ (Model 3)
"""


df = []
save_links = []
times = []
post_text = []

#scrape the forum overview for all links to the threads and save them in a dataframe
for page in range(1,x): #for x insert the last page number, if the forum has 3 pages it’s 3 then
    result = requests.get(URL + str(page))
    soup = bs(result.text, features="html.parser")
    #links = soup.find("ul", class_="_2DRQIffNCzdlprT-xoye1").find_all("li")
    links = soup.find("ul", class_="_2DRQIffNCzdlprT-xoye1", attrs={'data-test-id': "thread-list"}).find_all("li")
    for tag in links:
        a = tag.find_all('a', attrs={'data-test-id': "thread-list-item"})
        for argument in a:
            href = argument.get('href')
            print(href)
        save_links.append(href)

#create the complete link that sometimes is not scraped correctly
for y, x in enumerate(save_links):
    if re.match(r'^h', x):
        continue
    else:
        x = ('https://www.motor-talk.de' + x)
        save_links[y] = x
sleep(10)

#some links contain a "news" in the path and go to a wrong page --> delete these links
for h in save_links: 
    if "/news/" in h:
        save_links.remove(h)

text = []
link_text = []
wort = []
kontext = []
link_support = []

#go through the list of links and scrape the page numbers on the thread pages, then combine the thread links with the page numbers --> aim of this step is to scrape not just the first page of the thread but all pages
for i in save_links:
    try:
        response = requests.get(i)
        print("gehe auf Post", i)
        if (response.status_code == 200):
            soup = bs(response.content, features="html.parser")
    except Exception as e:
        print('error when accessing', i)
    page_length = str(soup.find("select"))
    x = re.findall('value="(\d+)"', page_length)
    print(x)
    if not x: #if thread doesn't have responses go to next link
        continue
    else:
        number_navigation = list(range(0, (int(x[-1])+1))) #get all page numbers, if more than 10 some are let out 			so need to fill numbers between first and last
        number_navigation_str = [str(h) for h in number_navigation] #transform list elements to strings
        for test in number_navigation_str:
            add = str(i + '?page=')
            link = add + test
            print(link)
            link_support.append(link)

#go through all links and get the post information, test if the post contains a keyword from the innovation or the opinion category
for k in link_support:
    innovation = ["innovation", "idee", "tipp", "verbessern", "verändern", "innovativ"]
    opinion = ["finde", "meine", "denke", "meinung", "feedback"]
    try:
        response = requests.get(k)
        print("gehe auf Post", k)
        if (response.status_code == 200):
            soup = bs(response.content, features="html.parser")
    except Exception as e:
        print('error when accessing', k)
    thread = soup.find_all("div", class_="_22gqRdhfhkURJPtZ2c2vS", attrs={'itemprop': 'text'})
    for e in thread:
        hasQuote = e.find("blockquote")
        if not hasQuote is None:
            hasQuote.extract()
        postinfo = [str(e.get_text(strip=True))]
        for word in postinfo:
            if any(x in word for x in innovation):
                print("Wort aus Innovation ist enthalten in: ", k)
                print(word)
                wort.append(word)
                link_text.append(k)
                kontext.append('Innovation')
            else:
                continue
            if any(x in word for x in opinion):
                print("Wort aus Meinung ist enthalten in: ", k)
                print(word)
                wort.append(word)
                link_text.append(k)
                kontext.append('Meinung')
            else:
                continue
        post_text.append(postinfo)
        

#save the posts in a dataframe and excel
df = pd.DataFrame({'Links': link_text,
                   'Satz': wort,
                   'Kontext': kontext})
#improve the df
df['Wort'] = ''
df_unique = df.drop_duplicates(subset=['Satz', 'Kontext']) #remove dublicates from excel list

df_unique.to_excel("results11.xlsx")


"""
Text Analyse
"""

#create a string out of the list "postinfo"
str_postinfo = ','.join(str(v) for v in post_text)

#convert text to lowercase
text = str_postinfo.lower()

#remove numbers, hyphens, punctuation and whitespaces
text_clean = re.sub(r'\d+', '', text)
text_clean1 = re.sub('-\n', '', text_clean)
text_clean2 = text_clean1.translate(str.maketrans("", "", string.punctuation))
text_clean3 = text_clean2.strip()

#Tokenize text and remove stopwords
stop_words = set(stopwords.words('german'))
stop_words.update('id')
tokens = word_tokenize(text_clean3)
result = [i for i in tokens if not i in stop_words]

#create bigrams
bigrams_full_text = list(nltk.bigrams(result))
counts_bigrams = Counter(bigrams_full_text)
#print(bigrams_full_text)
print(counts_bigrams.most_common(30))

#lemmatizing the text
lemmatizer = WordNetLemmatizer()
for word in result:
    lemmatizer.lemmatize(word)

#count the words and the unique words
word_freq = Counter(result)
common_words = word_freq.most_common(50)
print(common_words)
#print(word_freq)

#sentiment, polarity analysis
str_result = ' '.join(result)
sentiment = TextBlobDE(str_result).sentiment.subjectivity
print(sentiment)
polarity = TextBlobDE(str_result).sentiment.polarity
print(polarity)
