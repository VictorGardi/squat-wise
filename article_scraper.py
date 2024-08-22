from uuid import uuid4

import requests
from bs4 import BeautifulSoup


def scrape(limit: int = 100000) -> list[str]:
    # URL of the page containing the list of articles
    base_url = "https://squatuniversity.com/featured-links/blog/"  # Adjust this URL as needed
    
    article_links = get_article_links(base_url)[:limit]
    
    data = []
    for i, link in enumerate(article_links):
        print(f"Article {i + 1} of {len(article_links)}...")
        print(link)
        title, date, content = scrape_article(link)
        if not content:
            continue

        article_data = {
            "id": str(uuid4()),
            "title": title,
            "content": " ".join(content),
            "url": link,
            "date": date,
            "source": "article"
        }
        data.append(article_data)
    return data 


def get_article_links(url):
    article_links = []
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find the <ol> element within the entry-content div

    article_list = soup.find(id="post-2842")
    for ol in article_list.find_all("ol"):
        # Find all <li> elements within the <ol>
        for link in ol.find_all("li"):
            # Find the <a> tag within each <li>
            link = link.find("a")
            if link and "href" in link.attrs:
                article_links.append(link["href"])
    
    return article_links

def scrape_article(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    def find_article_title(soup: BeautifulSoup) -> str:
        title = soup.find(class_="entry-title")
        if title:
            return title.get_text()
        else:
            return ""

    def find_publishing_date(soup: BeautifulSoup) -> str:
        time = soup.time
        if time:
            return time.attrs["datetime"]
        else:
            return ""


    article_sections = soup.find('div', class_='entry-content')
    article_text = []
    for section in article_sections.find_all("p"):
        if section:
            article_text.append(section.get_text(separator=' ', strip=True))
    return find_article_title(soup), find_publishing_date(soup), article_text


if __name__ == "__main__":
    main()


