import logging
import inspect

from selenium.webdriver import ActionChains
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class BasePage:

    def __init__(self, driver, url):
        self.driver = driver
        self.url = url

    def open(self):
        self.driver.get(self.url)

    def element_is_visible(self, locator, timeout=5):
        self.go_to_element(self.element_is_present(locator))
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )

    def elements_are_visible(self, locator, timeout=5):
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_all_elements_located(locator)
        )

    def element_is_present(self, locator, timeout=5):
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(locator)
        )

    def elements_are_present(self, locator, timeout=5):
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_all_elements_located(locator)
        )

    def element_is_not_visible(self, locator, timeout=5):
        return WebDriverWait(self.driver, timeout).until(
            EC.invisibility_of_element_located(locator)
        )

    def element_is_clickable(self, locator, timeout=5):
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )

    def go_to_element(self, locator):
        self.driver.execute_script(
            "arguments[0].scrollIntoView();",
            locator
        )

    def action_move_to_element(self, locator):
        action = ActionChains(self.driver)
        action.move_to_element(locator)
        action.perform()

    def action_double_click(self, locator):
        action = ActionChains(self.driver)
        action.double_click(locator)
        action.perform()

    def action_right_click(self, locator):
        action = ActionChains(self.driver)
        action.context_click(locator)
        action.perform()

    def action_drag_and_drop_by_offset(self,
                                       locator,
                                       x_coord,
                                       y_coord):
        action = ActionChains(self.driver)
        action.drag_and_drop_by_offset(
            locator,
            x_coord,
            y_coord
        )
        action.perform()

    def action_drag_and_drop_to_element(self,
                                        chosen_draggable_item,
                                        drag_to_position):
        action = ActionChains(self.driver)
        action.drag_and_drop(
            chosen_draggable_item,
            drag_to_position
        )
        action.perform()

    def remove_footer(self):
        self.driver.execute_script(
            "document.getElementsByTagName('footer')[0].remove();"
        )
        self.driver.execute_script(
            "document.getElementById('close-fixedban').remove();"
        )

    def hide_ads(self):
        all_iframes = self.driver.find_elements(
            By.TAG_NAME,
            "iframe"
        )
        if len(all_iframes) > 0:
            self.driver.execute_script("""
                var elems = document.getElementsByTagName("iframe"); 
                for(var i = 0, max = elems.length; i < max; i++)
                     {
                         elems[i].hidden=true;
                     }
                                  """)

    def hide_image_ads(self):
        all_img_ads = self.driver.find_elements(
            By.TAG_NAME,
            "img"
        )
        if len(all_img_ads) > 0:
            self.driver.execute_script("""
                var elems = document.getElementsByTagName("img"); 
                for(var i = 0, max = elems.length; i < max; i++)
                     {
                         elems[i].hidden=true;
                     }
                                  """)

    def go_to_alert(self):
        return self.driver.switch_to.alert

    def go_to_new_window(self, index):
        self.driver.switch_to.window(self.driver.window_handles[index])

    def go_to_frame(self, locator):
        self.driver.switch_to.frame(locator)

    def go_to_default_content(self):
        self.driver.switch_to.default_content()

    def select_option_by_text(self, locator, value):
        select = Select(self.element_is_present(locator))
        select.select_by_visible_text(value)

    @staticmethod
    def get_logger():
        logger_name = inspect.stack()[1][3]
        logger = logging.getLogger(logger_name)
        file_handler = logging.FileHandler('logfile.log')
        formatter = logging.Formatter(
            "%(asctime)s : %(levelname)s : %(name)s : %(message)s"
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        logger.setLevel(logging.DEBUG)
        return logger
