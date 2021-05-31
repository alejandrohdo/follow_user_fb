from selenium.webdriver.chrome.options import Options as OptionsChrome
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.firefox.options import Options
from os.path import expanduser
from datetime import datetime, timedelta
import time
import traceback, tldextract

class DriverChrome:

    def verify_login(self):
        """Verificacion la pagina ya se encuentra loqueado
        return True: loqueado, False: sin login"""
        try:
            print("Verify login fb...!")
            text_login = ['Iniciar sesión', 'Log In']
            xpath_check_login = "//button[@id='loginbutton']"
            time.sleep(6)
            check_is_auth = self.driver.find_element_by_xpath(xpath_check_login).text
            print('TEXT:', check_is_auth)
            if check_is_auth in text_login:
                return False
        except Exception as e:
            print ('Is possible loged..!')
        return True

    def init_driver_chrome(self, headless=False, profile=True):
        """Inicilización driver and generate profile, large duration sesión """
        options = OptionsChrome()
        chromeProfilePath = None
        if headless:
            options.headless = True
        else:
            options.headless = False
            options.add_argument("--mute-audio")
        if profile:
            path_home = self.get_user_home_dir_path()
            if '/' in path_home:
                # path linux
                chromeProfilePath = path_home+"/.config/google-chrome/fb-user-profile/"
            else:
                # path windows
                chromeProfilePath = path_home+"\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\fb-user-profile"
            options.add_argument("user-data-dir=%s" % chromeProfilePath)
        return webdriver.Chrome(executable_path='/home/alejandro/chromedriver', chrome_options=options) 

    def get_user_home_dir_path(self):
        """Functions return current path """
        return expanduser("~")    

    def verify_url_valid(self):
        """Verify is url user is exists or valid"""
        message_invalid_url = ['Página no encontrada', 
        'No se pudo encontrar la página', 'Page Not Found']
        if self.driver.title in message_invalid_url:
            return False
        else:
            return True

    def login_user(self, user, password):
        """
        Function login fb
        :return:
        """
        # time.sleep(4)
        try:
            self.driver.find_element_by_id("email").send_keys(user)
            self.driver.find_element_by_id("pass").send_keys(password)
            self.driver.find_element_by_id("loginbutton").click()
            # sgte.send_keys(Keys.RETURN)
            time.sleep(3)
            if not self.verify_login():
                print ('Possibly the username or password are not correct .. try again later xD')
                time.sleep(6)
                self.driver.close()
                self.driver.quit()
                exit()
            self.main_fb()
        except Exception as error:
            print ("Error:", str(traceback.format_exc()))
            self.send_error(str(error), 'login_user')
            # self.driver.close()
            # self.driver.quit()

    def send_error(self, error, f_func):
        """
        this function capture erros driver
        :param error: messaje error
        :param f_func: Name error
        """
        str_error = {
            'file': 'ChromeInstagram - func: %s' % (f_func,),
            'date_error': datetime.now(),
            'user_admin': self.user,
            'menssage': error
        }
        print('========================================================')
        print('file: ', str_error['file'])
        print('date_error: ', str_error['date_error'])
        print('user_admin: ', str_error['user_admin'])
        print('menssage: ', str_error['menssage'])
        print('========================================================')
        # self.start_travel_history()

    def main_fb(self):
        print ('Main....')
        self.driver.get(self.url_home)
        return self.driver