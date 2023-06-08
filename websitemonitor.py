#Matt Bennett
#CNE350 6/7/2023
#Create a website monitoring script
#Full credit to https://pimylifeup.com/raspberry-pi-monitor-website/

import os
import sys
import requests

def has_website_changed(website_url, website_name):
    headers = {
        'User-Agent': 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; PIWEBMON)',
        'Cache-Control': 'no-cache'
    }

    response = requests.get(website_url, headers=headers)

    if (response.status_code < 200 or response.status_code > 299):
        return -1

    response_text = response.text

    cache_filename = website_name + "_cache.txt"

    if not os.path.exists(cache_filename):
        file_handle = open(cache_filename, "w")
        file_handle.write(response_text)
        file_handle.close()
        return 0

    file_handle = open(cache_filename, "r+")
    previous_response_text = file_handle.read()
    file_handle.seek(0)

    if response_text == previous_response_text:
        file_handle.close()

        return 0
    else:
        file_handle.truncate()
        file_handle.write(response_text)
        file_handle.close()

        return 1

def main():
    website_status = has_website_changed(sys.argv[1], sys.argv[2])

    if website_status == -1:
        print("Non 2XX response while fetching")
    elif website_status == 0:
        print("Website is the same")
    elif website_status == 1:
        print("Website has changed")

if __name__ == "__main__":
    main()
