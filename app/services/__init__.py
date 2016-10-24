
class Services:
    '''
    Container for all global services to be used
    in this application

        - Yahoo Fantasy API
    '''
    def __init__(self):
        import api
        self.yahoo_api = api.YahooAPI()


class AppState:
    '''
    '''
    def __init__(self):
        self.teams = {}
