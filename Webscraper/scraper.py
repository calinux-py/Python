# webscraper
# made by calinux

import requests
from bs4 import BeautifulSoup
import re

unique_emails = set()
unique_phone_numbers = set()

def extract_emails(html_content):
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return re.findall(email_pattern, html_content, re.IGNORECASE)

def extract_phone_numbers(html_content):
    phone_pattern = r'\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b'
    return re.findall(phone_pattern, html_content)

def scrape_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        html_content = response.text

        emails = extract_emails(html_content)
        for email in emails:
            if email not in unique_emails:
                store_email(email)
                unique_emails.add(email)

        phone_numbers = extract_phone_numbers(html_content)
        for phone_number in phone_numbers:
            if phone_number not in unique_phone_numbers:
                store_phone_number(phone_number)
                unique_phone_numbers.add(phone_number)

        soup = BeautifulSoup(html_content, 'html.parser')
        for link in soup.find_all('a'):
            href = link.get('href')
            if href is not None and href.startswith('http'):
                scrape_url(href)

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

def store_email(email):
    print(f"Found email: {email}")

def store_phone_number(phone_number):
    print(f"Found phone number: {phone_number}")

if __name__ == '__main__':
    starting_url = 'https://iamjakoby.com/'     # Enter target website here
                                                # shoutout to I_am_Jakoby - check his stuff out
    scrape_url(starting_url)
