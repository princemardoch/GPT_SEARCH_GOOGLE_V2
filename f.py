import requests
import json
from bs4 import BeautifulSoup
from openai import OpenAI
import time

# GPT CLEAN SEARCH INPUT OF USER
def clean_input_gpt(termes_brute):
    client = OpenAI(
        api_key="",
        )
    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "Exmple : User : 'Qui est alpha Wann et quel sont ses albums', Toi : Biographie Alpha Wann et Album - User : 'Qui est Damso' "},
        {"role": "user", "content": termes_brute}
    ]
    )

    clean_terms = completion.choices[0].message.content

    return clean_terms


# GPT RESUME ARTCILE INFORMATION
def resumegpt(article):
    client = OpenAI(
        api_key="",
        )
    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "Tu sert a resumé tout ce qu'ont te donne en moins de 100mots. Ce qui te serra donné c'est des donnée extrait d'un site web, donc ne prend pas en compte les contenus et balise HTML, Traduit et Parle uniquement en français, Ecris 2 phrase qui resume l'article et par la suite met en liste toute les information importante des articles que tu lit. Si la page web que tu reçois n'a pas de texte exploitable"},
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
        'num':1
    }
    params.update(kwargs)
    response = requests.get(service_url, params=params)
    return json.loads(response.text) 


def search(search_clean_terms):
    results = google_search(search_clean_terms,'','')


    for result in results['items']:
        lien = result['link']
    return lien


# BS4 VIEWS IN LINK GENERATE WITH GOOGLE SEARCH API
def views_page_with_bs4(link_search_g):
    try :
        url = link_search_g

        r = requests.get(url)
        if r.status_code == 200:
            html = r.content
            soup = BeautifulSoup(html, 'html5lib')
            try :
                body = soup.find('body')
                article_brute = [tag.get_text() for tag in body.find_all(['h1', 'h2', 'h3', 'p', 'span'])]
                article = str(article_brute)
            except:
                print('Error view article')
        else:
            print('Error link')
            print(r.status_code)

        return article

    except:
        print('ERROR View page')



# START SCRIPT
while True:
    t = time.time()
    while True:
        search_input_brute = input('Search : ')
        if search_input_brute:
            clean_term = clean_input_gpt(search_input_brute)
            print(clean_term)
            break
        else:
            continue
            
    link_search  = search(clean_term)

    article = views_page_with_bs4(link_search)
    print('\n -------------------- \n')
    resumegpt(article)
    print('\n -------------------- \n')
    t2 = time.time()
    s = f'{int(t - t2)} secondes'
    print('\n')
    print(s)



