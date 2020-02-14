from pymongo import MongoClient
from pprint import pprint

client = MongoClient("mongodb+srv://crawler:i3im5THC2HG7h62X@theglobecrawler-73kqg.gcp.mongodb.net/test?retryWrites=true&w=majority")
db = client.admin

serverStatusResult=db.command("serverStatus")
pprint(serverStatusResult)
