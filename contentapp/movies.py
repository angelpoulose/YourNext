import requests

API_KEY = '1n6M6drijMA2iXuHkH7rdabCqiF9IBUTu2Li0s8e'

def fetch_genre_map():
    url = f'https://api.watchmode.com/v1/genres/?apiKey={API_KEY}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return {item['name'].lower(): item['id'] for item in data}
    return {}

def get_movies(genre_ids, language='en', exclude_ids=None):
    genre_ids = [str(i) for i in genre_ids]
    exclude_ids = exclude_ids or []

    url = 'https://api.watchmode.com/v1/list-titles/'
    params = {
        'apiKey': API_KEY,
        'genres': ','.join(genre_ids),
        'language': language,
        'types': 'movie',
        'limit': 10 
    }

    response = requests.get(url, params=params)
    print("List Titles Status:", response.status_code)
    print("List Titles Response:", response.text)

    if response.status_code != 200:
        return []

    titles = response.json().get('titles', [])
    detailed_movies = []

    for title in titles:
        title_id = title.get('id')
        if title_id in exclude_ids:
            continue

        detail_url = f'https://api.watchmode.com/v1/title/{title_id}/details/'
        detail_response = requests.get(detail_url, params={'apiKey': API_KEY})

        if detail_response.status_code == 200:
            detail_data = detail_response.json()
            movie_info = {
                'id': title_id,
                'title': detail_data.get('title'),
                'plot': detail_data.get('plot_overview') or "No plot available",
                'image': detail_data.get('poster'),
                'year': detail_data.get('year')
            }
            detailed_movies.append(movie_info)

        if len(detailed_movies) >= 8:
            break
    return detailed_movies

def get_movies_by_ids(id_list):

    movies = []

    for movie_id in id_list:
        url = f'https://api.watchmode.com/v1/title/{movie_id}/details/'
        params = {'apiKey': API_KEY}
        response = requests.get(url, params=params)

        if response.status_code == 200:
            data = response.json()
            movies.append({
                'id': movie_id,
                'title': data.get('title'),
                'plot': data.get('plot_overview') or 'No plot available',
                'image': data.get('poster'),
                'year': data.get('year')
            })

    return movies