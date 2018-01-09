# -*- coding: utf-8 -*-
#Библиотеки, които използват python и Kodi в тази приставка
import re
import sys
import os
import urllib
import urllib2
import cookielib
import xbmc, xbmcplugin,xbmcgui,xbmcaddon
import base64

#Място за дефиниране на константи, които ще се използват няколкократно из отделните модули
__addon_id__= 'plugin.video.kidamom'
__Addon = xbmcaddon.Addon(__addon_id__)
__settings__ = xbmcaddon.Addon(id='plugin.video.kidamom')
login = base64.b64decode('aHR0cHM6Ly9raWRhbW9tLmNvbS9sb2dpbg==')
baseurl = base64.b64decode('aHR0cHM6Ly9raWRhbW9tLmNvbQ==')
fol1 = base64.b64decode('aHR0cHM6Ly9raWRhbW9tLmNvbS9hcHBsZS10b3VjaC1pY29uLTE0NC5wbmc=')
fol2 = base64.b64decode('aHR0cHM6Ly9raWRhbW9tLmNvbS9mbHVpZC1pY29uLnBuZw==')
UA = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'
username = xbmcaddon.Addon().getSetting('settings_username')
password = xbmcaddon.Addon().getSetting('settings_password')
access = xbmcaddon.Addon().getSetting('access')
if not username or not password or not __settings__:
        xbmcaddon.Addon().openSettings()
#Инициализация
req = urllib2.Request(login)
req.add_header('User-Agent', UA)
cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
f = opener.open(req)
data = f.read()
match = re.compile('authenticity_token" value="(.+?)"').findall(data)
for token in match:
    params = {'utf8':'✓',
              'authenticity_token':token,
              'authentication[email]': username,
              'authentication[password]': password,
              'authentication[remember_me]': '1',
              'commit':'Вход'
              }
    req = urllib2.Request(login, urllib.urlencode(params))
    req.add_header('User-Agent', UA)
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    f = opener.open(req)
    data = f.read()

#Меню с директории в приставката
def CATEGORIES():
        addDir('Филми', baseurl + '/movies', 1, fol1)
        addDir('Видео Облак', baseurl + '/cloud', 1, fol1)
        addDir('Филми за деца', baseurl + '/kids/movies', 1, fol2)
        if '0' in access:
         url = baseurl + '/kids/series/'
         req = urllib2.Request(url)
         req.add_header('User-Agent', UA)
         opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
         f = opener.open(req)
         data = f.read()
         match = re.compile('<div class="movie-item"><a href="(.+?)"><div class="thumb-holder"><img class="background" src="(.+?).\d+" alt=".+?" /></div><div class="text-holder"><h4 class="name dotted-overflow">(.+?)</h4>').findall(data)
         for link,img,tit in match:
          url = baseurl + link
          thumbnail = baseurl + img
          title = 'Детски Сериал: ' + tit
          addDir(title, url, 1,fol2)

