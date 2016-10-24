from app import app, svc, app_state
from flask import session
from flask import flash, redirect, url_for

from app.services.api.yahoo import YahooTeam

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"

@app.route('/test')
def test():
    response = svc.yahoo_api.get_games_info(['nba'])

    game_info = response['fantasy_content']['users']['user']['games']['game']
    teams_info = game_info['teams']
    teams_list = teams_info['team']
    if int(teams_info['@count']) == 1:
        teams_list = [teams_list]

    for team in teams_list:
        this_team = YahooTeam(team['team_key'],
                              team['team_id'],
                              team['name'],
                              url=team['url'])
        app_state.teams[team['team_key']] = this_team


    data = '\n'.join([str((team.name, team.url)) for team in app_state.teams.values()])
    return data



# Yahoo accessors {{{

YAHOO_TOKEN_KEY = 'yahoo_token'

@svc.yahoo_api.api.tokengetter
def get_yahoo_token(token=None):
    return session.get(YAHOO_TOKEN_KEY)

@app.route('/yahoo_login')
def yahoo_login():
    return svc.yahoo_api.authorize(callback=url_for('yahoo_authorized'))

@app.route('/yahoo_authorized')
@svc.yahoo_api.api.authorized_handler
def yahoo_authorized(response):
    if response is None:
        flash(u'Authorization request failed.')
        return redirect(url_for('index'))

    print response

    session[YAHOO_TOKEN_KEY] = (
            response['oauth_token'],
            response['oauth_token_secret'],)

    return redirect(url_for('test'))

# }}}
