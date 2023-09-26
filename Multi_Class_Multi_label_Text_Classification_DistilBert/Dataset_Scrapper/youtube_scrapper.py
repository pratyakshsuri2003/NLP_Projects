from sqlite3 import Row
from youtubesearchpython import *
from youtubesearchpython import ChannelsSearch, VideoSortOrder, CustomSearch
import requests
import json
import pandas as pd
import traceback
import urllib3
from bs4 import BeautifulSoup
import time
import traceback
import urllib3
import time
from bs4 import BeautifulSoup
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import concurrent.futures

def channel_calling(keyword, channel_id, imp_list):
    for ch_id in channel_id:
        CH_ID = ch_id
        try:
            playlist = Playlist(playlist_from_channel_id(CH_ID))
            res = json.dumps(playlist.videos)
            rrr = json.loads(res)
            del res 
            linit = len(playlist.videos)
            for m in range(7):    
                m_id = rrr[m]["id"]
                imp_list.append((keyword, m_id))
                
        except:
            
            continue
    return

def page1(keyword, video_list):
    search = CustomSearch(keyword, VideoSortOrder.relevance, region="IN")
    for itr in range(1):
        try:
            res = search.result()
            for video in res["result"]:
                video_list.append((keyword, video["id"]))
            search.next()
        except:
            print(traceback.format_exc(),flush=True)
            print(keyword,flush=True)
            continue
    return video_list    
    
def page(keyword, channel_list):
    search = CustomSearch(keyword, VideoSortOrder.relevance, region="IN")
    for itr in range(1):
        try:
            res = search.result()
            for video in res["result"]:
                channel_list.append([keyword, video["id"]])
            del res
            search.next()
        except: 
            print(keyword, flush=True)
            continue
    return channel_list

def search(keywords):
    channel_list = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=12) as executor:
        for keyword in keywords:
            executor.submit(page, keyword=keyword, channel_list=channel_list)
    df_temp = pd.DataFrame(channel_list, columns=['keyword', 'video_id'])
    return df_temp 
        
def relevancy(df) :
    keywords = df['keyword'].str.lower().tolist()
    df_temp = search(keywords) 
    del keywords 
    df_temp.drop_duplicates(subset=['video_id'], inplace=True)
    df['keyword'] = df['keyword'].str.lower()
    df_temp = pd.merge(df_temp, df, on="keyword", how="outer")
    df_temp = df_temp.dropna(subset=["video_id"])
    del df
    return df_temp

