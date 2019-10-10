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


def scrape_jobs(max_pages, page=0):
    url = f"{SO_URL}&pg={page}"
    response = requests.get(url)
    print(f"Scrapping SO Page: {page}")
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        results = soup.findAll("div", {"class": "-job"})
        for result in results:
            print(result)
    return


def get_so_jobs():
    pages = get_so_pages()
    scrape_jobs(max_pages=pages)
    print(pages)
