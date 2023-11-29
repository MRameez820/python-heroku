# Shamelessly copied from http://flask.pocoo.org/docs/quickstart/

from flask import Flask, render_template,request
import requests

app = Flask(__name__)


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
      
    
@app.route("/<string:name>/")
def say_hello(name):
    return f"Hello {name}!"
    

if __name__ == '__main__':
    app.run()

