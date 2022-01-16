# Naman and Navya Mishra
# extract everything from an extreme left wing and extreme right wing source and then compare the source to them
# the topics must be same or similar for most accuracy

# first put the web scraping tools in place
import spacy
import re
import requests
import pandas as pd
from bs4 import BeautifulSoup
from string import punctuation

# user input a left leaning source and check if it's from our approved list
# user input a right leaning source and check if it's from our approved list
# the lefist and righty source banks are based on recently update confirmed media with clear political leaning
# as times change, these banks can be changed. we're just trying to use extremes as the boundary points
from spacy.tokens import Doc

print("Please enter the link to a Left-leaning source with the 'https://':")
left = str(input())
while left.startswith("https://") == False:
    print("Please enter the link to a Left-leaning source with the 'https://':")
    left = str(input())
leftsourcesbank = ["nytimes", "washingtonpost", "usatoday", "buzzfeed", "motherjones",
                   "vox", "cnn", "huffpost", "newyorker", "theatlantic", "cbsnews"]

for item in leftsourcesbank:
    if item in left:
        vars = 0
        break
    else:
        vars = 1

while vars == 1:  # don't let user pass left source until they put in a valid one
    print("Please enter a link from a verified source:")
    print(leftsourcesbank)
    left = str(input())
    for item in leftsourcesbank:
        if item in left:
            vars = 0
            break
        else:
            vars = 1

        # user input a right leaning source and check if it's from our approved list
print("Please enter the link to a Right-leaning source with the 'https://':")
right = str(input())
while right.startswith("https://") == False:
    print("Please enter the link to a Right-leaning source with the 'https://':")
    right = str(input())
rightsourcesbank = ["foxnews", "drudgereport", "breitbart", "dailymail", "dailywire",
                    "theepochtimes", "theamericanconservative", "sfexaminer",
                    "washingtontimes", "theblaze", "spectator"]

for item in rightsourcesbank:
    if item in right:
        vars = 0
        break
    else:
        vars = 1

while vars == 1:  # don't let user pass right source until they put in a valid one
    print("Please enter a link from a verified source:")
    print(rightsourcesbank)
    right = str(input())
    for item in rightsourcesbank:
        if item in right:
            vars = 0
            break
        else:
            vars = 1
# once the parameter sources are put in, calculate their buzzword to normal word ratio
# calculate similarity to eachother
buzzwords = ["working class", "red state", "blue state", "career politician", "socialism",
             "capitalism", "radical", "fascist", "patriot", "elites", "triggered",
             "fake news", "microaggression", "racism", "white privilege",
             "white fragility", "white supremacy", "implicit bias", "oppression",
             "identity politics", "social construct", "power structure", "alt-right", "alt right",
             "gamergate", "sjw", "social justice warrior", "nazi", "white genocide", "libtard",
             "globalism", "trump", "president", "obama", "clinton", "hillary", "campaign",
             "media", "police", "republican", "police", "black", "election", "russia",
             "cnn", "fox", "twitter", "facebook", "fox", "administration", "national",
             "investigation", "attack", "immigration", "voter", "protester", "violence"]


# we took this list from https://www.researchgate.net/figure/Top-100-Keyword-Features-Extracted-from-the-English-Fake-News-Data-Set_tbl2_347563252
# most of it anyway. this part of the code can be modified so that you can use a list from a separate file and import it in list format
# that way you can have some sort of ai generator or something picking up more words fake news likes to use
# count words of the source before checking for buzzwords for the ratio

def numWords(url):
    r = requests.get(url, allow_redirects=False)
    soup = BeautifulSoup(r.text, 'html.parser')
    data = ''
    text = ""
    for data in soup.find_all("p"):
        text += (data.get_text())
    nopunct = re.sub("[^\w\s]", "", text)  # remove all punctuation
    wrdlist = nopunct.split()  # split words by space
    if (len(wrdlist)) > 0:
        return (len(wrdlist))  # tha's how many words in the list from the text
    else:
        print("The following source could not be accurately loaded:" + url)
    # independently works now


