# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
from selenium import webdriver
from selenium.webdriver.common.by import By
import re
import cv2
import imutils


def check_screenshot():
    origin_screen_path = "./element_1.png"
    new_screen_path = "./element_2.png"

    # Open the page
    driver = webdriver.Chrome("./chromedriver-2")
    driver.get("https://mint.intuit.com/how-mint-works/alerts")

    # Find widget
    element_1 = driver.find_element(By.XPATH, './/section[contains(@data-com-id,"com-cms-cg-mktg-component-promo")]')
    element_1.screenshot(origin_screen_path)

    # Change style and take new screenshot
    class_attr = element_1.get_attribute("class")
    class_attr = re.sub('cgmt-bgcolor-.*\n', 'cgmt-bgcolor-gray01', class_attr)
    class_attr = re.sub('\n', ' ', class_attr)
    driver.execute_script("arguments[0].setAttribute('class', '"+class_attr+"')", element_1)
    element_1.screenshot(new_screen_path)
    driver.quit()

    # Compare screenshot
    compare_screenshots(origin_screen_path, new_screen_path)


def compare_screenshots(path1, path2):
    original = cv2.imread(path1)
    changed = cv2.imread(path2)
    original = imutils.resize(original, height=600)
    changed = imutils.resize(changed, height=600)

    diff = original.copy()
    cv2.absdiff(original, changed, diff)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    for i in range(0, 3):
        dilated = cv2.dilate(gray.copy(), None, iterations=i + 1)
    (T, thresh) = cv2.threshold(dilated, 3, 255, cv2.THRESH_BINARY)
    cnts = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    for c in cnts:
        # nicely fiting a bounding box to the contour
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(changed, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.imwrite("./changes.png", changed)


if __name__ == '__main__':
    check_screenshot()
