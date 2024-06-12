from hdfs import InsecureClient
import os

# HDFS Namenode IP addr
client = InsecureClient("http://192.168.0.48:50070", user="hadoop")
with client.read("/user/hadoop/strawberry_avg.csv", encoding='utf-8') as f:
    print(f.read())