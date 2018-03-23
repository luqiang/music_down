"""
 搜索类 对目标歌曲在几大平台内进行搜索

"""
import requests
import json
class Search:
    def __init__(self):
         #'http://music.163.com/weapi/song/enhance/player/url?csrf_token='
        self.find163Url = 'http://music.163.com/api/search/get'  #搜索曲目列表
        self.getSong163Url = 'http://music.163.com/weapi/song/enhance/player/url?csrf_token=' #获取歌曲详细的下载地址
    def findSong(self,songName):
        
        self.songName = songName
        """
         模拟浏览器的访问 
        """
        self.headers = {
       
                    'Accept': '*/*',
                    'Accept-Encoding': 'gzip,deflate,sdch',
                    'Accept-Language': 'zh-CN,zh;q=0.8,gl;q=0.6,zh-TW;q=0.4',
                    'Connection': 'keep-alive',
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'Host': 'music.163.com',
                    'Referer': 'http://music.163.com/search/',
                    'User-Agent':
                    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.152 Safari/537.36'
          
                   
                  }

        sendData = {"type":1,"s":self.songName,"limit":1,'offset':0} 
        r = requests.post(self.find163Url,data = sendData,headers=self.headers)
        jsonData = json.loads(r.text)
        if 'code' in jsonData and jsonData['code']==200:
            self.parseData(jsonData['result'])
        else:
            print('解析出错')
    def parseData(self,data):
        songVoArray = []
        songData = data['songs']
        for song in songData:
             songVo = {'down_url':None,'singer':None,'songName':None,'platform':'网易云音乐'}
             songVo['down_url'] = song[''] #歌曲下载地址
             songVo['singer'] = song[''] #歌手名
             songVo['songName'] = song['name'] #歌曲名