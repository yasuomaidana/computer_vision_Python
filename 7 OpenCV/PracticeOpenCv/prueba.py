from selenium import webdriver #import webdriver from selenium
from selenium.webdriver.common.keys import Keys #obtains special keys as return delete...

driver = webdriver.Chrome() #starts webbrowser
driver.get("http://www.python.org") #go to an specific page
assert "Apple" in driver.title
elem = driver.find_element_by_name("q")
elem.clear()
elem.send_keys("pycon")
elem.send_keys(Keys.RETURN)
assert "No results found." not in driver.page_source
driver.close()