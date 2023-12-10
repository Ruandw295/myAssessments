from flask import Flask
import requests, json, queue
from threading import Thread

app = Flask(__name__)

@app.route("/")
def social_network_activity():
    # TODO: your code here
    social_networks = [
                {
                    'Name': "Twitter",
                    'URL': "https://takehome.io/twitter"
                },
                {
                    'Name': "Facebook",
                    'URL': "https://takehome.io/facebook"
                },
                {
                    'Name': "Instagram",
                    'URL': "https://takehome.io/instagram"
                }
            ]


  
    result_queue = queue.Queue()
    # Create a loop that kicks off a thread in each iteration
    threads = []
    for i in social_networks:
        social_network_name = i["Name"].lower()
        social_network_api_url = i["URL"]

        thread = Thread(target=get_records, args=(social_network_api_url,social_network_name, result_queue,))
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete   
    for thread in threads:
        thread.join()

    # Retrieve data from the queue    
    results = {}
    while not result_queue.empty():
        thread_num, data = result_queue.get()
        results[thread_num] = data

    json_response =json.dumps(results)
    return json_response


def get_records(api_url, thread_num, data_queue):
    
        response = requests.get(api_url)
        
        if response.status_code == 200:
            data = response.json()
            number_of_records = len(data)
            data_queue.put((thread_num, number_of_records))
        else:
            data_queue.put((thread_num, None))
            print("Thread "+ thread_num +" failed to fetch data from API")
        

