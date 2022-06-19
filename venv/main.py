# By: Timothy Metzger
# Date: 6/18/2022
import time
from bs4 import BeautifulSoup
import re

from selenium import webdriver
import chromedriver_autoinstaller
from selenium.webdriver.chrome.options import Options
import winsound

def main():
    WINDOW_SIZE = "1920,1080"

    # Install chomredriver and set PATH if not found
    chromedriver_autoinstaller.install()
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)



    driver = webdriver.Chrome(options=chrome_options)

    # Accept a url on first run
    url = "https://www.specialized.com/us/en/s-works-torch/p/200598?color=330081-200598&searchText=61022-03465"

    # Check if the product is available every 11 seconds (Minimum request rate is 10seconds on specialized, so 11 to be safe)
    available = False
    print("Checking on your product...")
    while True:
        driver.get(url)
        time.sleep(5)
        html = driver.page_source


        soup = BeautifulSoup(html, 'html.parser')

        regex = re.compile('^Toast__Container.*')
        toast_div = soup.find_all("div",attrs={"class": regex})


        print("Shoes: 46.5 - wide \t\t\t",end="")
        if len(toast_div) == 0:
            print('Available')
        else:
            availability_text = toast_div[0].find('p').text

            if availability_text == "Out of Stock Online":
                print("Not Available")

            else:
                available = True
                print("Available")

        if available:
            break

        time.sleep(6)
        print('\n')

    while True:
        # Play system sound at 800 Hz for 0.5 seconds
        winsound.Beep(800,500)
        time.sleep(0.25)



if __name__ == "__main__":
    main()