# I don't know HTML so let's hope I'm looking in the right places
def buzzOccur(url, wordlist):
    r = requests.get(url, allow_redirects=False)
    soup = BeautifulSoup(r.text, 'html.parser')
    data = ''
    text = ""
    counter = 0
    for data in soup.find_all("p"):
        text += (data.get_text())
    nopunct = re.sub("[^\w\s]", "", text)  # remove all punctuation
    q = nopunct.lower()
    for word in wordlist:
        counter += q.count(word)
    return (counter)


# count how many times any of the buzzwords were used
# works individually as long as the text is in the html text segment and the page loads


leftwords = numWords(left)
leftbuzz = buzzOccur(left, buzzwords)
leftratio = leftbuzz / leftwords

rightwords = numWords(right)
rightbuzz = buzzOccur(right, buzzwords)
rightratio = rightbuzz / rightwords

# smilarity checker
nlp = spacy.load("en_core_web_lg")


def simFormat(url):
    r = requests.get(url, allow_redirects=False)
    soup = BeautifulSoup(r.text, 'html.parser')
    data = ''
    for data in soup.find_all("p"):
        return (data.get_text())


lefttext = nlp(simFormat(left))
righttext = nlp(simFormat(right))

# these two numbers should be the same but we need them separate for later possibly
leftsimilarity = lefttext.similarity(righttext)
rightsimilarity = righttext.similarity(lefttext)

buzzavg = (leftbuzz + rightbuzz) / 2  # for the exception case

# get the unknown resources for the comparison
print("How many sources would you like to compare? Please enter an integer:")
number = (input())
while number.isnumeric() == False or int(number) < 1:
    print("How many sources would you like to compare? Please enter an integer:")
    number = (input())
number = int(number)
unkn = {}
for i in range(1, number + 1):
    print("Please enter the link to your source with the 'https://':")
    cake = str(input())
    while cake.startswith("https://") == False:
        print("Please properly enter the link to your source with the 'https://':")
        cake = str(input())
    unkn["unkn" + str(i)] = cake
# created a dictionary so i dont accidentally overwrite

buzzdict = {}  # creating a dictionary of the unknown sources' buzzword ratio
# first test to see if we should even check for legitimacy
for source in unkn:
    xx = buzzOccur(unkn[source], buzzwords)
    yy = numWords(unkn[source])
    if (xx / yy) <= buzzavg:
        buzzdict["unkn" + str(source)] = unkn[
            source]  # this separate dictionary will go through to the similarity checker
    else:
        print(unkn[
                  source] + " uses a lot of langauge often associated with Fake News/ Propoganda. This source is not recommended.")
        # according to the paper we used to make the buzzword list, an AI sniffed out that those words were most common in fake news
        # idk about research what exact percentage of those words makes the news fake so this is kind of arbitrary
        # so the buzzavg number can be adjusted if someone with those fancy AIs wants to share
        # the concept will still be the same
# now we check if the remaining sources are closer to the one with more or less buzzwords
# if they are closer to the one with less buzzwords, they are likely better sources

if rightratio > leftratio:
    better = lefttext
    worse = righttext
elif leftratio > rightratio:
    better = righttext
    worse = lefttext
else:
    if leftsimilarity > 0.5:  # or right doesnt matter because they should be same number. again this is arbitrary because we don't know how similar they should be to consider both sources consistent
        print("Out of the remaining sources, we are unable to determine any heavy bias or any attempts at deliberate attempts to spread Fake News/ Propoganda.")
    else:
        print("There are no reliable sources to compare the remaining sources against.")

# if both sources use similar amount of buzzwords, then the jargon for the topic could be similar or both are lying to get you.

# now we get to the actual similarity checker
for things in buzzdict:
    bb = better.similarity(nlp(simFormat(buzzdict[things])))
    ww = worse.similarity(nlp(simFormat(buzzdict[things])))
    if bb > ww:
        print(buzzdict[things] + " is closer in content similarity to the seemingly more credible News Source.")
    elif ww > bb:
        print(buzzdict[
                  things] + " is closer in content similarity to the seemingly less credible News Source. Procceed with caution.")
    else:
        print(buzzdict[
                  things] + " is equally similar to both the seemingly more credible and the seemingly less credible sources. Procceed with caution.")

# and there we have it. a general framework for if you should read a source or not. but in the end, this is merely a suggestion

