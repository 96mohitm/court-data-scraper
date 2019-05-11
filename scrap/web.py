"""
Author: Mohit
Date: 15/04/2019
Status: Development
"""
from PIL import Image 
from pytesseract import image_to_string 
from selenium import webdriver
import time


class Webpage:
    """
    Website clicks and and crawling.
    """
    def __init__(self):
        self.driver = webdriver.Firefox(executable_path="./geckodriver")

    def fill_value(self, id, val):
        """Fills the value in the html tag using id.
        """
        try:
            sdate = self.driver.find_element_by_id(id)
            sdate.send_keys(val)
        except Exception as ex:
            print("UNABLE TO FILL VALUE IN INPUT BOX")
            print(ex)

    def get_captcha(self):
        """Extracts captcha text using the image.
        """
        try:
            capcha_path = '//*[@id="captcha_image"]'

            element = self.driver.find_element_by_xpath('//*[@id="captcha_image"]')
            location = element.location    
            size = element.size

            self.driver.save_screenshot('screenshot.png')
            im = Image.open('screenshot.png')

            left = location['x']    
            top = location['y']    
            right = location['x'] + size['width']    
            bottom = location['y'] + size['height']
            im = im.crop((left, top, right, bottom))
            im.save('new.png')
            captcha_text = image_to_string(im)
        
        except Exception as ex:
            print(ex)

        finally:
            return captcha_text

    def process(self):
        """The main driver function of Webpage.
        """
        try:
            site = 'http://court.mah.nic.in/courtweb/index_eng.php'
            self.driver.get(site)
            self.driver.set_window_size(1120, 900)

            # Selecting Pune
            self.driver.find_element_by_xpath("//select[@id='sess_dist_code']/option[text()='Pune-पुणे ']").click()

            # Clicking on Court Orders
            self.driver.find_element_by_xpath("//a[@href='javascript:void(0)' and text()='Court Orders']").click()

            # Clicking on Order Date
            self.driver.find_element_by_xpath("/html/body/form/div/div[1]/div[3]/div[3]/div[2]/div/ul/li[2]/div[2]/ul/li[4]/a").click()
            self.driver.implicitly_wait(10)

            # Switching to iframe
            self.driver.switch_to.frame(self.driver.find_element_by_xpath('//*[@id="data"]'))
            
            # Clicking on Court Complex
            self.driver.find_element_by_xpath('//*[@id="court_complex_code"]/option[12]').click()

            # fill date using id
            self.fill_value('from_date', '01-01-2019')
            self.fill_value('to_date', '02-01-2019')

            self.driver.find_element_by_xpath('//*[@id="captcha_label"]').click()

            captcha_text = self.get_captcha()
            print("Auto generated Captcha text: " + captcha_text)

            in_text = str(input("Input captcha "))
            self.fill_value('captcha', in_text)

            #click on final go
            self.driver.find_element_by_name('submit1').click()
            
            # Waiting until the table loads.
            i=0
            while True:
                e = self.driver.find_element_by_xpath('/html/body/form/div[2]/div[10]/table/tbody')
                if i > 30:
                    print("More than 30 seconds and the captcha is wrong.")
                    break

                if not 'tr' in e.get_attribute('innerHTML'):
                    i += 1
                    time.sleep(1)
                else:
                    break

            table = self.driver.find_element_by_xpath('//table[@id="showList3"]')
            self.table_html = table.get_attribute('outerHTML')
        except Exception as ex:
            print(ex)