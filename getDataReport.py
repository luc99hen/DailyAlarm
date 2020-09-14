from getWeatherStats import WeatherDataSource
import datetime

dataSource = WeatherDataSource()

# report generated by hour (try to inform you of the weather in next 12 hours)
def hourly_report(predictLength=12):
    warningLevel = 0

    # analyse stats from meizu weather
    mzstartTime = None
    mzWarningLevel = 0
    mz = dataSource.get_meizu()
    forecastList = mz["weather3HoursDetailsInfos"]
    for i in range(min(len(forecastList),int(predictLength/3))):
        # utmost as long as 12 hours
        weather = forecastList[i]['weather']
        mzstartTime = forecastList[i]['startTime']
        if '雨' in weather:
            mzWarningLevel += 1
            if i == 0:
                mzWarningLevel += 1
            break
    if mzWarningLevel == 0:
        mzstartTime = None

    #analyse stats from xiaomi weather
    xm = dataSource.get_xiaomi()["weather"]
    forecastList = xm["value"]
    xmstartTime = None
    xmWarningLevel = 0
    startTime = datetime.datetime.strptime(xm["pubTime"], "%Y-%m-%dT%H:%M:%S+08:00")
    for i in range(min(len(forecastList),predictLength)):
        weather = forecastList[i]
        startTime += datetime.timedelta(hours=1)
        # weather code > 2 means it's not 晴,多云 or 阴
        if weather > 2:
            xmWarningLevel += 1
            if i < 3:
                xmWarningLevel += 1
            break
    xmstartTime = startTime.strftime("%Y-%m-%d %H:%M:%S+08:00")
    if xmWarningLevel == 0:
        xmstartTime = None    
    
    warningLevel += mzWarningLevel
    warningLevel += xmWarningLevel
    
    return warningLevel,mzstartTime,xmstartTime


if __name__=="__main__":
    warningLevel,mzstartTime,xmstartTime = hourly_report()
