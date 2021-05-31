"""Script que busca personas con mi mi perfil parecido en fb y empieza a seguir o 
agregar como amigo xD
Requerimientoss:
extracion de datos: Fb api y webscraping
Motor de busqueda: apache solr
"""
import argparse
import time
import json
from bs4 import BeautifulSoup
from driver import DriverChrome
from lxml import html
from utils import *
class FollowUserFb(DriverChrome):
    """docstring for FollowUserFb"""
    def __init__(self, user = None, password = None,  *args, **kwargs):
        self.driver=self.init_driver_chrome()
        self.user = user
        self.password = password
        self.url_login = 'https://www.facebook.com/login'
        self.url_home = 'https://www.facebook.com/'
        self.driver.get(self.url_login)
        # only access when it is not login
        if self.verify_login():
            print('is auth Ok')
            #self.main_fb()
            # return self.driver
        else:
            print ("Autentication fb..")
            self.login_user(user, password)

    def query_data_solr(self,keyworks):
    	self.driver.get(url_place)

    def depurate_data_user_profile(self, data_user):
        try:
            data = data_user.split('(ScheduledApplyEach,')[1].replace(');});});</script>', '')
            data_json = json.loads(data)
            # print ('DATA PROFILE:', json.dumps(data_json))
            return data_json.get('require')[7][3][1].get('__bbox').get('result').get('data').get('profile_intro_card').get('bio').get('text')
        except Exception as e:
            try:
                return data_json.get('require')[1][3][1].get('__bbox').get('result').get('data').get('profile_intro_card').get('bio').get('text')
            except Exception as e:
                print ("Its possible not exist summary profile user")

    def get_tree_html(self, response):
        """Functions curation xml html"""
        return html.fromstring(response)

    def get_description(self):
        #extraction description user profile
        try:
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            # self.save_data_html(userName+".html",soup.prettify())
            # save_data_html(username, soup.prettify())
            # data_script = [s for s in soup('script')]
            for script in soup('script'):
                if 'profile_intro_card' in str(script):
                    # print ('SCRIPT PROFILE====>', str(script))
                    return self.depurate_data_user_profile(str(script))
        except Exception as e:
            print ('Error extract description>', e)
            raise e
            # self.driver.close()
            # self.driver.quit()
    def get_driver(self, url):
        """Get driver selenium """
        self.driver.get(url)

    def get_places_recent(self, url_place):
        """Function get recent visits plances user """
        try:
            self.get_driver(url_place)
            time.sleep(2)
            tree = self.get_tree_html(self.driver.page_source)
            xpath_places_recent = "//div[contains(@data-pagelet, 'ProfileAppSection')]//a/span/text()"
            text_places_recent = tree.xpath(xpath_places_recent)
            # print ('DATA:', text_places_recent)
            return text_places_recent
        except Exception as e:
            print ("Error place:", e)

    def get_books(self, username):
        url_books = "https://www.facebook.com/{}/books".format(username)
        self.driver.get(url_books)

    def get_likes_all(self):
        url_likes_all = "https://www.facebook.com/{}/books".format(username)
        self.driver.get(url_likes_all)

    def get_match_my_interest(self, my_interests, data_fb):
        '''Check if I have some kind of interest with the user'''
        is_match_interest = False
        is_match_biografy = False
        if data_fb.get('description_user',{}):
            for my_interest in my_interests.get('interest_biography',{}):
                for data in data_fb.get('description_user',{}):
                    if my_interest.lower() in data.lower():
                        is_match_interest = True
                        break
        if data_fb.get('places_recent_user',{}):
            for my_interest in my_interests.get('my_places',{}):
                for data in data_fb.get('places_recent_user',{}):
                    if my_interest.lower() in data.lower():
                        is_match_biografy = True
                        break
        return is_match_interest,is_match_biografy

    def verify_if_is_my_friend(self, username):
        try:
            button_xpath_add_friend = "(//span[text()='Agregar']/../../../..)[1]"
            python_button = self.driver.find_element_by_xpath(button_xpath_add_friend)
            print('Not is not my friend: {} continuo proccess..'.format(username))
            return True
        except Exception as e:
            print ('Possibly already my friend')
        return False

    def add_my_friend_match(self, username):
        try:
            button_xpath_add_friend = "(//span[text()='Agregar']/../../../..)[1]"
            python_button = self.driver.find_element_by_xpath(button_xpath_add_friend)
            python_button.click()
            print('Add my frend {} ok..'.format(username))
            return True
        except Exception as e:
            print ('Possibly already my friend')
        return False


def main():
    parser = argparse.ArgumentParser()
    #Args username and password login fb
    parser.add_argument('-user', '--user', help='username or email facebook' , required=False)  
    parser.add_argument('-pas', '--pas', required=False, help='password fb') 
    parser.add_argument('arg', nargs='*') # use '+' for 1 or more args (instead of 0 or more)
    parsed = parser.parse_args()
    return (parsed.user, parsed.pas)

if __name__ == "__main__":
    try:
        # verify or init chrome
        load_data_users = get_users_json_data()
        # load_data_users = [{
        #   "id":"564866976",
        #   "name":"Sandra Robles Donayre",
        #   "gender":1,
        #   "vanity":"meliza.ninadavila.1"}]
        my_interests = {'interest_biography': ['datascience', 'big data', 
                    'computación', 'informática', 'meditación', 'meditation', 'educación',
                    'ciencia de datos', 'ia', 'innovación','startup','emprendimientos'],

                    'my_places':['san isidro', 'lima', 'apurimac', 
                    'miraflores', 'pucp','unmsm', 'utec', 'meditación',
                    'unamba', 'uni','la católica','la molina', 'peru', 'perú', '']}
        # mi_driver = DriverChrome()
        user_follow = FollowUserFb(user=main()[0], password=main()[1])
        for user in load_data_users:
            username = user.get('vanity')
            url_user_fb = 'https://www.facebook.com/{}/places_recent'.format(username)
            dict_data_profile_user = {}
            dict_data_profile_user['places_recent_user'] =user_follow.get_places_recent(url_user_fb)
            if not user_follow.verify_url_valid():
                print ('Possibly the url does not exist, was deleted or requires a login to access. Skipping')
                continue
            if user_follow.verify_if_is_my_friend(username):
                dict_data_profile_user['description_user'] = user_follow.get_description()
                is_match_biogray, is_match_interest = user_follow.get_match_my_interest(my_interests, dict_data_profile_user)
                if is_match_biogray or is_match_interest:
                    user_follow.add_my_friend_match(username)
                else:
                    print ('It is likely that the user:{} does not have my interests, adding as a friend is omitted'.format(username))
            else:
                print ('It is possible that the user:{} is already friends'.format(username))
        print('Finish proccess....')
        user_follow.driver.close()
        user_follow.driver.quit()
    except Exception as e:
        print ("Error init driver:", e)
        raise e
