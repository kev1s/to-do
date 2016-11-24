import re 
from django.core import mail
from .base import FunctionalTest

TEST_EMAIL = 'edith@example.com'
SUBJECT = 'Your login link for To-do'

class LoginTest(FunctionalTest):

        def test_can_get_email_link_to_login(self):
                # Edith goes to the awesome superlists site
                # and notices a "Log in" section in the navbar for the first time
                # It's telling her to enter her email address, so she does
                self.browser.get(self.server_url)
                self.browser.find_element_by_name('email').send_keys(
                        TEST_EMAIL + '\n')

                #A message appears telling her an email has been sent
                body = self.browser.find_element_by_tag_name('body')
                self.assertIn('Check your email', body.text)

                #she checks her email and finds a message
                email = mail.outbox[0]
                self.assertIn(TEST_EMAIL, email.to)
                self.assertEqual(email.subject, SUBJECT)

                #it has a url link in it
                self.assertIn('Use this link to login', email.body)
                url_search = re.search(r'http://.+/.+$', email.body)
                if not url_search:           
                    self.fail(
                            'Could not find url in email body:\n{}'.format(email.body))
                url = url_search.group(0)
                self.assertIn(self.server_url, url)

                #she clicks it
                self.browser.get(url)

                #she is logged in!
                self.browser.find_element_by_link_text('Log out')
                navbar = self.browser.find_element_by_css_selector('.navbar')
                self.assertIn(TEST_EMAIL, navbar.text)



