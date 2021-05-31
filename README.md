### Requirements:
- git
- pip3 
- python3.6.x 
- selenium4.x
- beautifulsoup4

### Execution in script:

Create a virtual environment (optional)
```
virtualenv -p python3 env_follow_user_fb && source env_follow_user_fb/bin/activate
```
clonate projects:
```
git@github.com:alejandrohdo/follow_user_fb.git
```

install dependencies
```
pip install -r install requeriments.txt
```
download driver seleniuim python and copy /home/{user}: https://chromedriver.chromium.org/downloads

Run .py is  loggind fb
```
python follow_recommended_users_fb.py
```
 
run .py, log in and authenticate on facebook

Note: the session is automatically saved in your profile in path: /home/user-xxx/.config/google-chrome/fb-user-profile/ 

```
python follow_recommended_users_fb.py -user='username o email fb' -pas='*******'
```
