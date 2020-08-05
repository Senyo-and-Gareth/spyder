import os
import wget
import json
import urllib
import requests
from bs4 import BeautifulSoup


BASEURL = 'https://www.tumblr.com/search'
VALID_EXTS = ['.png', '.jpg', '.gif', '.gifv']


def request(url, headers=None):
    if headers is None:
        headers = {
            'Content-Type': 'text/html',
            'Accept-Encoding': 'identity'
        }
    response = requests.get(url, headers=headers)
    return response


if __name__ == "__main__":
    search = 'cowboy bebop'
    url = urllib.parse.quote_plus(search)
    url = f'{BASEURL}/{url}'
    
    response = request(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    photos = []
    articles = soup.find_all('article')
    for i, article in enumerate(articles, start=1):
        print(f'Processing {i}/{len(articles)}')
        data = json.loads(article.get('data-json'))
        photoset = data.get('photoset_photos', None)
        if photoset is None:
            post_url = data['share_popover_data']['post_url']
            response = request(post_url)
            soup = BeautifulSoup(response.content, 'html.parser')
        
            subarticles = soup.find_all('article')
            for subarticle in subarticles:
                images = subarticle.find_all('img')
                for image in images:
                    image = image.get('src')
                    ext = os.path.basename(image)[-1]
                    if ext in VALID_EXTS:
                        photos.append(image)
        else:
            for photo in photoset:
                photos.append(photo['high_res'])
                
    base = 'images'
    os.makedirs(base, exist_ok=True)
    for photo in photos:
        wget.download(photo, out=base)
