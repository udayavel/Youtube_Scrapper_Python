import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as bs
import yt_video_download as yt
import sql_db_operations as sq
import base64
import mongo_db_operations as md


# DRIVER_PATH = r'chromedriver.exe'
# yt_video_link = "https://www.youtube.com/@Srinivlog/videos"
# video_count=1

def scrape_data(DRIVER_PATH,yt_video_link,video_count):
    service = Service(executable_path=DRIVER_PATH)
    driver = webdriver.Chrome(service=service)

    links = []
    thumbnails = []
    driver.get(yt_video_link)
    driver.maximize_window()
    time.sleep(4)
    driver.execute_script("window.scrollTo(0, 200);")
    for i in range(0, 2):
        time.sleep(2)
        driver.execute_script("window.scrollTo(0, 10000);")

    thumbnail_link = driver.find_elements(By.XPATH, '//*[@id="thumbnail"]/yt-image/img')
    for t in thumbnail_link:
        thumbnails.append(t.get_attribute('src'))
        if len(thumbnails) == video_count:
            break

    video_thumb = driver.find_elements(By.TAG_NAME, 'ytd-rich-item-renderer')
    print(len(video_thumb))

    for i in range(len(video_thumb)):
        video_link = video_thumb[i].find_element(By.ID, 'video-title-link').get_attribute("href")
        links.append(video_link)
        if len(links) == video_count:
            break

    # looping each link
    for l in range(len(links)):
        yt.download_yt(links[l])
        driver.get(links[l])
        driver.maximize_window()
        time.sleep(4)
        driver.execute_script("window.scrollTo(0, 200);")
        for i in range(0, 2):
            time.sleep(2)
            driver.execute_script("window.scrollTo(0, 10000);")

        comments_section = driver.find_element(By.XPATH, '//*[@id="comments"]')
        comments_author = driver.find_element(By.XPATH, '//*[@id="author-text"]')
        comments_count = driver.find_element(By.XPATH, '//*[@id="count"]/yt-formatted-string/span[1]')
        video_title = driver.find_element(By.XPATH, '//*[@id="title"]/h1/yt-formatted-string')
        likes_count = driver.find_element(By.XPATH,
                                          '//*[@id="segmented-like-button"]/ytd-toggle-button-renderer/yt-button-shape/button/div[2]/span')


        # extract the HTML content of the comments section
        comments_html = comments_section.get_attribute('innerHTML')
        author_html = comments_author.get_attribute('innerHTML')

        # parse the HTML content with BeautifulSoup
        soup_comments = bs(comments_html, 'html.parser')
        soup_author = bs(comments_html, 'html.parser')
        # soup_comments_count = bs(comments_count_html,'html.parser')

        # extract the text of the comments
        comments = [comment.text for comment in
                    soup_comments.find_all('yt-formatted-string', {'class': 'style-scope ytd-comment-renderer'})]
        authors = [author.text.replace("\n", "").strip() for author in soup_author.find_all('a', {'id': 'author-text'})]
        comment_avatar = [avatar.get_attribute('src') for avatar in driver.find_elements(By.XPATH, '//*[@id="author-thumbnail"]/a/yt-img-shadow/img')]

        comments_count_text = comments_count.text
        video_title_text = video_title.text
        likes_count_text = likes_count.text

        lst_comments = []
        # dictionary formation for comments
        for i in range(len(comments)):
            # dict_comments[authors[i]] = comments[i]
            # dict_comments["comment_avatar"] = comment_avatar[i]
            print({"author":authors[i],"comment":comments[i],"avatar":comment_avatar[i]})
            lst_comments.append({"author":authors[i],"comment":comments[i],"avatar":comment_avatar[i]})

        # final json
        scrape_final_sql = {"video_title": video_title_text, 'comments_count': comments_count_text,
                            'likes_count': likes_count_text, 'video_link': links[l],
                            'video_link_downloaded': None, 'thumbnail_link': thumbnails[l]}

        print(scrape_final_sql)
        scrape_final_mongodb = {"video_title": video_title_text, "comments": lst_comments,
                                "thumbnail": base64.b64encode(requests.get(thumbnails[l]).content)}
        print(scrape_final_mongodb)
        print("===============================END===============================")
        # sending data to SQL DB
        sq.data_to_sql(scrape_final_sql)
        md.insert_into_mongo(scrape_final_mongodb)










