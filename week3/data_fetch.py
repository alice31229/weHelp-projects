import csv
import json
from bs4 import BeautifulSoup
import urllib.request
from urllib.request import urlopen

## Task 1
def get_data_from_url(url):
    try:
        with urlopen(url) as response:
            data = response.read().decode('utf-8')

            return data
        
    except Exception as e:
        print(f"Failed to fetch data from '{url}': {e}")

        return None


# spot
spot = []
spot_data_url = 'https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment-1'
spot_data = get_data_from_url(spot_data_url)
spot_data_json = json.loads(spot_data)
for d in  spot_data_json['data']['results']:
    spot.append({'SERIAL_NO':d['SERIAL_NO'], 
                 'stitle':d['stitle'], 
                 'latitude':d['latitude'], 
                 'longitude':d['longitude'], 
                 'picture':'https'+d['filelist'].split('https')[1]})


# MRT
MRT = []
mrt_data_url = 'https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment-2'
mrt_data = get_data_from_url(mrt_data_url)
mrt_data_json = json.loads(mrt_data)
for d in mrt_data_json['data']:
    MRT.append({'SERIAL_NO':d['SERIAL_NO'], 
                'MRT':d['MRT'], 
                'address':d['address'].split('  ')[1][:3]})


# join spot and MRT by SERIAL_NO
def join_spot_mrt(j1, j2):
    key = {d['SERIAL_NO']: d for d in j2}  
    combined_attractions_info = [d | key.get(d['SERIAL_NO']) for d in j1]

    return combined_attractions_info

joined_data = join_spot_mrt(spot, MRT)

# MRT spots arrange
# StationName,AttractionTitle1,AttractionTitle2,AttractionTitle3,...
# 新北投,新北投溫泉區,北投圖書館,地熱谷,...

mrt_spots_d = {}
for m in joined_data:
    if m['MRT'] not in mrt_spots_d:
        mrt_spots_d[m['MRT']] = [m['stitle']]
    else:
        mrt_spots_d[m['MRT']].append(m['stitle'])


with open('mrt.csv', 'w', newline='') as mrt_csv:
    writer = csv.writer(mrt_csv)
    for ms in mrt_spots_d:
        insert_row = [ms] + mrt_spots_d[ms]
        writer.writerow(insert_row)

# spots info arrange
# SpotTitle,District,Longitude,Latitude,ImageURL
# 新北投溫泉區,北投區,123.5446,24.5312,https://www.travel.taipei/pic/11000848.jpg

with open('spot.csv', 'w', newline='') as spot_csv:
    writer = csv.writer(spot_csv)
    for s in joined_data:
        writer.writerow([s['stitle'],s['address'],s['longitude'],s['latitude'],s['picture']])


####################
## Task 2
# ArticleTitle,Like/DislikeCount,PublishTime
# [問題] 享受輸的感覺539,4,Fri Jul 14 23:34:43 2023

ptt_url_lottery = 'https://www.ptt.cc/bbs/Lottery/index.html'
headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
           "cookie": "over18=1;"}

def get_publish_time(article_url):
    request = urllib.request.Request(article_url, headers=headers)
    resp = urlopen(request)
    html = resp.read()
    soup_publish = BeautifulSoup(html, 'html.parser')

    time = soup_publish.find_all('span', class_='article-meta-value')[-1]
    
    return time.text

def web_scrape_ptt(ptt_url):
    try:
        # Fetch the HTML content of the webpage
        req = urllib.request.Request(ptt_url, headers=headers)
        response = urlopen(req)

        # Read the HTML content
        html_content = response.read()

        # Parse the HTML using BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')

        # Extract all the demand links from ptt_url
        titles = soup.find_all('div', class_ = 'title')
        Y_good = soup.find_all('div', class_ = 'nrec')
        for title_ind in range(len(titles)):
            temp = {}
            #print(titles[title_ind].a['href'])
            if titles[title_ind].a != None:
                temp['ArticleTitle'] = titles[title_ind].text.replace('\n','')
                
                # https://pttpedia.fandom.com/zh/wiki/%E7%9C%8B%E6%9D%BF%E4%BA%BA%E6%95%B8%E3%80%81%E7%9C%8B%E6%9D%BF%E4%BA%BA%E6%B0%A3
                # https://pttpedia.fandom.com/zh/wiki/%E5%99%93%E6%96%87%EF%BC%88%E5%99%93%E7%88%86%EF%BC%89
                if Y_good[title_ind].text == '':
                    temp['Like/DislikeCount'] = 0
                elif Y_good[title_ind].text == '爆':
                    temp['Like/DislikeCount'] = 'Like/DislikeCount>99'
                elif 'X' in Y_good[title_ind].text:
                    temp['Like/DislikeCount'] = 'DislikeCount>10'
                else:
                    temp['Like/DislikeCount'] = Y_good[title_ind].text

                try:
                    temp['PublishTime'] = get_publish_time('https://www.ptt.cc/'+titles[title_ind].a['href'])
                except:
                    temp['PublishTime'] = ''
            
            if temp != {}:
                lottery_info.append(temp)

        next_url = soup.find('a', string='‹ 上頁')
        next_url = 'https://www.ptt.cc'+next_url['href']
        
        return next_url

            
    except Exception as e:
        print("Error:", e)

count = 1
next_url = ''
lottery_info = []
while count < 4:
    if count == 1:
        next_url = web_scrape_ptt(ptt_url_lottery)
    else:
        next_url = web_scrape_ptt(next_url)
    count += 1

with open('articles.csv', 'w', newline='') as articles_file:
    writer = csv.writer(articles_file)
    for a in lottery_info:
        #print(a)
        if a['PublishTime'] != '':
            writer.writerow([a['ArticleTitle'], a['Like/DislikeCount'], a['PublishTime']])
        else:
            writer.writerow([a['ArticleTitle'], a['Like/DislikeCount']])