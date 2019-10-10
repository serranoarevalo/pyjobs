import requests
from bs4 import BeautifulSoup

SO_URL = "https://stackoverflow.com/jobs?q=python&sort=i"


def get_so_pages():
    response = requests.get(SO_URL)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        job_links = soup.find("div", attrs={"class": "pagination"}).findAll(
            "a", {"class": "job-link"}
        )
        job_links = job_links[:-1]
        higher_page = 0
        for link in job_links:
            link_number = int(link.get_text(strip=True))
            if higher_page < link_number:
                higher_page = link_number
        return higher_page
    return


def scrape_jobs():
    return


def get_so_jobs():
    pages = get_so_pages()
    print(pages)
