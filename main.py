import requests
import json
from bs4 import BeautifulSoup
from openai import OpenAI
import time

# GPT CLEAN SEARCH INPUT OF USER
def clean_user_input(raw_terms):
    client = OpenAI(
        api_key="",
    )
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": ""},
            {"role": "user", "content": raw_terms}
        ]
    )

    clean_terms = completion.choices[0].message.content

    return clean_terms


# GPT RESUME ARTICLE INFORMATION
def resume_article(article):
    client = OpenAI(
        api_key="",
    )
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": ""},
            {"role": "user", "content": article}
        ]
    )

    message_content = completion.choices[0].message.content
    print(message_content)
    return message_content


# GOOGLE SEARCH API
def google_search(search_term, api_key, cse_id, **kwargs):
    service_url = 'https://www.googleapis.com/customsearch/v1'
    params = {
        'q': search_term,
        'key': api_key,
        'cx': cse_id,
        'num': 1
    }
    params.update(kwargs)
    response = requests.get(service_url, params=params)
    return json.loads(response.text)


def perform_search(clean_terms):
    results = google_search(clean_terms, '', '')

    for result in results['items']:
        link = result['link']
    return link


# BS4 VIEWS IN LINK GENERATED WITH GOOGLE SEARCH API
def view_page_with_bs4(search_link):
    try:
        url = search_link

        r = requests.get(url)
        if r.status_code == 200:
            html = r.content
            soup = BeautifulSoup(html, 'html5lib')
            try:
                body = soup.find('body')
                article_raw = [tag.get_text() for tag in body.find_all(['h1', 'h2', 'h3', 'p', 'span'])]
                article = str(article_raw)
            except:
                print('Error viewing article')
        else:
            print('Error in link')
            print(r.status_code)

        return article

    except:
        print('ERROR viewing page')


# START SCRIPT
while True:
    t = time.time()
    while True:
        raw_search_input = input('Search: ')
        if raw_search_input:
            clean_terms = clean_user_input(raw_search_input)
            print(clean_terms)
            break
        else:
            continue

    search_link = perform_search(clean_terms)

    article = view_page_with_bs4(search_link)
    print('\n -------------------- \n')
    resume_article(article)
    print('\n -------------------- \n')
    t2 = time.time()
    s = f'{int(t2 - t)} seconds'
    print('\n')
    print(s)
