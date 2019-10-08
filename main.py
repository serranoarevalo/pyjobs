from urllib.parse import parse_qs
import requests
from bs4 import BeautifulSoup

INDEED_LIMIT = 50
INDEED_URL = f"https://www.indeed.com/jobs?as_and=python&radius=25&fromage=3&limit={INDEED_LIMIT}&sort=date&psf=advsrch"


indeed_jobs = []


def get_pages():
    response = requests.get(INDEED_URL)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        pages = soup.find("div", attrs={"class": "pagination"})
        all_pages = pages.findAll("a")
        higher_page = 0
        for page in all_pages:
            query = parse_qs(page["href"])
            start, = query.get("start")
            if higher_page < int(start):
                higher_page = int(start)
        return higher_page
    else:
        print("Can't get pages")


def get_jobs(page, max_pages):
    url = f"{INDEED_URL}&start={page}"
    response = requests.get(url)
    print(f"Scrapping page: {page}")
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        results = soup.findAll("div", {"class": "jobsearch-SerpJobCard"})
        for result in results:
            job = {}
            job["title"] = result.find("a", {"class": "jobtitle"})["title"]
            job["company"] = result.find("span", {"class": "company"}).get_text(
                strip=True
            )
            job["location"] = result.find("span", {"class": "location"}).get_text(
                strip=True
            )
            job["apply_link"] = f"https://www.indeed.com/viewjob?jk={result['data-jk']}"
            indeed_jobs.append(job)
        next_page = page + INDEED_LIMIT
        if next_page <= max_pages:
            # get_jobs(page + INDEED_LIMIT, max_pages)
            pass
    else:
        print("Error!")


max_pages = get_pages()
get_jobs(0, max_pages)
print(indeed_jobs)
