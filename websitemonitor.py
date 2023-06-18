#Matt Bennett
#CNE350 6/7/2023
#Create a website monitoring script
#Full credit to https://pimylifeup.com/raspberry-pi-monitor-website/
#The crontab edit should read "0 * * * * python3 /home/pi/350final/websitemonitor.py" to check hourly

import os
import requests
from bs4 import BeautifulSoup
import smtplib

#Establishing variables for email. Config.py used for privacy purposes.
from config import SMTP_USER, SMTP_PASSWORD, SMTP_FROM_EMAIL
SMTP_HOST='smtp.gmail.com'
SMTP_PORT='465'
SMTP_SSL=True

SMTP_TO_EMAIL='cne350throwaway@hotmail.com'

#Sends email if change has occurred (result 1)
def email_notification(subject, message):
    if (SMTP_SSL):
        smtp_server = smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT)
    else:
        smtp_server = smtplib.SMTP(SMTP_HOST, SMTP_PORT)

    smtp_server.ehlo()
    smtp_server.login(SMTP_USER, SMTP_PASSWORD)

    email_text = \
"""From: %s
To: %s
Subject: %s

%s
""" % (SMTP_FROM_EMAIL, SMTP_TO_EMAIL, subject, message)

    smtp_server.sendmail(SMTP_FROM_EMAIL, SMTP_TO_EMAIL, email_text)

    smtp_server.close()

#Cleans up html fetch. Reduces instances of false flag for change
def cleanup_html(html):
    soup = BeautifulSoup(html, features="lxml")

    for s in soup.select('script'):
        s.extract()

    for s in soup.select('style'):
        s.extract()

    for s in soup.select('meta'):
        s.extract()

    return str(soup)

#Pulls html from site and checks for change in website against cache
def has_website_changed(website_url, website_name):
    headers = {
        'User-Agent': 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; PIWEBMON)',
        'Cache-Control': 'no-cache'
    }

    response = requests.get(website_url, headers=headers)

    if not response.ok:
        return -1

    response_text = cleanup_html(response.text)

    cache_filename = website_name + "_cache.txt"

    if not os.path.exists(cache_filename):
        with open(cache_filename, "w", encoding="utf-8") as file_handle:
            file_handle.write(response_text)
        return 0

    with open(cache_filename, "r+", encoding="utf-8") as file_handle:
        previous_response_text = file_handle.read()
        file_handle.seek(0)

        if response_text == previous_response_text:
            return 0
        else:
            file_handle.truncate()
            file_handle.write(response_text)
            return 1

def main():
    website_status = has_website_changed("https://rtc.edu/computer-network-engineering", "CNEProgram")

    if website_status == -1:
        print("Non 2XX response while fetching")
    elif website_status == 0:
        print("Website is the same")
    elif website_status == 1:
        email_notification("A Change has Occurred",  "CNE Program has changed.")
        print("Website has changed")

if __name__ == "__main__":
    main()
