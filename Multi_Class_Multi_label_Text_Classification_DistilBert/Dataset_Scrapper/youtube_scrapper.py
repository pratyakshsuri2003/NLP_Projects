# Copyright (c) [2023] [PRATYAKSH SURI]
# Unauthorized use, reproduction, or copying is prohibited.

import json
import time
import pandas as pd
import requests
from bs4 import BeautifulSoup
import concurrent.futures
from youtubesearchpython import *

# Suppress insecure request warnings
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

# Define the YouTube video info API endpoint
GET_VIDEO_INFO_API = "https://www.youtube.com/watch?v="

# List of keywords for searching
keyword_list = [
    "sutta",
    "ganja",
    # Add more keywords here
]

def retrieve_video_data(video_id_):
    video_data = []
    video_url = GET_VIDEO_INFO_API.format(video_id_)
    
    # Define headers for making the request
    headers = {
        'X-Crawlera-profile': 'desktop',
        'X-Crawlera-cookies': 'disable',
        # Add any other headers you need here
    }

    # Make a request to get video details
    response = requests.get(video_url, headers=headers, verify=False)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        script = soup.body.find('script')
        script = str(script).replace("<script>", "").replace("<\script>", "")
        from_ = script.find("{") 
        to_ = script.rfind("}")
        output_df = json.loads(script[from_:to_ + 1])
        
        # Check if 'videoDetails' is present in the response
        videodetails_present = "videoDetails" in output_df
        
        if videodetails_present:
            status = output_df['playabilityStatus']['status'] if 'status' in output_df['playabilityStatus'] else ""
            if status == "OK":
                status = "Active"
            else:
                status = "Not Active"
            
            try: 
                title = output_df['videoDetails']['title']
            except:
                # Fallback to scraping the title from the video page if not found in JSON
                page = requests.get(video_url)
                soup = BeautifulSoup(page.content, 'html.parser')
                title = soup.find("meta", itemprop="name")['content']
            
            # Retrieve other video details
            owner_channel_name = output_df['microformat']['playerMicroformatRenderer']['ownerChannelName']
            category = output_df['microformat']['playerMicroformatRenderer']['category']
            tags = output_df['videoDetails']['keywords']
            thumbnail = output_df['videoDetails']['thumbnail']['thumbnails']
            channel_id = output_df['videoDetails']['channelId']
            description = output_df['videoDetails']['shortDescription']
            length_seconds = output_df['videoDetails']['lengthSeconds']
            
            # Fallback to scraping view count if not found in JSON
            try:
                view_count = output_df['videoDetails']['viewCount']
            except:
                page = requests.get(video_url)
                soup = BeautifulSoup(page.content, 'html.parser')
                view_count = soup.find("meta", itemprop="interactionCount")['content']
            
            publish_date = output_df['microformat']['playerMicroformatRenderer']['publishDate']
            upload_date = output_df['microformat']['playerMicroformatRenderer']['uploadDate']
            author = output_df['videoDetails']['author']
            is_private = output_df['videoDetails']['isPrivate']
            is_unplugged_corpus = output_df['videoDetails']['isUnpluggedCorpus']
            is_live_content = output_df['videoDetails']['isLiveContent']
            thumb = json.dumps(str(thumbnail))
            
            inserted_datetime = str(time.strftime('%Y-%m-%d %H:%M:00', time.localtime(time.time())))
            
            video_data.append((video_url, video_id_, status, channel_id, owner_channel_name,
                                category, view_count, title, publish_date, ','.join(tags), description,
                                length_seconds, upload_date, author, is_private, is_unplugged_corpus,
                                is_live_content, thumb, inserted_datetime))
    
    return video_data

def main():
    video_data = []
    
    # Iterate through the list of keywords
    for keyword in keyword_list:
        search = CustomSearch(keyword, VideoSortOrder.relevance, region="IN")
        try:
            res = search.result()
            for video in res["result"]:
                video_data.append(retrieve_video_data(video["id"]))
            search.next()
        except Exception as e:
            print(f"Error searching for keyword '{keyword}': {str(e)}")
            continue
    
    # Flatten the data (since each inner list contains a list)
    flat_data = [item for sublist in video_data for item in sublist]

    # Define columns for the DataFrame
    columns_list = ['video_url', 'video_id_', 'status', 'channel_id', 'owner_channel_name', 'category', 'view_count',
                    'title', 'publish_date', 'tags', 'description', 'length_seconds', 'upload_date', 'author',
                    'is_private', 'is_unplugged_corpus', 'is_live_content', 'thumb', 'inserted_datetime']

    # Create a DataFrame
    df_new = pd.DataFrame(flat_data, columns=columns_list)
    
    # Save the DataFrame to a CSV file
    df_new.to_csv("illegal_drugs_e-vaping_alcohol_category_data.csv", index=False)
    
    # Display the DataFrame
    print(df_new)

if __name__ == '__main__':
    main()
