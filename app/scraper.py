import datetime

import celery
from celery.schedules import crontab
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import requests
from bs4 import BeautifulSoup

from models.student_group import GroupStatus
from settings import IMG_FORMAT
from servise import static_servises, group_servises

app = celery.Celery("scraper", broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')
app.conf.timezone = "UTC"


def get_comic_img():
    current_date = datetime.date.today()
    url = "https://dilbert.com"
    page = requests.get(url).text
    soup = BeautifulSoup(page, "html.parser")
    current_post = soup.find('div', class_="js-comic-container-" + str(current_date))
    if current_post:
        img = current_post.find("img", class_="img-responsive img-comic")
        src = img.get("src")
        photo = requests.get(src).content
        with open(f'comics.{IMG_FORMAT}', 'wb') as f:
            f.write(photo)
        static_servises.put_date(comics_date=current_date)
        return True
    return False


@app.task
def get_schedule_img():
    groups = group_servises.get_groups(status_code=GroupStatus.completed.value)
    options = webdriver.ChromeOptions()
    result_dict = {}
    options.add_argument("headless")
    options.add_argument('window-size=1920,1080')
    driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
    driver.get("https://raspisanie.grsu.by/TimeTable/UMU.aspx")
    for group in groups:
        driver.find_element_by_xpath("//div[@id='ddlFaculty_chosen']/a[@class='chosen-single']").click()
        driver.find_element_by_xpath(
            f"//div[@id='ddlFaculty_chosen']/div[@class='chosen-drop']/ul/li[text()='{group.faculty.name}']").click()

        driver.find_element_by_xpath("//div[@id='ddlDepartment_chosen']/a[@class='chosen-single']").click()
        driver.find_element_by_xpath(
            f"//div[@id='ddlDepartment_chosen']/div[@class='chosen-drop']/ul/li[text()='{group.form.type} форма']").click()

        driver.find_element_by_xpath("//div[@id='ddlCourses_chosen']/a[@class='chosen-single']").click()
        driver.find_element_by_xpath(
            f"//div[@id='ddlCourses_chosen']/div[@class='chosen-drop']/ul/li[text()='{group.course.num} курс']").click()

        driver.find_element_by_xpath("//div[@id='ddlGroups_chosen']/a[@class='chosen-single']").click()
        driver.find_element_by_xpath(
            f"//div[@id='ddlGroups_chosen']/div[@class='chosen-drop']/ul/li[text()='{group.name}']").click()
        driver.find_element_by_id("btnShowTT").click()
        tbody = driver.find_element_by_xpath("//table[@id='TT']/tbody")
        if tbody.text == group.last_schedule:
            result_dict[group.name] = "no changes"
        else:
            tbody.screenshot(f"schedule_imgs/{group.name}.{IMG_FORMAT}")
            group_servises.put_group(group.id, current_schedule=tbody.text, status_code=GroupStatus.updated.value)
            result_dict[group.name] = "updated"
    driver.close()



