import os
import random
import sys
import time
from datetime import datetime
from email import message_from_bytes

import requests
from bs4 import BeautifulSoup
from craigslist import Craigslist
from craigslist_email import CraigslistEmail
from selenium.webdriver.common.by import By

# SET UP ENVIRONMENT VARIABLES
CL_USERNAME = os.environ.get('CL_USER')
CL_PASSWORD = os.environ.get('CL_PASS')
EMAIL_ADDRESS = CL_USERNAME
EMAIL_PASSWORD = os.environ.get('CL_EMAIL_PASS')
# WEBHOOK (optional) configures the discord webhook url to send summary to
WEBHOOK = os.environ.get('DISCORD_WEBHOOK')

# MAX_POST_DAYS configures the maximum number of days after posting before reposting 
MAX_POST_DAYS = random.randint(8,14)
# MAX_REPOSTS configures the maximum number of posts to repost per run
MAX_REPOSTS = int(sys.argv[1])
# MAX_RENEWALS configures the manimum number of posts to renew per run
MAX_RENEWALS = int(sys.argv[2])

# IMAP_SERVER for email provider, default for gmail
IMAP_SERVER = 'imap.gmail.com'

repost_count = 0
renew_count = 0

current_time = datetime.now()

# Initialize connection to email inbox
inbox = CraigslistEmail(IMAP_SERVER, EMAIL_ADDRESS, EMAIL_PASSWORD)
# Delete unread emails from robot@craigslist.com prior to beginning craigslist portion of script
inbox.delete_craigslist_emails()

# Initialize Craigslist object and login to craigslist account
cl = Craigslist(CL_USERNAME)

# Check if logged in, if not, wait for email confirmation and verify login
if not cl.check_logged_in():
    cl.login(CL_USERNAME, CL_PASSWORD)
    time.sleep(1)
    if not cl.check_logged_in():
        print('Not logged in, verifying login')
        cl.driver.find_element(By.CLASS_NAME, 'submit-onetime-link-button').click()
        time.sleep(5)
        # Wait for emails from craigslist to be received
        for msgid, data in inbox.wait_unread_emails():
            print('Found email from craigslist')
            contents = message_from_bytes(data[b'RFC822'])
            content = contents.get_payload()[1].get_payload(decode=True)
            soup = BeautifulSoup(content, 'html.parser')
            links = soup.find_all('a', href=True)
            # When email is received, get the link to verify login
            cl.driver.get(links[0]['href'])
            inbox.email.delete_messages(msgid)
            time.sleep(1)
cl.filter_active_posts()
time.sleep(2)

cl.set_home_window()
active_posts = cl.get_posts()

# Loop through active posts and repost if older than MAX_POST_DAYS
for post in active_posts:
    if repost_count == MAX_REPOSTS:
        print(f"Maximum reposts of {MAX_REPOSTS} reached")
        break
    # parse_date converts string from dd MTH yyyy HH:MM format to datetime object
    def parse_date(string):    
        date = string.split(' ')
        time = date[3].split(':')
        return datetime(int(date[2]), datetime.strptime(date[1], "%b").month, int(date[0]), int(time[0]), int(time[1]))
    post_date = parse_date(cl.get_post_date(post))
    posted_days = (current_time - post_date).days
    if posted_days > MAX_POST_DAYS:
        repost_count += 1
        print(f'Reposting, post active for {posted_days} days: {cl.get_post_title(post)}')
        cl.repost(post)
        cl.driver.close()
        cl.driver.switch_to.window(cl.home_window)
        sleep_time = random.randint(10,230)
        print(f'Reposted, sleeping {sleep_time} seconds...')
        time.sleep(sleep_time)

# Delete unread emails which are verifying reposts
inbox.delete_craigslist_emails()
print('Unread emails from craigslist deleted')

# Loop through present renew buttons, clicking to renew post
cl.driver.refresh()
for button in cl.get_renewal_buttons():
    if renew_count == MAX_RENEWALS:
        print(f"Maximum renewals of {MAX_RENEWALS} reached")
        break
    renew_count += 1
    sleep_time = random.uniform(0.5,3.5)
    print(f'Renewing post and sleeping for {sleep_time} seconds...')
    cl.command_click(button)
    time.sleep(sleep_time)

cl.driver.quit()

# Print and send count of posts resposted and renewed to discord webhook
summary = f'{CL_USERNAME}\nCraigslist.com listings renewed: {renew_count}\nCraigslist.com listings reposted: {repost_count}'
print(summary)
if WEBHOOK:
    data = {'content':summary}
    result = requests.post(WEBHOOK, json = data)