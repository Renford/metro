from urllib import parse, request
import json

import requests

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
  res = requests.get(url)
  station = res.json()[0]
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

def mapStation(station):
  id = station["id"].replace("station", "")
  return {
    "id": id,
    "name": station["title"]
  }

def getStations(line): 
  url = "http://m.shmetro.com/interface/metromap/metromap.aspx?func=lineStations&line=" + line
  res = requests.get(url)
  stations = res.json()["levels"][0]["locations"]
  stats = list(map(mapStation, stations))

  filePath = "./lines/" + line + ".json"
  wirteJson(stats, filePath)

  for station in stats:
    getStationInfo(station["id"])

lines = [1,2,3,4,5,6,7,8,9,10,11,12,13,16,17,41]
for line in lines:
  getStations(str(line))
