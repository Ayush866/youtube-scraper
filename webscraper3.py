from selenium import webdriver
import time
from flask import Flask, render_template, request,jsonify
from flask_cors import CORS,cross_origin
from selenium.webdriver.chrome.options import Options

app = Flask(__name__)

@app.route('/',methods=['GET'])  # route to display the home page
@cross_origin()
def homePage():
    return render_template("index.html")

@app.route('/review',methods=['POST','GET']) # route to show the review comments in a web UI
@cross_origin()
def index():
    if request.method == 'POST':
            youtuber_name = request.form['content'].replace(" ","")
            baseurl = "https://www.youtube.com/results?search_query={}".format(youtuber_name)
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            driver = webdriver.Chrome(chrome_options=chrome_options)
            driver.implicitly_wait(3)
            driver.get(baseurl)
            time.sleep(5)
            link = driver.find_element_by_xpath(".//*[@id='text']/a").get_attribute("href")
            driver.get(f"{link}/videos?view=0&sort=p&flow=grid")
            driver.execute_script("window.scrollBy(0, document.body.scrollHeight);")
            time.sleep(5)
            channel_name = driver.find_element_by_xpath('.//*[@id="channel-name"]').text
            viedos = driver.find_elements_by_class_name("style-scope ytd-grid-video-renderer")
            viedo_list = []
            thumbnail = []
            i=1
            for viedo in viedos:
                if i>10:
                    break
                else:
                    titles = viedo.find_element_by_xpath(".//*[@id='video-title']").text
                    views = viedo.find_element_by_xpath('.//*[@id="metadata-line"]/span[1]').text
                    uploaded = viedo.find_element_by_xpath('.//*[@id="metadata-line"]/span[2]').text
                    viedo_link = viedo.find_element_by_xpath('.//*[@id="thumbnail"]').get_attribute("href")
                    image = viedo.find_element_by_xpath('.//*[@id="img"]').get_attribute("src")
                    vido_dict = {
                        "titles": titles,
                        "upload_date": uploaded,
                        "views": views,
                        "link": viedo_link,
                        "image_link": image
                    }
                    viedo_list.append(vido_dict)
                    i+=1

            return render_template('results.html', reviews=viedo_list[0:(len(viedo_list)-1)],name=channel_name)


    else:
        return render_template('index.html')








if __name__ == "__main__":
    app.run(debug=True)


#style-scope ytd-grid-video-renderer

#//*[@id="video-title"]
#//*[@id="metadata-line"]/span[1]
#//*[@id="metadata-line"]/span[2]
#.//*[@id='info-section']/a
#//*[@id="thumbnail"]
#//*[@id="img"]
#//*[@id="text"]
