import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import requests
import multiprocessing as mp
from cloudinary import CloudinaryImage
import cloudinary
import cloudinary.uploader


def worker():
    GOOGLE_CHROME_PATH = '/app/.apt/usr/bin/google_chrome'
    CHROMEDRIVER_PATH = '/app/.chromedriver/bin/chromedriver'
    PORT = int(os.environ.get('PORT', 11978))
    options1 = Options()
    options1.binary_location = os.environ.get('$GOOGLE_CHROME_BIN')
    options1.add_argument('--no-sandbox')
    options1.add_argument("disable-infobars")
    options1.add_argument("--disable-extensions")

    options1.add_argument('--disable-application-cache')
    options1.add_argument('--disable-gpu')
    options1.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(executable_path=str(os.environ.get('CHROMEDRIVER_PATH')), options=options1)
    driver.maximize_window()
    driver.get('https://tryshowtime.com/c/spotlights')
    print("On the page")
    time.sleep(5)
    i = 0
    old_rest = set()
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(10)
        images = driver.find_elements_by_xpath('//div[@class="relative"]//img')
        ans = set(images) - set(old_rest)  # Remove old elements
        for image in ans:
            i += 1
            link = image.get_attribute('src')
            print(f"got {i}" + "link")
            try:
                img_f = requests.get(link, stream=True)
                with open(f'Image_{i}.jpg', 'wb') as f:
                    f.write(img_f.content)
                # img = Image.open(f'Image_{i}.jpg')
                # if img.mode != 'RGB':
                #    img = img.convert('RGB')
                # img.save(f'Image_{i}.jpg')
                cloudinary.uploader.upload(f'Image_{i}.jpg')
            except:
                pass

            print("Image saved successfully")

            old_rest = images
            # Calculate new scroll height and compare with last scroll height.
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break

            last_height = new_height
            time.sleep(3)


if __name__ == '__main__':
    p = mp.Process(target=worker)
    # run `worker` in a subprocess
    p.start()
    # make the main process wait for `worker` to end
    p.join()
    # all memory used by the subprocess will be freed to the OS

