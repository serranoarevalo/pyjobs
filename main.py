import requests
from bs4 import BeautifulSoup

INDEED_URL = "https://www.indeed.com/jobs?as_and=python&radius=25&fromage=3&limit=10&sort=date&psf=advsrch"

indeed_jobs = []


def get_jobs(page):
    response = requests.get(f"{INDEED_URL}&start={page}")
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        results = soup.findAll("div", {"class": "jobsearch-SerpJobCard"})
        for result in results:
            job = {}
            job_title = result.find("a", {"class": "jobtitle"})
            job["title"] = job_title["title"]
            indeed_jobs.append(job)

    else:
        print("Error!")


get_jobs(0)

print(indeed_jobs)
