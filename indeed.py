from urllib.parse import parse_qs
import requests
from bs4 import BeautifulSoup

INDEED_LIMIT = 50
INDEED_URL = f"https://www.indeed.com/jobs?as_and=python&radius=25&fromage=3&limit={INDEED_LIMIT}&sort=date&psf=advsrch"

jobs = []


def get_indeed_pages():
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


def extract_indeed_job(job_html):
    title = job_html.find("a", {"class": "jobtitle"})["title"]
    company = job_html.find("span", {"class": "company"})
    if company:
        company = company.get_text(strip=True)
    location = job_html.find("span", {"class": "location"})
    if location:
        location = location.get_text(strip=True)
    job_id = job_html["data-jk"]
    apply_link = f"https://www.indeed.com/viewjob?jk={job_id}"
    job = {
        "title": title,
        "company": company,
        "location": location,
        "apply_link": apply_link,
    }
    return job


def scrappe_jobs(page, max_pages):
    url = f"{INDEED_URL}&start={page}"
    response = requests.get(url)
    print(f"Scrapping Indeed Page: {page}")
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        results = soup.findAll("div", {"class": "jobsearch-SerpJobCard"})
        for result in results:
            job = extract_indeed_job(result)
            jobs.append(job)
        next_page = page + INDEED_LIMIT
        if next_page <= max_pages:
            scrappe_jobs(page + INDEED_LIMIT, max_pages)
    else:
        print("Error!")


def get_indeed_jobs():
    max_pages = get_indeed_pages()
    scrappe_jobs(0, max_pages)
    return jobs