def retrieve(video_id_):
    
    video_data = []
    video_url = 'https://www.youtube.com/watch?v={}'.format(video_id_)
    headers = {'X-Crawlera-profile': 'desktop', 'X-Crawlera-cookies': 'disable',
               "Cookie": "VISITOR_INFO1_LIVE=OSHPZSXMW84; PREF=tz=Asia.Kolkata&f1=50000000&al=en&f5=20000&f4=4000000; CONSENT=YES+cb.20210518-05-p0.en-GB+FX+139; NID=206=VKYbgMB9pmuC5jVkvUNnYgZ9ZwZvvmXbK0-xUuEkQ1WmqZTXQa9fj-B27fIUt3IoQqiTGlkCAAi2wH9PcO6vpzUjKCZkyDo8W_4zEf02o5tGD-GoL9mK2rbeMX6q_z9vEr5oYXvGXO-gUJOkrpRAQmSN3n_rYbiYV82wWhh96aM; _ga=GA1.2.2124897624.1610103116; SID=9gfr_SqihtBeI6nXY3P1ZtpSguV-_78geYPXfk4yhJaJY-K5rOr8Ef633c0i-vTPCJKYAQ.; __Secure-3PSID=9gfr_SqihtBeI6nXY3P1ZtpSguV-_78geYPXfk4yhJaJY-K5-FAfer9I8b7j6sRML3fh1Q...dZW2RZWtb6vIqYjDCRg0RlqZ6-IleViQ; __Secure-3PSIDCC=AJi4QfGXBbUfDROcdiOBLXhM1uYFC_wXUKu1nXdaCI6YaxqkfeYyjUwVpGWIjoPbl0fNsDKaHw; LOGIN_INFO=AFmmF2swRgIhAKR8bNEwTHZgJSqnSmxbogJYWMH4dNulHHWVf12z8UbOAiEAq4VzGrcxrU_mLEF-0UvsjOZwz8Ue4J-UcoOf9hX7pfs:QUQ3MjNmd0hHRU5SQmE2T1hGeGl2VDVSVzdIUnNIQmZUcFRDYUNNRFNJQUZBT2tiTThuR0trbkhWY3BLZnFHZ0Uxek5Bck4tUzBWNDJPTkttdW5Tc2dYQnBucHgtbXRUM2FfamJXOFNKT2UwT3ZsMUhCeXZWb2xQMllJeGtlWldORnFscnlPcjZUY19BVVl6Z0NzLUVxa0NLZDhkR3FqZmplSmw0aHI1cXgwSW9iei1KVmlhRmhJ; YSC=Ouk74GIosyg; wide=1"}

    response = requests.get(GET_VIDEO_INFO_API.format(video_id_), headers=headers, verify=False)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        script = soup.body.find('script')
        script = str(script).replace("<script>", "").replace("<\script>", "")
        from_ = script.find("{") 
        to_ = script.rfind("}")
        video_url = 'https://www.youtube.com/watch?v={}'.format(video_id_)
        output_df = json.loads(script[from_:to_ + 1])  
        videodetails_present = "videoDetails" in output_df
        if (videodetails_present == True): 
            status = output_df['playabilityStatus']['status'] if 'status' in output_df['playabilityStatus'] else ""
            if status == "OK":
                status = "Active"
            else:
                status = "Not Active"
            try: 
                title = output_df['videoDetails']['title']
            except:
                page = requests.get(video_url)
                soup = BeautifulSoup(page.content, 'html.parser')
                title = soup.find("meta", itemprop="name")['content']
                print(title, flush=True)
            try:
                owner_channel_name = output_df['microformat']['playerMicroformatRenderer']['ownerChannelName']
            except:
                owner_channel_name = " "
            try:
                category = output_df['microformat']['playerMicroformatRenderer']['category']
            except:
                category = " "
            try: 
                tags = output_df['videoDetails']['keywords']
            except:
                tags = " "
            try:
                thumbnail = output_df['videoDetails']['thumbnail']
                thumb = thumbnail["thumbnails"]
            except:
                thumbnail = " "
                thumb = " "
            try:
                channel_id = output_df['videoDetails']['channelId']
            except:
                channel_id = " "
            try:
                description = output_df['videoDetails']['shortDescription']
            except:
                description = " "
            try:
                length_seconds = output_df['videoDetails']['lengthSeconds']
            except:
                length_seconds = " "
            try:
                view_count = output_df['videoDetails']['viewCount']
            except:
                page = requests.get(video_url)
                soup = BeautifulSoup(page.content, 'html.parser')
                view_count = soup.find("meta", itemprop="interactionCount")['content']
                print(view_count, flush=True)
            try:
                publish_date = output_df['microformat']['playerMicroformatRenderer']['publishDate']
            except:
                publish_date = 'NULL'
            try:
                upload_date = output_df['microformat']['playerMicroformatRenderer']['uploadDate']
            except:
                upload_date = " "
            try:
                author = output_df['videoDetails']['author']
            except:
                author = " "
            try:
                is_private = output_df['videoDetails']['isPrivate']
            except:
                is_private = " "
            try:
                is_unplugged_corpus = output_df['videoDetails']['isUnpluggedCorpus']
            except:
                is_unplugged_corpus = " "
            try:
                is_live_content = output_df['videoDetails']['isLiveContent']
            except:
                is_live_content = " " 
            try:
                is_crawlablekey_ = output_df['videoDetails']['isCrawlable']
            except:
                is_crawlablekey_ = " " 
            inserted_datetime = str(time.strftime('%Y-%m-%d %H:%M:00', time.localtime(time.time())))
            print(video_url)
            video_data.append((video_url, video_id_, status, channel_id, owner_channel_name,
                                category, view_count, title, publish_date, ','.join(tags), description,
                                length_seconds, upload_date, author, is_private, is_unplugged_corpus,
                                is_live_content, json.dumps(str(thumb)), inserted_datetime))
        return video_data

if __name__ == '__main__':
   
    GET_VIDEO_INFO_API = "https://www.youtube.com/watch?v={}"
    keyword_list = [    
    "sutta",
    "ganja",
    "charas",
    "Sharab",
    "Beer",
    "Whiskey",
    "Viski", 
    "Wine",
    "Sharaabi",
    "Liquor",
    "Madira",
    "Drunk",
    "Nasha",
    "Drug",
    "Cocaine",
    "Kokain",
    "Marijuana",
    "Bhang",
    "Heroin",
    "Heroin",
    "Smoking",
    "Dhoomrapaan",
    "Cigarette",
    "Nicotine",
    "Illegal Drugs",
    "Illegal drug trade",
    "Drug trafficking",
    "Drug abuse",
    "Drug addiction",
    "Drug overdose",
    "Tobacco",
    "Cigarettes",
    "Smoking",
    "Tobacco industry",
    "E-cigarettes",
    "Vaping",
    "Vape products",
    "Alcohol",
    "Alcohol consumption",
    "Alcohol addiction",
    "Alcoholism",
]

df = pd.DataFrame({'keyword': keyword_list}) 
relevancy_df = relevancy(df) 
video_ids = relevancy_df['video_id'].to_list() 
video_data = []

for ids in video_ids:
    video_data.append(retrieve(ids))

print(video_data)
print(type(video_data))

columns_list = ['video_url', 'video_id_', 'status', 'channel_id', 'owner_channel_name', 'category', 'view_count','title', 'publish_date', 'tags', 'description', 'length_seconds', 'upload_date', 'author', 'is_private','is_unplugged_corpus','is_live_content', 'thumb', 'inserted_datetime']

# Flatten the data (since each inner list contains a list)
flat_data = [item for sublist in video_data for item in sublist]

# Create a DataFrame
df_new = pd.DataFrame(flat_data, columns=columns_list)
df_new.to_csv(r"illegal_drugs_e-vaping_alcohol_category_data.csv", index=False)

# Display the DataFrame
print(df_new)



