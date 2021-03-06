#!/usr/bin/python
import argparse
import sys
import pytest
import time
import json
import os.path
import shutil
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
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

file_backup_folder = os.path.dirname(args.file) + "/"+ "finished_transfer_movies" + "/" + os.path.basename(args.file)

class TestBitchuteUploadClass(object):
  def __init__(self, name, file, thumb, email, password, visibly_advice):
    self.name = name
    self.file = file
    self.thumb = thumb
    self.email = email
    self.password = password
    self.visibly_advice = visibly_advice

  def setup_method(self, method):
    self.driver = webdriver.Chrome()
    self.vars = {}
  
  def teardown_method(self, method):
    self.driver.quit()
  
  def test_bitchuteUploadClass(self):
     while True:
        try:
           self.driver.get("https://www.bitchute.com/")
           print(" ** Connection to bitchute.com succeeds!")
           print(" ** Upload Video: " + self.name + "!")
        except:
           time.sleep(2.0)
           print(" ** Network connection failure!")
           time.sleep(4.0)
           print(" ** Retry connecting to bitchute.com!")
           continue
        else:
           break
        
     while True:
       try:
          #self.driver.minimize_window()
          self.driver.set_window_size(880, 640)
          self.driver.set_window_position(90, 90)
       except:
          continue
       else:
          break

     ## Login process
     while True:
        try:
           self.driver.find_element(By.LINK_TEXT, "Login").click()
           WebDriverWait(self.driver, 30).until(expected_conditions.visibility_of_element_located((By.XPATH, "//input[@id=\'id_username\']")))
           self.driver.find_element(By.XPATH, "//input[@id=\'id_username\']").click()
           self.driver.find_element(By.CSS_SELECTOR, "#id_username").send_keys(self.email)
           self.driver.find_element(By.XPATH, "//input[@id=\'id_password\']").click()
           self.driver.find_element(By.CSS_SELECTOR, "#id_password").send_keys(self.password)
           #self.driver.set_timeout(60) # seconds
           self.driver.find_element(By.ID, "auth_submit").click()
           WebDriverWait(self.driver, 30).until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, ".fa-upload > path")))
        except:
           continue
        else:
           break
           
     ## Check bitchute Upload bottom and try to click it - on timeout or failure retry it, till will succeed!
     while True:
        # Go to upload page if possible!
        while True:
           try:
              self.driver.find_element(By.CSS_SELECTOR, ".fa-upload > path").click()
              #self.driver.set_timeout(60) # seconds
              WebDriverWait(self.driver, 30).until(expected_conditions.visibility_of_element_located((By.ID, "publish")))
           except TimeoutException as ex:
               continue
           except:
               self.driver.back()
               continue
           else:
               break
        break

    ## If not failure on connectinng to bitchute upload subdomain  page! 
    ##Continue workflow - on Subdomain with Upload interface!
     while True:
       try:
          self.driver.find_element(By.XPATH, "//input[@id=\'title\']").send_keys(self.name)
          self.driver.find_element(By.XPATH, "//input[@id=\'title\']").click()
          self.driver.find_element(By.XPATH, "//option[@value=\'"+ self.visibly_advice + "\']").click()
       except:
          continue
       else:
          break

     #self.driver.find_element(By.XPATH, "//label[contains(.,\'Publish right away\')]").click()

     while True:
       try:
          WebDriverWait(self.driver, 30).until(expected_conditions.visibility_of_element_located((By.XPATH, "//div[@id=\'videoInput\']/div/label")))
          self.driver.find_element(By.NAME, "thumbnailInput").send_keys(self.thumb)
          time.sleep(5.0)
          while True:
             try:
                WebDriverWait(self.driver, 30).until(expected_conditions.visibility_of_element_located((By.XPATH, "(//button[@type=\'button\'])[8]")))
             except:
                try:
                   WebDriverWait(self.driver, 30).until(expected_conditions.visibility_of_element_located((By.XPATH, "(//button[@type=\'button\'])[7]")))
                   self.driver.find_element(By.CSS_SELECTOR, ".filepond--action-remove-item").click()
                   WebDriverWait(self.driver, 30).until(expected_conditions.visibility_of_element_located((By.XPATH, "//div[@id=\'videoInput\']/div/label")))
                   self.driver.find_element(By.NAME, "thumbnailInput").send_keys(self.thumb)
                   #self.driver.find_element(By.XPATH, "(//button[@type=\'button\'])[7]").click()
                   continue
                except:
                   continue
             else:
                break
             break
       except:
          continue
       else:
          break

     while True:
       try:
          WebDriverWait(self.driver, 30).until(expected_conditions.visibility_of_element_located((By.XPATH, "//div[@id=\'videoInput\']/div/label")))
          self.driver.find_element(By.NAME, "videoInput").send_keys(self.file)
          time.sleep(5.0)
          while True:
             try:
                WebDriverWait(self.driver, 30).until(expected_conditions.visibility_of_element_located((By.XPATH, "(//button[@type=\'button\'])[7]")))
             except:
                try:
                    WebDriverWait(self.driver, 30).until(expected_conditions.visibility_of_element_located((By.XPATH, "(//button[@type=\'button\'])[6]")))
                    self.driver.find_element(By.XPATH, "(//button[@type=\'button\'])[6]").click()
                    continue
                except:
                    continue
             else:
                break
             break
       except:
          continue
       else:
          break

     while True:
        try:
           title = self.driver.title
           if title == "Upload":
              print("Click Upload Bottum")
              time.sleep(2.0)
              self.driver.find_element(By.XPATH, "//button[@type=\'submit\']").click()
           else:
              print("Upload of: " + self.name + " is complete and succeeds!")
              break
        except:
           continue

     time.sleep(4.0)
     while True:
        try:
           self.driver.find_element(By.CSS_SELECTOR, "#notifylink path").click()
           title = self.driver.title
           if title == "Notifications - BitChute":
              self.driver.close()
              break
           else:
              continue
        except:
           continue
  
Bitchute = TestBitchuteUploadClass(args.name, args.file, args.thumbnail, args.email, args.password, args.visibly_advice)

Bitchute.setup_method("")

while True:
   try: 
      Bitchute.test_bitchuteUploadClass()
   except:
      print("Retry Upload")
   else:
      print ("Move " + args.file + " to " + file_backup_folder)
      shutil.move(args.file, file_backup_folder)
      break

Bitchute.teardown_method("")

