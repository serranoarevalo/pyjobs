import requests
from bs4 import BeautifulSoup

SO_URL = "https://stackoverflow.com/jobs?q=python&sort=i"


so_jobs = []


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


def extract_job(job_html):
    title = (
        job_html.find("div", {"class": "-title"})
        .find("h2", {"class": "job-details__spaced"})
        .find("a")["title"]
    )
    subtitle = list(
        job_html.find("div", {"class": "-company"}).findAll("span", recursive=False)
    )
    company = subtitle[0].get_text(strip=True)
    location = subtitle[1].get_text(strip=True)
    location = location.strip("-").strip(" \r").strip("\n")
    link = job_html.find("h2", {"class": "job-details__spaced"}).find("a")["href"]
    job = {
        "title": title,
        "company": company,
        "location": location,
        "apply_link": f"https://stackoverflow.com{link}",
    }
    return job


def scrape_jobs(max_pages, page=0):
    url = f"{SO_URL}&pg={page}"
    response = requests.get(url)
    print(f"Scrapping SO Page: {page}")
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        results = soup.findAll("div", {"class": "-job"})
        for result in results:
            job = extract_job(result)
            so_jobs.append(job)
        next_page = page + 1
        if next_page <= max_pages:
            scrape_jobs(max_pages, page + 1)
    return


def get_so_jobs():
    pages = get_so_pages()
    scrape_jobs(max_pages=pages)
    return so_jobs
