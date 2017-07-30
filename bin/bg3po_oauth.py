import logging
import configparser

log = logging.getLogger(__name__)

config_file_name = "/home/bg3po/.config/praw.ini"
from pathlib import Path

config_file = Path(config_file_name)
if not config_file.is_file():
    print("Missing praw.ini value with /r/boardgames customized values, stick it in ", config_file_name)
    
def login():
    import praw
    #I'm parsing the config file because praw isn't....  
    config = configparser.ConfigParser()
    config.read(config_file_name)
    # todo: make it error out on file missing
    print("found: ", config.sections(), " if this doens't have bg3po_helper_scripts, you have a generic file")
    bg3po = config['bg3po_helper_scripts']
    log.info('logging into reddit')
    r = praw.Reddit(
	client_id=bg3po['client_id'],
        client_secret=bg3po['client_secret'],
        user_agent=bg3po['user_agent'],
        redirect_uri=bg3po['oauth_redirect_uri'],
        refresh_token=bg3po['refresh_access_information'],
        scopes=bg3po['scopes']
    )
    log.info('connected. logging in.')
    return r
