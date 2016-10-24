import os
import xmltodict
from flask_oauthlib.client import OAuth


class YahooAPI:
    client_envvar = 'YAHOO_CLIENT_ID'
    secret_envvar = 'YAHOO_CLIENT_SECRET'

    service_name = 'yahoo'
    request_token_URL = 'https://api.login.yahoo.com/oauth/v2/get_request_token'
    access_token_URL = 'https://api.login.yahoo.com/oauth/v2/get_token'
    request_auth_URL = 'https://api.login.yahoo.com/oauth/v2/request_auth'
    base_URL = 'http://fantasysports.yahooapis.com/fantasy/v2/'
    fmt = 'json'

    def __init__(self):
        # access client key and secret from environment variables
        key = os.getenv(YahooAPI.client_envvar, None)
        secret = os.getenv(YahooAPI.secret_envvar, None)

        if key is None or secret is None:
            raise LookupError("""
Unable to identify API client.
Ensure environment variables for {} and {} are set correctly.
""".format(YahooAPI.client_envvar, YahooAPI.secret_envvar))

        self.oauth = OAuth()
        self.api = self.oauth.remote_app(
                        name=YahooAPI.service_name,

                        consumer_key=key,
                        consumer_secret=secret,

                        request_token_url=YahooAPI.request_token_URL,
                        access_token_url=YahooAPI.access_token_URL,
                        authorize_url=YahooAPI.request_auth_URL,

                        base_url=YahooAPI.base_URL)

        self.game_key = 'nba'


    # Yahoo generic helper functions {{{
    def __construct_user_uri(self):
        return "users;use_login=1"

    def __construct_uri(self, collection, keys=[]):
        '''
        '''
        uri = "/"
        uri += collection

        def resource_keys(keys):
            return ','.join(str(key) for key in keys)

        if len(keys) > 0:
            uri += "="
            uri += resource_keys(keys)

        return uri

    def __get(self, uri):
        return self.api.get(uri)

    # }}} - Yahoo generic helper functions
    # Yahoo API accessing {{{

    def authorize(self, **kwargs):
        return self.api.authorize(**kwargs)

    # Leagues information {{{

    def get_games_info(self, keys):
        '''
        '''
        uri = self.__construct_user_uri()
        uri += self.__construct_uri('games;game_keys', keys=keys)
        uri += self.__construct_uri('teams')

        response = self.__get(uri)
        if response.status != 200:
            return None

        print response.raw_data

        info = xmltodict.parse(response.raw_data)
        return info

    def get_leagues_info(self):
        uri = 'league//'
        return self.__get(uri)

    # }}} - Leagues information

    # }}} - Yahoo API accessing


class YahooTeam:
    def __init__(self, team_key, team_id, name, **kwargs):
        self.team_key = team_key
        self.team_id = team_id
        self.name = name

        self.url = kwargs.get('url', None) 

