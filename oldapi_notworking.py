# this file will get data: video, comments, title of reddit post

# imports
import subprocess
import json
from bs4 import BeautifulSoup
import requests
import sys
import os


class Data:
    def __init__(self, url):
        self.url = url
    
    def extract(self):
        headers = {'User-Agent':'Mozilla/5.0'}
        response = requests.get(self.url, headers = headers)

        post_id = self.url[self.url.find('comments/') + 9:]
        post_id = f"t3_{post_id[:post_id.find('/')]}"


        if(response.status_code == 200):    # checking if the server responded with OK
            soup = BeautifulSoup(response.text,'lxml')
            # I looked up the original code of the reddit page 
            # to find where all the data was and it was in a script tag
            # with the id set to 'data'
            required_js = soup.find('script',id='data') 
            print(response.text)
            c = 0
            if required_js == None:
                while required_js == None:
                    required_js = soup.find('script',id='data') 
                    c += 1
                    if c > 50:
                        print('NONE soup after 5 tries')
                        break
            else:
                
                #print('required', required_js)
                json_data = json.loads(required_js.text.replace('window.___r = ','')[:-1])
                #json_data = json.loads(required_js.text)
                #print('json',json_data)
                # 'window.___r = ' and a semicolon at the end of the text were removed
                print(json_data)
                with open('json.json', 'w') as file:
                    file.write(str(json_data))
                    print('Title text saved')
                # to get the data as json
                title = json_data['posts']['models'][post_id]['title']
                title = title.replace(' ','_')
                dash_url = json_data['posts']['models'][post_id]['media']['dashUrl']
                height  = json_data['posts']['models'][post_id]['media']['height']
                dash_url = dash_url[:int(dash_url.find('DASH')) + 4]
                # the dash URL is the main URL we need to search for
                # height is used to find the best quality of video available
                video_url = f'{dash_url}_{height}.mp4'    # this URL will be used to download the video
                audio_url = f'{dash_url}_audio.mp4'    # this URL will be used to download the audio part

                parent_dir = '/Users/tanishsurana/Reddit-yt/'
                directory = title.split()[1]


                path = os.path.join(parent_dir, post_id)
                
                os.mkdir(path)
                print("Directory '% s' created" % directory)

                with open(f'{title}_video.mp4','wb') as file:
                    print('Downloading Video...',end='',flush = True)
                    response = requests.get(video_url,headers=headers)
                    if(response.status_code == 200):
                        file.write(response.content)
                        print('\rVideo Downloaded...!')
                    else:
                        print('\rVideo Download Failed..!')

                with open(f'{title}_audio.mp3','wb') as file:
                    print('Downloading Audio...',end = '',flush = True)
                    response = requests.get(audio_url,headers=headers)
                    if(response.status_code == 200):
                        file.write(response.content)
                        print('\rAudio Downloaded...!')
                    else:
                        print('\rAudio Download Failed..!')
                    

                subprocess.call(['ffmpeg','-i',f'{title}_video.mp4','-i',f'{title}_audio.mp3','-map','0:v','-map','1:a','-c:v','copy',f'{title}.mp4'])
                subprocess.call(['rm',f'{title}_video.mp4',f'{title}_audio.mp3'])

                with open(f'{title}_text.txt', 'w') as file:
                    file.write(title)
                    print('Title text saved')
                    # TODO: NEED TO HANDLE COMMENTS
                    

        else:
            print('Response not okay', response.status_code)


link = 'https://www.reddit.com/r/nextfuckinglevel/comments/14hycay/guy_discovered_new_talent_and_it_does_good/'
files = Data(link)

files.extract()

