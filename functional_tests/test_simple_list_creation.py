from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from .base import FunctionalTest
import sys


class NewVisitorTest(FunctionalTest):

    @classmethod
    def setUpClass(cls):
        for arg in sys.argv:
            if 'liveserver' in arg:
                cls.server_url = 'http://' + arg.split('=')[1]
                return
        super(NewVisitorTest, cls).setUpClass()
        cls.server_url = cls.live_server_url

    # @classmethod
    # def tearDownClass(cls):
    #     if cls.server_url == cls.live_server_url:
    #         super(NewVisitorTest, cls).tearDownClass()

    
    def setUp(self):
        self.browser = webdriver.Chrome('C:\Program Files (x86)\Google\Chrome\Application\chromedriver')
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.refresh()
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        self.browser.get(self.server_url)

        #she notices the page title and header mentions to-do lists
        self.assertIn('To-do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-do', header_text)

        #she has to enter a todo item
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item')

        #She enters Buy Os into a text box
        inputbox.send_keys('Buy Os')

        #when she hits enter the page updates with her new todo items
        inputbox.send_keys(Keys.ENTER)

        #After hitting enter she sees her todo list at a new urld
        edith_list_url = self.browser.current_url
        self.assertRegexpMatches(edith_list_url, '/lists/.+')

        self.check_for_row_in_list_table('1: Buy Os')

        #She then can add a new todo item, she enters Buy goats and hits enter
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy Goats')
        inputbox.send_keys(Keys.ENTER)

        self.check_for_row_in_list_table('2: Buy Goats')
        self.check_for_row_in_list_table('1: Buy Os')
       

        # Now a new user, Francis, comes along to the site.

        ## We use a new browser session to make sure that no information
        ## of Edith's is coming through from cookies etc

        self.browser.quit()


        self.browser = webdriver.Chrome('C:\Program Files (x86)\Google\Chrome\Application\chromedriver')
         # Francis visits the home page.  There is no sign of Edith's
        # list
        self.browser.get(self.server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy Os', page_text)
        self.assertNotIn('Buy Goats', page_text)

        # Francis starts a new list by entering a new item. He
        # is less interesting than Edith...
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)

        # Francis gets his own unique URL
        francis_list_url = self.browser.current_url
        self.assertRegexpMatches(francis_list_url, '/lists/.+')
        self.assertNotEqual(francis_list_url, edith_list_url)

        # Again, there is no trace of Edith's list
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy Goats', page_text)
        self.assertIn('Buy milk', page_text)