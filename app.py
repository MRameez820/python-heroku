# Shamelessly copied from http://flask.pocoo.org/docs/quickstart/

from flask import Flask, render_template,request
import requests
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)
app.url_map.strict_slashes = False

def calculate_similarity(article, phrase):
    vectorizer = TfidfVectorizer()
    # Combine the article and phrase into one list for vectorization
    all_text = [article, phrase]
    # Convert the text to vectors
    tfidf_matrix = vectorizer.fit_transform(all_text)
    # Calculate cosine similarity (returns a matrix)
    similarity_matrix = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
    # The similarity score between the article and the phrase
    similarity_score = similarity_matrix[0][0]
    return similarity_score


def get_html(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # This will raise an exception for HTTP errors
        return response.text
    except requests.RequestException as e:
        print("Error fetching the URL: {e}")
        return None



def findTitle(url):
  html_content = get_html(url)
  beginningTitleIndex = html_content.find("<title>")
  endTitleIndex = html_content.find("</title")
  title = html_content[beginningTitleIndex + 7 : endTitleIndex]
  return title



def analyzePageTitle(title,url):
  titleLength = len(title)
  titleWords = title.split()
  titleWordCount = len(titleWords)
  domainName = url.split('//')[1].split('/')[0]
  lowercaseDomainName = domainName.lower()
  wordsInDomain = []
  for word in titleWords:
    if word.lower() in lowercaseDomainName:
       wordsInDomain.append(word)
  domainCount = len(wordsInDomain)
  finret = "Domain : " + url +  " Title : " + title +  " Title Length : " + str(titleLength) + " Word Count : " + str(titleWordCount) + " Words in domain : " + str(domainCount)
  return finret


def submitclick():
    return 'clicked'

@app.route("/")
def hello():
    url = "https://polygonsmedia.com/"  
    version = findTitle(url)
    message = analyzePageTitle(version,url)
    return render_template('index.html')


@app.route('/results')
def showres():
    domain = request.args.get('domain')
    version = findTitle(domain)
    message = analyzePageTitle(version,domain)
    return render_template('results.html' , value=message)

@app.route('/textresults')
def showsim():
    frsttxt = request.args.get('firsttext')
    lasttxt = request.args.get('secondtext')
    similarity_score = round(calculate_similarity(frsttxt, lasttxt)*100, 2)
    return render_template('sim_results.html' , value=similarity_score)


    

if __name__ == '__main__':
    app.run()

