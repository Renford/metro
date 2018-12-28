from urllib import parse, request
import json

import requests

import urllib3

# ids = [1,2,3,4,5,6,7,8,9,10,11,12,13,16,17,41]
# http://m.shmetro.com/interface/metromap/metromap.aspx?func=lineStations&line=41
# http://m.shmetro.com/interface/metromap/metromap.aspx?func=stationInfo&stat_id=0241
# http://service.shmetro.com/skin/zct/0241.jpg


def wirteJson(datas, filePath):
    fileData = json.dumps(datas, ensure_ascii=False)
    fp = open(filePath, "w")
    fp.write(fileData)
    fp.close()


def getStationInfo(id):
    url = "http://m.shmetro.com/interface/metromap/metromap.aspx?func=stationInfo&stat_id=" + id

    http = urllib3.PoolManager()
    response = http.request('GET', url)
    jsonData = json.loads(response.data)
    station = jsonData[0]

    item = {
        "id": id,
        "zhName": station["name_cn"],
        "enName": station["name_en"],
        "pinyin": station["pinyin"],
        "lines": station["lines"],
        "toilet": station["toilet_position"],
        "entrance": station["entrance_info"]
    }

    filePath = "./stations/" + id + ".json"
    wirteJson(item, filePath)

    return item


def mapStation(station):
    id = station["id"].replace("station", "")
    return {"id": id, "name": station["title"]}


def getStations(line):
    url = "http://m.shmetro.com/interface/metromap/metromap.aspx?func=lineStations&line=" + line
    http = urllib3.PoolManager()
    response = http.request('GET', url)
    jsonData = json.loads(response.data)
    stations = jsonData["levels"][0]["locations"]
    stats = list(map(mapStation, stations))

    filePath = "./lines/" + line + ".json"
    wirteJson(stats, filePath)

    lines = []
    for station in stats:
        item = getStationInfo(station["id"])
        lines.append(item)

    print('==========line', line, lines)

    filePath = "./lines2/" + line + ".json"
    wirteJson(lines, filePath)


lines = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 16, 17, 41]
for line in lines:
    getStations(str(line))
