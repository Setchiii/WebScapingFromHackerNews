import requests
from bs4 import BeautifulSoup

# Fonction qui récupère les données de la page web entrée en paramètre et retourne un object BeautifulSoup contenant le code HTML de la page


def get_soup_from_url(url):
    response = requests.get(url)
    # On retourne un objet BeautifulSoup
    return BeautifulSoup(response.text, 'html.parser')


def extract_links(soup: BeautifulSoup, min_score=100):
    links_list = []

    # Find all rows with class 'subtext' (where the score is located)
    subtexts = soup.find_all('td', class_='subtext')

    for subtext in subtexts:
        link_info = []
        # Extract score
        score = subtext.find('span', class_='score')
        if score:
            # Get the number part of the score
            score = int(score.text.split()[0])

        # If score is not found, or if it is less than the minimum score, skip
        if score and score >= min_score:
            # Find the parent row. The title is in the second 'td' tag with class 'title'
            row = subtext.find_parent('tr').find_previous_sibling('tr')
            if row:
                title_data = row.find_all('td', class_='title')[1]
                if title_data:
                    link = title_data.find('a')
                    if link:
                        link_info.append(link.text)
                        link_info.append(link['href'])
                        link_info.append(score)
                        links_list.append(link_info)
# Trier la liste par ordre de score décroissant avant de retourner le résultat
    links_list.sort(key=lambda x: x[2], reverse=True)
    return links_list


if __name__ == '__main__':
    url = 'https://news.ycombinator.com/news'
    soup = get_soup_from_url(url)
    links = extract_links(soup, 0)
    for link in links:
        print(link)
