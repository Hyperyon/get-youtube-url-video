# -*- coding:Utf-8 -*-
import urllib2 as get
import time as t
import json

dir = 'the_path_of_directory'
api_key = 'AIzaSyAXsj8DMG3qWgwKtbwvX1idlBxxxxxxxxx'
id_channel = 'UC72lswiocu5Asjt6j9RWh7A'
base_url = 'http://www.youtube.com/watch?v='

base = ['https://www.googleapis.com/youtube/v3/search?part=snippet&channelId=',
        '&maxResults=50&order=date',
        '&pageToken=',
        '&fields=items(id%2Csnippet)%2CnextPageToken&key='+api_key]


def get_channel(): #from file
    with open(dir+'chaine.txt', 'r') as f:data=f.read().split('\n')
    url = data[0]
    data = '\n'.join(data[1:] + data[:1])
    with open(dir+'chaine.txt', 'w') as f:f.write(data)
    return url

def get_id_channel(url):
    id_channel = get.urlopen(url).read().split('data-channel-external-id="')[1].split('"')[0]
    return id_channel

def get_payload(id_channel):
    payload, title = [], ''
    json_data = json.load(get.urlopen(base[0]+id_channel+base[1]+base[3]))

    while 1:
        for i, element in enumerate(json_data['items']):
            if json_data['items'][i]['id']['kind'] == 'youtube#video':
                a = base_url
                a +=json_data['items'][i]['id']['videoId'] + ' ' + json_data['items'][i]['snippet']['title']
                payload.append(a)
                print a.encode('Utf-8')

            if json_data['items'][i]['id']['kind'] == 'youtube#channel': title = json_data['items'][i]['snippet']['title']

        if 'nextPageToken' in json_data :
            token = json_data['nextPageToken']
            json_data = json.load(get.urlopen(base[0]+id_channel+base[1]+base[2]+token+base[3]))
        else:
            break #if not next page token, leave loop
        t.sleep(2.5)

    payload.insert(0, '\n\n'+ url+' '+title)
    chaine = '\n'+url+' '+id_channel+' '+title
    with open(dir+'channel.txt', 'a+') as f:data=f.write(chaine.encode('Utf-8'))
    return payload


def check_channel(channel):
    with open(dir+'channel.txt', 'r') as f:data=f.read()
    return True if not channel in data else False


url = get_channel()
if check_channel(url): #check if not exist in file channel.txt
    id_channel = get_id_channel(url)
    data = '\n'.join(get_payload(id_channel))
    with open(dir+'test.txt', 'a+') as f:data=f.write(data.encode('Utf-8'))
