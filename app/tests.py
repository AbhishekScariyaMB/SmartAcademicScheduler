from django.test import TestCase
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
# Create your tests here.
class PlayerFormTest(LiveServerTestCase):

  def testform(self):
    selenium = webdriver.Chrome()
    #Choose your url to visit
    selenium.get('http://127.0.0.1:8000/login')
    player_name = selenium.find_element('name','username')
    player_ps = selenium.find_element('name','password')
    
    submit= selenium.find_element('name','submit')

    player_name.send_keys('abzrkz@gmail.com')
    player_ps.send_keys('abzrkz')
    submit.send_keys(Keys.RETURN)

    # assert 'abzrkz@gmail.com' in selenium.page_source