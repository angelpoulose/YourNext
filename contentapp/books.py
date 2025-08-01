import requests

def get_books_by_genres(genres, limit_per_genre=5, exclude_titles=None):
    exclude_titles = set(exclude_titles or [])
    seen_titles = set()
    results = []

    for genre in genres:
        url = f'https://openlibrary.org/subjects/{genre.lower().strip()}.json?limit={limit_per_genre * 5}'
        response = requests.get(url)

        if response.status_code != 200:
            continue

        data = response.json()
        for book in data.get('works', []):
            title = book.get('title')
            if not title or title in seen_titles or title in exclude_titles:
                continue

            seen_titles.add(title)

            cover_id = book.get('cover_id')
            authors = [a.get('name') for a in book.get('authors', [])]
            plot = book.get('description') or book.get('first_sentence') or "No description available"
            if isinstance(plot, dict):
                plot = plot.get('value', "No description available")

            results.append({
                'title': title,
                'cover': f"https://covers.openlibrary.org/b/id/{cover_id}-L.jpg" if cover_id else None,
                'authors': authors,
                'plot': plot
            })

            if sum(b['title'] in seen_titles for b in results) >= limit_per_genre * len(genres):
                break

    return results
