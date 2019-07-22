# -*- coding: utf-8 -*-
"""
Created on Fri Jul 19 19:43:36 2019

@author: AlbertVillarOrtiz
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time

def getClasifications(matchDriver, idMatch, situation):
    print("CLASIFICATION: " + situation)
    url = "https://www.mismarcadores.com/partido/{}/#clasificacion;table;{}".format(idMatch, situation)
    matchDriver.get(url)
    print("LINK: " + url)
    time.sleep(2) 
    data = matchDriver.find_elements_by_xpath("//tr[contains(@class, 'highlight') and not(contains(@class, 'highlights'))]")
    for i in range(len(data)):
        value = data[i].text
        if len(value) != 0:
            print(value)
        
def getMatchs(matchDriver, idMatch, situation):
    print("MATCHS: " + situation)
    url = "https://www.mismarcadores.com/partido/{}/#h2h;{}".format(idMatch, situation)
    matchDriver.get(url)
    print("LINK: " + url)
    time.sleep(2) 
    
    showMores = matchDriver.find_elements_by_xpath("//a[contains(@class, 'show_more')]")
    if situation == "overall":
        size = len(showMores) if (len(showMores) <= 3) else 3;
    else: 
        size = len(showMores) if (len(showMores) <= 2) else 2;
    
    print("SIZE: " + str(size) + " SHOWMORES: " + str(len(showMores)))        
    for i in range(size):
        if len(showMores[i].text) != 0:    
            print("TAG: " + showMores[i].text + " SIZE: " + str(len(showMores[i].text)))
            time.sleep(.1)
            showMores[i].click()
            time.sleep(.1)
        
    data = matchDriver.find_elements_by_class_name('highlight')
    for i in range(len(data)):
        value = data[i].text
        if len(value) != 0:
            print(value)
    
        
option = webdriver.ChromeOptions()
main = webdriver.Chrome(executable_path= 'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
match = webdriver.Chrome(executable_path= 'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')

main.get('https://www.mismarcadores.com/beisbol/usa/mlb/partidos/')
partidos = main.find_elements_by_class_name('event__match')

#############
SITUATIONS = ['overall', 'home', 'away']

clasi = {
        'position': 0,
        'positionAsSide': 0
}

matchs = {
        'winsLast10': 0,
        'totalLast10': 0,
        'totalAt5Last10': 0,
        'winsAsSideLast10': 0,
        'totalAsSideLast10': 0,
        'totalAt5AsSideLast10': 0,
        'winsH2HLast10': 0,
        'totalH2HLast10': 0,
        'totalAt5H2HLast10': 0}
    

for i in range(1):
    idMatch = partidos[i].get_attribute("id")
    index = idMatch.rfind('_')
    
    for situation in SITUATIONS:
        #getClasifications(match, idMatch[index+1:], situation)
        getMatchs(match, idMatch[index+1:], situation)          
        time.sleep(2)

main.quit()
match.quit()
    

