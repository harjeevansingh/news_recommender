from bs4 import BeautifulSoup
import urllib.request,sys,time
import requests
import pandas as pd

# Other news pages
# https://www.newindianexpress.com/world
# https://www.indiatoday.in/world?page=4
# https://www.deccanchronicle.com/world/asia?pg=2

# News with " Load More"
# https://www.npr.org/sections/world/archive



pagesToGet = 10000
sr_no = 1
upperframe = []
filename = "NEWS.csv"
f = open(filename, "a", encoding='utf-8')
headers = "Id,Title,Summary,Date,Link,\n"
f.write(headers)

for page in range(1, pagesToGet+1):
    print('processing page :', page)
    url = 'https://www.deccanchronicle.com/world/americas?pg=' + str(page)
    print(url)

    # an exception might be thrown, so the code should be in a try-except block
    try:
        # use the browser to get the url. This is suspicious command that might blow up.
        page = requests.get(url)  # this might throw an exception if something goes wrong.

    except Exception as e:  # this describes what to do if an exception is thrown
        error_type, error_obj, error_info = sys.exc_info()  # get the exception information
        print('ERROR FOR LINK:', url)  # print the link that cause the problem
        print(error_type, 'Line:', error_info.tb_lineno)  # print error info and line that threw the exception
        continue  # ignore this page. Abandon this and go back.
    time.sleep(2)
    soup = BeautifulSoup(page.text, 'html.parser')
    frame = []
    links = soup.find_all('div', attrs={'class': 'col-sm-12 SunChNewListing'})
    print(len(links))

    for j in links:

        news_id = str(sr_no)
        title = j.find("div", attrs={'class': 'col-sm-8'}).find('h3').text.strip()
        Link = "https://www.indiatoday.in"
        Link += j.find("div", attrs={'class': 'col-sm-8'}).find('a')['href'].strip()
        Date = j.find('span', attrs={'class': 'SunChDt2'}).text[0:11].strip()
        try:
            summary = j.find("div", attrs={'class': 'OpinionStrapList'}).text.strip()
            #print(title)
        except:
            summary = " "
        #Source = j.find('div', attrs={'class': 'm-statement__meta'}).find('a').text.strip()
        #Label = j.find('div', attrs={'class': 'm-statement__content'}).find('img',
        #                                                                   attrs={'class': 'c-image__original'}).get(
        #    'alt').strip()
        frame.append((news_id,title,summary,Date,Link))
        f.write(news_id.replace(",", "^") + "," + title.replace(",", "^") + "," + summary.replace(",", "^") + "," +
                Date.replace(",", "^") + "," + Link + "\n")
        sr_no += 1

    upperframe.extend(frame)
f.close()
data = pd.DataFrame(upperframe, columns=['Id', 'Title', 'Summary', 'Date', 'Link'])
print(data.head(20))
