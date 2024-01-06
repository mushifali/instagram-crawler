from typing import List

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


class InstagramCrawlerService:
    """
    Instagram Crawler - It crawls instagram for images.
    """

    def __init__(self):
        self.instagram_images_url = 'https://www.instagram.com/explore/tags/{keyword}/'
        # Create chrome service and install the latest driver
        chrome_service = ChromeService(ChromeDriverManager().install())

        # Enable headless mode (without any GUI)
        chrome_options = Options()
        chrome_options.add_argument('--headless')

        # Create a chrome driver
        self.driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

    def crawl(self, keyword: str, max_images: int = 5) -> List[str]:
        """
        This method crawls instagram for images and returns them in a list of URLs.
        :param keyword: The keyword to search for.
        :param max_images: The maximum number of images to
        :return: A list of images URLs
        """
        # Load the Instagram website with the provided keyword
        self.driver.get(self.instagram_images_url.format(keyword=keyword))
        self._wait_until_the_website_is_loaded()
        # Find all <img> tags
        image_elements = self.driver.find_elements(By.TAG_NAME, 'img')
        # Slice the first 3 elements (instagram logo, meta logo and keyword/hashtag image)
        image_elements = image_elements[3:max_images + 3]

        # Extract the instagram images URLs and return as list
        return list(map(lambda img_element: img_element.get_attribute('src'), image_elements))

    def _wait_until_the_website_is_loaded(self):
        """
        This method waits for the website to load before parsing the HTML. As Instagram
        extensively uses JavaScript, we need to wait for it to completely load the images.
        """
        # Wait until the <main> tag is located in the page
        WebDriverWait(self.driver, timeout=10).until(presence_of_element_located((By.TAG_NAME, 'main')))
