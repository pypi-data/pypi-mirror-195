import random, requests, time

def get_proxy():
    proxyscrape_url = "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all"
    global proxy_list, last_update_time
    
    # Check if the proxy list needs to be updated
    current_time = time.time()
    if current_time - last_update_time > 1800: # update every 30 minutes
        response = requests.get(proxyscrape_url)
        if response.status_code == 200:
            # Split the response by line and update the proxy list
            proxy_list = response.text.strip().split('\n')
            last_update_time = current_time
            print("Updated proxy list from Proxyscrape")

    # Return a random proxy server from the list
    if len(proxy_list) > 0:
        return {"http": "http://" + random.choice(proxy_list)}
    else:
        return None