# -*- coding: utf-8 -*-
"""
Created on Sun Aug 11 19:42:18 2019

@author: alber
"""
import requests

class Telegram():
    
    def __init__(self):
        self.__BASEURL = "https://api.telegram.org/bot"
        self.__TOKEN = "663289094:AAHWT65WGo2MbmJMojS1W1pAgoJy8b9onPI"
        self._url_send_message = self.__BASEURL + self.__TOKEN + "/sendMessage?chat_id={}&parse_mode=Markdown&text={}"
        self._channels = {"Testing": -1001309824846}
    
    def sendMessage(self, sport, msg):
        id_chat = self._identifyChannel(sport).id_chat
        url = self._url_send_message.format(id_chat, msg)
        status = requests.get(url)
        
        return status.json()
    
    def _identifyChannel(self, sport):
        return self._channels[sport]
    
    def getFullChat(self, id_chat):
        result = requests.get(self.__BASEURL + self.__TOKEN + '/getUpdates').json()
        
        return result

    def getAllMembersByChat(self):
        pass
    
    




        
    
    