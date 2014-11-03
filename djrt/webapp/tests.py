from selenium import webdriver
# from selenium.webdriver.common.keys import Keys

from django.test import LiveServerTestCase
# from django.conf import settings


class SimpleSeleniumTest(LiveServerTestCase):

    def setUp(self):

        self.browser = webdriver.Firefox()
        # settings.DEBUG = True

    def tearDown(self):

        self.browser.quit()

    def test_login(self):

        self.browser.get(self.live_server_url + '/login/')
        self.browser.find_element_by_id('logo')
