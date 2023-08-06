from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import os

from selenium_stealth import stealth
from time import sleep

br = ChromeDriverManager().install()


### options - Options of webdriver
### proxy   - ip of proxy if it's needed
### user_data_dir_ = directory where data of driver will be saved 
#  (default folder fdir1 in current directory)
###
def Get(profile: str, options: Options=None, desired_capabilities=None,
user_data_dir_:str=None, languages: list = None, proxy: str=None, **kwargs):
    if options is None: options = Options()

    if proxy is not None: options.add_argument("--proxy-server=%s" % proxy)

    if user_data_dir_ is None: p = os.path.abspath(os.getcwd()) + "\\" + "fdir1"
    user_data_dir = p

    options.add_argument("start-maximized")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")

    # Chrome is controlled by automated test software
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    options.add_argument("--disable-blink-features=AutomationControlled") 

    
    options.add_argument('--profile-directory=%s' % profile)
    options.add_argument("--user-data-dir=%s" % user_data_dir)

    driver= webdriver.Chrome(br, options=options, 
    desired_capabilities=desired_capabilities, **kwargs)

    # AddCookies(driver)

    if languages is None: languages=["en-US", "en"]
    
    stealth(driver,
        languages=languages,
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Google Inc. (AMD)",
        renderer="ANGLE (AMD, AMD Radeon(TM) Graphics Direct3D11 vs_5_0 ps_5_0, D3D11)",
        # fix_hairline=True,
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
        )

    sleep(2)

    return driver

    