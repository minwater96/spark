import requests
import time
from confluent_kafka import Producer

server_url = "https://api.upbit.com"
params = {
    "markets": "KRW-BTC"
}

producer = Producer({'bootstrap.servers': 'localhost:9092'}) 

while True:
    res = requests.get(server_url + "/v1/ticker", params=params)
    data = res.json()[0]

    csv_data = f"{data['market'], data['trade_date'], {data['trade_time']}, {data['trade_price']}}"

    print(csv_data)
    
    producer.poll(0)
    producer.produce('upbit-api', csv_data)
    producer.flush()


    time.sleep(2)