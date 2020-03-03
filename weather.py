import datetime
import SpiderLib
import re
import sendemail
import time
url = "http://www.nmc.cn/publish/forecast/AZJ/xiaoshan.html"

url_map = {
'http://image.nmc.cn/static2/site/nmc/themes/basic/weather/white/day/1.png':'cloudy' ,
'http://image.nmc.cn/static2/site/nmc/themes/basic/weather/white/day/2.png' : 'overcast' ,
'http://image.nmc.cn/static2/site/nmc/themes/basic/weather/white/day/3.png' :'cloudy_to_rain',
'http://image.nmc.cn/static2/site/nmc/themes/basic/weather/white/day/4.png' : 'thundershower' ,
'http://image.nmc.cn/static2/site/nmc/themes/basic/weather/white/day/5.png' : 'snow' ,
'http://image.nmc.cn/static2/site/nmc/themes/basic/weather/white/day/6.png' :'rain_and_snow' ,
'http://image.nmc.cn/static2/site/nmc/themes/basic/weather/white/day/7.png' :'little_rain',
'http://image.nmc.cn/static2/site/nmc/themes/basic/weather/white/day/8.png' : 'mid_rain' ,
'http://image.nmc.cn/static2/site/nmc/themes/basic/weather/white/day/9.png' :'heavy_rain' ,
'http://image.nmc.cn/static2/site/nmc/themes/basic/weather/white/day/10.png' :'cat_dog_rain',
'http://image.nmc.cn/static2/site/nmc/themes/basic/weather/white/day/11.png' : 'unstopable_rain',
'http://image.nmc.cn/static2/site/nmc/themes/basic/weather/white/day/12.png' : 'wtf_rain',
'http://image.nmc.cn/static2/site/nmc/themes/basic/weather/white/day/13.png' : 'sunny_to_snow',
'http://image.nmc.cn/static2/site/nmc/themes/basic/weather/white/day/0.png' : 'sunny'
}

alarmer_list = ['cloudy_to_rain','thundershower','rain_and_snow','little_rain','mid_rain',
                'heavy_rain','cat_dog_rain','unstopable_rain','wtf_rain']

weather_map = {
    'cloudy' : "多云",
    'overcast' : "阴天",
    'cloudy_to_rain' : '多云转雨',
    'thundershower' : '雷阵雨',
    'snow' : '雪',
    'rain_and_snow' : '雨夹雪' ,
    'little_rain' : '小雨',
    'mid_rain' : '中雨',
    'heavy_rain' : '大雨',
    'cat_dog_rain' : "暴雨",
    'unstopable_rain' : "大暴雨",
    'wtf_rain' : "特大暴雨",
    'sunny_to_snow' : '晴转雪',
    'sunny' : "晴天"
}



def getTime():
    ISOTIMEFORMAT = '%H:%M'
    time = datetime.datetime.now().strftime(ISOTIMEFORMAT)
    return time

def getWeather(url):
    flag_rain = 0
    title = "天气预报"
    main_aprt = ""
    web = SpiderLib.visitByLocalNet(url)
    conclusion_re = r'<div id="forecast" class="forecast">(.+)<div class="clear"></div> \n    </div> \n'
    title_list = re.findall(conclusion_re,web.data.decode('UTF-8'),re.S)
    tomorrow_re = r'<div class="detail"> (.+?)</div> \n      </div> \n     </div> \n'
    part_list = re.findall(tomorrow_re,title_list[0],re.S)
    print(part_list[1])
    weather_re = r'<td class="wdesc">(.+?)</td> '
    temp_re = r'<td class="temp">(.+?)</td>'
    weather = re.findall(weather_re,part_list[1],re.S)#0 today 1 tomorrow 2 the day after tomorrow
    temp = re.findall(temp_re,part_list[1],re.S)
    print(weather)
    print(temp)
    weather_list = []
    temp_list = []
    for i in weather :
        weather_list.append(i)
    for i in temp:
        temp_list.append(i)
    main_aprt += "明天天气" + weather_list[0] + "到" + weather_list[1] + "<br>"
    main_aprt += "温度" + temp[1] + "到" + temp[0] + ' <br>'

    full_re = r'<div id="day1" class="hour3" style="display(.+?)<!--'
    full_list = re.findall(full_re,web.data.decode("UTF-8"),re.S)
    print(full_list[0])
    time_re = r'<div class="row second tqxx">(.+?)<div class="row wd">'
    time_list = re.findall(time_re,full_list[0],re.S)
    url_re = r'src="(.+?)">'
    url_list = re.findall(url_re,time_list[0],re.S)
    start_time = 8
    for i in url_list:
        if start_time>24:
            break
        main_aprt += str(start_time) + ":00  天气为:"
        if i in url_map:
            key = url_map[i]
            if key in alarmer_list:
                flag = 1
            weather_data = weather_map[key]
            main_aprt += weather_data + ' <br>'
        start_time +=3
    print(main_aprt)
    if flag == 1:
        title += "——明天有降雨概率"
    sendemail.SendToMe(title,main_aprt)
def start():
    while 1==1:
        times = getTime()
        if times == "22:30":
            print(times)
            getWeather(url)
        time.sleep(59)

start()