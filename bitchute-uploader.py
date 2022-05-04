#!/usr/bin/python
import argparse
import sys
import pytest
import time
import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options

parse = argparse.ArgumentParser()
parse.add_argument("-n", "--name", required=True, type=str, help="Set Video title for the Video at Bitchute!")
parse.add_argument("-f", "--file", required=True, type=str, help="Set the upload Video for Bitchute!")
parse.add_argument("-t", "--thumbnail", required=True, type=str, help="Set the Thumbnail image of the Video!")
parse.add_argument("-e", "--email", required=True, type=str, help="Set the login E-Mail Address for Bitchute!")
parse.add_argument("-p", "--password", required=True, type=str, help="Set the login Passwort for Bitchute!")
parse.add_argument("-v", "--visibly_advice", required=True, type=str, help="Set the Video content view advice for shocking videos! [10, 40 or 70]")
args = parse.parse_args()

class TestBitchuteUploadClass(object):
  def __init__(self, name, file, thumb, email, password, visibly_advice):
    self.name = name
    self.file = file
    self.thumb = thumb
    self.email = email
    self.password = password
    self.visibly_advice = visibly_advice

  def setup_method(self, method):
    options = Options()
    options.add_argument("start-minimized")
    self.driver = webdriver.Chrome(chrome_options=options)
    self.vars = {}
  
  def teardown_method(self, method):
    self.driver.quit()
  
  def test_bitchuteUploadClass(self):
     self.driver.get("https://www.bitchute.com/")
     while True:
       try:
          self.driver.set_window_size(880, 640)
          self.driver.set_window_position(50, 50)
       except:
          continue
       else:
          break

     ## Login process
     self.driver.find_element(By.LINK_TEXT, "Login").click()
     WebDriverWait(self.driver, 30).until(expected_conditions.visibility_of_element_located((By.XPATH, "//input[@id=\'id_username\']")))
     self.driver.find_element(By.XPATH, "//input[@id=\'id_username\']").click()
     self.driver.find_element(By.CSS_SELECTOR, "#id_username").send_keys(self.email)
     self.driver.find_element(By.XPATH, "//input[@id=\'id_password\']").click()
     self.driver.find_element(By.CSS_SELECTOR, "#id_password").send_keys(self.password)
     self.driver.find_element(By.ID, "auth_submit").click()
     # Re-open Bitchute baseurl!
     while True:
        #self.driver.get("https://www.bitchute.com/")

        # Go to uplpsd page if possible!
        WebDriverWait(self.driver, 30).until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, ".fa-upload > path")))
        self.driver.find_element(By.CSS_SELECTOR, ".fa-upload").click()

        ## Check 3 times the bitchute subdomain loading - (Trying to go to Upload page!)
        time.sleep(4.0)
        title = self.driver.title
        if title != "Upload":
           time.sleep(4.0)
           title = self.driver.title
           if title != "Upload":
              time.sleep(4.0)
              title = self.driver.title
              if title != "Upload":
                 self.driver.back()
                 continue
              else:
                 break
           else:
              break
        else:
           break

    ## Continue workflow <- No failure on bitchute subdomain loading!
     while True:
       try:
          WebDriverWait(self.driver, 30).until(expected_conditions.visibility_of_element_located((By.ID, "publish")))
       except:
          continue
       else:
          break

     while True:
       try:
         self.driver.find_element(By.XPATH, "//input[@id=\'title\']").send_keys(self.name)
       except:
          continue
       else:
          break

     #self.driver.find_element(By.XPATH, "//label[contains(.,\'Publish right away\')]").click()

     while True:
       try:
          WebDriverWait(self.driver, 30).until(expected_conditions.visibility_of_element_located((By.XPATH, "//div[@id=\'videoInput\']/div/label")))
          WebDriverWait(self.driver, 30).until(expected_conditions.visibility_of_element_located((By.XPATH, "//button[contains(.,\'Proceed\')]")))
          self.driver.find_element(By.XPATH, "//input[@id=\'title\']").click()
          self.driver.find_element(By.XPATH, "//option[@value=\'"+ self.visibly_advice + "\']").click()
          self.driver.find_element(By.NAME, "videoInput").send_keys(self.file)
          self.driver.find_element(By.NAME, "thumbnailInput").send_keys(self.thumb)
          WebDriverWait(self.driver, 30).until(expected_conditions.visibility_of_element_located((By.XPATH, "//button[contains(.,\'Proceed\')]")))         
          WebDriverWait(self.driver, 300000000000000000000000000000000000000000000000).until(expected_conditions.visibility_of_element_located((By.XPATH, "(//button[@type=\'button\'])[7]")))
       except:
          continue
       else:
          break

     while True:
        try:
          title = self.driver.title
          if title == "Upload":
             print(title)
             time.sleep(5.0)
             self.driver.find_element(By.XPATH, "//button[@type=\'submit\']").click()
          else:
             break
        except:
          break
        else:
          continue

     time.sleep(4.0)
     self.driver.close()
  
Bitchute = TestBitchuteUploadClass(args.name, args.file, args.thumbnail, args.email, args.password, args.visibly_advice)

Bitchute.setup_method("")
Bitchute.test_bitchuteUploadClass()
Bitchute.teardown_method("")
