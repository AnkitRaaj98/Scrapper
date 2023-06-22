from flask import Flask,render_template, request,jsonify
from flask_cors import CORS,cross_origin
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq

app = Flask(__name__)

@app.route("/", methods = ['GET'])
def homepage():
    return render_template("index.html")

@app.route("/review" , methods = ['POST' , 'GET'])

def index():
    if request.method == 'POST':
        try:
            searchString = request.form['content'].replace(" ","")
            flipkart_url = "https://www.flipkart.com/search?q=" + searchstring
            urlclient = uReq(flipkart_url)
            flipkartPage = urlclient.read()
            urlclient.close()
            flipkart_html = bs(flipkart, "html.parser")
            bigboxes = flipkart_html.findAll("div" , {"class":"_1AtVbE col-12-12"})
            del bigboxes[0:3]
            box = bigboxes[0]
            productlink = "https://www.flipkart.com"+box.div.div.div.a['href']
            productreq = requests.get(productlink)
            productreq.encioding='utf-8'
            prod_html = bs(productreq.text,"html.parser")
            print(prod_html)
            comment_box = prod_html.findAll("div", {"class" : "_16PBlm"})

            filename = searchString + ".csv"
            fw = open(filename, "w")
            headers = "Product, Customer Name, Rating, Heading, Comment \n"
            fw.write(headers)
            reviews = []
            for commentbox in commentboxes:
                try:
                   name = comment_box.div.div.find_all("p" , {"class" :"_2sc7ZR _2V5EHH"})[0].text

                except:
                    name = 'No Name'

                try:
                    rating = commentbox.div.div.div.div.text

                except:
                    rating = 'No Rating'
                    
                try:
                    commentHead = 'No Comment Heading'

                except:
                     Exception
                try:
                    comtag = comment_box.div.div.find_all("div" , {"class" : ""})

                    custComment = comtag[0].div.text
                except Exception as e:
                    print("Exception while creating dictionary: ",e)

                mydict = {"Product": searchString, "Nmae": name, "Rating":rating, "CommentHead": commentHead,
                          "Comment": custComment}
                review.append(mydict)
            return render_template('results.html', reviews=reviews[0:(len(reviews)-1)])
        except Exception as e:
            print('The Exception message is: ',e)
            return 'something is wrong'


        else:
            return render_template('index.html')

if __name__=="__main__":
    app.run(host="0.0.0.0")
