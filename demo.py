from selenium import webdriver
# from selenium.webdriver.common.keys import Keys

# driver = webdriver.Firefox()
# driver.get("http://www.python.org")
# assert "Python" in driver.title
# elem = driver.find_element_by_name("q")
# elem.clear()
# elem.send_keys("pycon")
# elem.send_keys(Keys.RETURN)
# assert "No results found." not in driver.page_source
# driver.close()
import time
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions
from pytesseract import image_to_string 
from PIL import Image 
import pandas as pd



driver = webdriver.Firefox(executable_path="./geckodriver")
driver.get('http://court.mah.nic.in/courtweb/index_eng.php')
driver.set_window_size(1120, 900)
driver.find_element_by_xpath("//select[@id='sess_dist_code']/option[text()='Pune-पुणे ']").click()
driver.find_element_by_xpath("//a[@href='javascript:void(0)' and text()='Court Orders']").click()
driver.find_element_by_xpath("/html/body/form/div/div[1]/div[3]/div[3]/div[2]/div/ul/li[2]/div[2]/ul/li[4]/a").click()
# driver.find_element_by_xpath("//select[@id='sess_dist_code']/option[text()='Pune-पुणे ']").click()
# time.sleep(5)
# driver.find_element_by_xpath("//select[@id='court_complex_code']").click()
# /html/body/form/div[2]/div[3]/span[3]/select/option[12]

# driver.implicitly_wait(3)
# elem = driver.find_element_by_xpath("/html")
# print(elem.get_attribute('innerHTML'))
# WebDriverWait(driver, 3).until(
#     expected_conditions.text_to_be_present_in_element(
#         (By.ID, 'caseNoDet'),
#         'Court Complex'
#     )
# )
# caseNoDet


driver.switch_to.frame(driver.find_element_by_xpath('//*[@id="data"]'))
driver.implicitly_wait(1000000000000)
driver.find_element_by_xpath('//*[@id="court_complex_code"]/option[12]').click()

sdate_val = '01-01-2019'
sdate = driver.find_element_by_id("from_date")
sdate.send_keys(sdate_val)

fdate_val = '02-01-2019'
sdate = driver.find_element_by_id("to_date")
sdate.send_keys(fdate_val)

driver.find_element_by_xpath('//*[@id="captcha_label"]').click()

# Capcha part starts here.

# capcha_path = '//*[@id="captcha_image"]'

# element = driver.find_element_by_xpath('//*[@id="captcha_image"]')
# location = element.location    
# size = element.size

# driver.save_screenshot('screenshot.png')
# im = Image.open('screenshot.png')

# left = location['x']    
# top = location['y']    
# right = location['x'] + size['width']    
# bottom = location['y'] + size['height']
# im = im.crop((left, top, right, bottom)) # defines crop points    im.save('screenshot.png')    
# im.save('new.png')
# captcha_text = image_to_string(im)
# Getting the captcha text.
in_text = str(input("Input captcha"))
sdate = driver.find_element_by_id("captcha")
sdate.send_keys(in_text)


#click on final go
driver.find_element_by_name('submit1').click()

tt = driver.find_element_by_xpath('//*[@id="showList1"]')
x = 1
while x == 1:
    e = driver.find_element_by_xpath('/html/body/form/div[2]/div[10]/table/tbody')
    if e.get_attribute('innerHTML') == '':
        time.sleep(1)
    else:
        break

# time.sleep(15)
driver.find_element_by_xpath('/html/body/form/div[2]/div[10]/table/tbody/tr[1]')

table = driver.find_element_by_xpath('//table[@id="showList3"]')

table_html = table.get_attribute('outerHTML')

# text_file = open("Output.txt", "w")
# text_file.write("Purchase Amount: %s" % TotalAmount)
# text_file.close()
df_list = pd.read_html(table_html)
df = df_list[0]
# now breaking the df into four pieces.
df['break'] = ~df['Sr No'].str.isnumeric()
df['break'] = df['break'].astype('int')

break_list = list(df[df['break'] ==1].index)
df.drop('break', axis=1, inplace=True)

dfs = list()
df_name = list()

start = 0
for i in range(0, len(break_list)):
    
    start = break_list[i]
    if break_list[i] == break_list[-1]:
        end = -1
    else:
        end = break_list[i+1]
    curr_df = df.iloc[start+1: end, :]
    dfs.append(curr_df)
    df_name.append(df.iloc[break_list[i],0])
    # start = break_list[i]
    curr_df.to_csv(df_name[i] + '.csv', index=False)

print(df_name)




df.to_csv('df.csv', index=False)
