from .base import FunctionalTest

class LayoutAndStylingTest(FunctionalTest):

    def test_layout_and_styling(self):
        #User goes to homepage
        self.browser.get(self.server_url)
        self.browser.set_window_size(1024, 768)

        #she notices the input box is nicely centered

        inputbox = self.get_item_input_box()
        # inputbox.send_keys('testing\n')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2, 
            510,
            delta = 5)