# By: Timothy Metzger
# Date: 6/18/2022
import time
from bs4 import BeautifulSoup
import re

from selenium import webdriver
import chromedriver_autoinstaller
from selenium.webdriver.chrome.options import Options
import winsound
import os
from colorama import init, Fore, Style

def main():
    # Initialize colorama
    init()

    WINDOW_SIZE = "1920,1080"

    # Install chomredriver and set PATH if not found
    chromedriver_autoinstaller.install()
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
    chrome_options.add_argument('--log-level=3')



    driver = webdriver.Chrome(options=chrome_options)
    os.system('cls')

    # Accept a url on first run
    url = "https://www.specialized.com/us/en/s-works-torch/p/200598?color=330081-200598&searchText=61022-03465"

    # Check if the product is available every 11 seconds (Minimum request rate is 10seconds on specialized, so 11 to be safe)
    available = False
    print(Fore.WHITE + Style.BRIGHT + "Checking on your product...")

    while True:

        driver.get(url)
        check_time = time.localtime(time.time())
        time.sleep(5)
        html = driver.page_source
        os.system('cls')
        print(Fore.WHITE + "Checking on your product\t\t Last Update - ", check_time[3] if check_time[3] <= 12 else check_time[3] - 12,":",check_time[4],":",check_time[5])

        soup = BeautifulSoup(html, 'html.parser')

        regex = re.compile('^Toast__Container.*')
        toast_div = soup.find_all("div",attrs={"class": regex})


        print(Fore.WHITE + "Shoes: 46.5 - wide || ",end="")
        if len(toast_div) == 0:
            print(Fore.GREEN + 'Available')
        else:
            availability_text = toast_div[0].find('p').text

            if availability_text == "Out of Stock Online":
                print(Fore.RED + "Not Available")

            else:
                available = True
                print(Fore.GREEN + "Available")

        if available:
            break

        time.sleep(6)

    while True:
        # Play system sound at 800 Hz for 0.5 seconds
        winsound.Beep(800,500)
        time.sleep(0.25)



if __name__ == "__main__":
    main()