#Разлистване видеата на първата подадена страница
def INDEXPAGES(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', UA)
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        f = opener.open(req)
        data = f.read()
        if '0' in access:
         br = 0
         match = re.compile('<div class="movie-item"><a href="(.+?)">.+?src=.+?original="(.+?).\d+">.+?<h4>(.+?)</h4>').findall(data)
         for link,img,title in match:
          url = baseurl + link
          thumbnail = baseurl + img
          addDir(title,url,3,thumbnail)
          br = br + 1
         if br == 24:  # тогава имаме следваща страница и конструираме нейния адрес
          getpage = re.compile('<li class="current"><a href="">(.+?)</a></li> <li><a rel="next" href="(.+?)page=').findall(data)
          for page,pageurl in getpage:
           newpage = int(page) + 1
           url = baseurl + pageurl + 'page=' + str(newpage)
           addDir('следваща страница>>' + str(newpage), url, 1, 'DefaultFolder.png')
        if '1' in access:
         br = 0
         match = re.compile('>без регистрация</span>.+?<div class="movie-item"><a href="(.+?)">.+?src=.+?original="(.+?).\d+">.+?<h4>(.+?)</h4>').findall(data)
         for link, img, title in match:
          url = baseurl + link
          thumbnail = baseurl + img
          addDir(title, url, 1, thumbnail)
         br = br + 1
         if br >= 1:
           getpage = re.compile('<li class="current"><a href="">(.+?)</a></li> <li><a rel="next" href="(.+?)page=').findall(data)
           for page, pageurl in getpage:
            newpage = int(page) + 1
            url = baseurl + pageurl + 'page=' + str(newpage)
            addDir('следваща страница>>' + str(newpage), url, 1, 'DefaultFolder.png')
         if br == 0:  # тогава имаме следваща страница и конструираме нейния адрес
           getpage = re.compile('<li class="current"><a href="">(.+?)</a></li> <li><a rel="next" href="(.+?)page=').findall(data)
           for page, pageurl in getpage:
            newpage = int(page) + 1
            newurl = baseurl + pageurl + 'page=' + str(newpage)
            INDEXPAGES(newurl)

def INDEXOBLAK(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', UA)
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        f = opener.open(req)
        data = f.read()
        br = 0
        match = re.compile('<div class="movie-item"><a href="(.+?)"><div class="thumb-holder"><img draggable="false" alt="(.+?)" src="(.+?)"').findall(data)
        for link,img,title in match:
         url = baseurl + link
         thumbnail = baseurl + img
         addDir(title,url,3,thumbnail)
        br = br + 1
        if br == 24:  # тогава имаме следваща страница и конструираме нейния адрес
         getpage = re.compile('<li class="current"><a href="">(.+?)</a></li> <li><a rel="next" href="(.+?)page=').findall(data)
         for page,pageurl in getpage:
          newpage = int(page) + 1
          url = baseurl + pageurl + 'page=' + str(newpage)
          addDir('следваща страница>>' + str(newpage), url, 2, 'DefaultFolder.png')


def SHOW(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', UA)
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        f = opener.open(req)
        data = f.read()
        match = re.compile('<source label="(\d+\w)" src="(.+?)"').findall(data)
        matchi = re.compile('og:image" content="(.+?)"').findall(data)
        matchd = re.compile('og:description" content="(.*) ').findall(data)
        for kachestvo,url in match:
         for thumbnail in matchi:
          for descr in matchd:
           title = name + '  Качество:' + kachestvo
           addLink(title,url,4,descr,thumbnail)


#Зареждане на видео
def PLAY(url):
         li = xbmcgui.ListItem(iconImage=iconimage, thumbnailImage=iconimage, path=url)
         li.setArt({ 'thumb': iconimage,'poster': iconimage, 'banner' : iconimage, 'fanart': iconimage })
         li.setInfo('video', { 'title': name })
         try:
            xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, li)
         except:
            xbmc.executebuiltin("Notification('Грешка','Видеото липсва на сървъра!')")






#Модул за добавяне на отделно заглавие и неговите атрибути към съдържанието на показваната в Kodi директория - НЯМА НУЖДА ДА ПРОМЕНЯТЕ НИЩО ТУК
def addLink(name,url,mode,plot,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
        liz.setArt({ 'thumb': iconimage,'poster': iconimage, 'banner' : iconimage, 'fanart': iconimage })
        liz.setInfo( type="Video", infoLabels={ "Title": name, "plot": plot } )
        liz.setProperty("IsPlayable" , "true")
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        return ok



#Модул за добавяне на отделна директория и нейните атрибути към съдържанието на показваната в Kodi директория - НЯМА НУЖДА ДА ПРОМЕНЯТЕ НИЩО ТУК
def addDir(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
        liz.setArt({ 'thumb': iconimage,'poster': iconimage, 'banner' : iconimage, 'fanart': iconimage })
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok


#НЯМА НУЖДА ДА ПРОМЕНЯТЕ НИЩО ТУК
def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param







params=get_params()
url=None
name=None
iconimage=None
mode=None

try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        name=urllib.unquote_plus(params["iconimage"])
except:
        pass
try:
        mode=int(params["mode"])
except:
        pass


#Списък на отделните подпрограми/модули в тази приставка - трябва напълно да отговаря на кода отгоре
if mode==None or url==None or len(url)<1:
        print ""
        CATEGORIES()
    
elif mode==1:
        print ""+url
        INDEXPAGES(url)

elif mode==2:
        print ""+url
        INDEXOBLAK(url)
        
elif mode==3:
        print ""+url
        SHOW(url)

elif mode==4:
        print ""+url
        PLAY(url)
xbmcplugin.endOfDirectory(int(sys.argv[1]))
