from flask import Flask
app = Flask(__name__)

from services import AppState
app_state = AppState()

from services import Services
svc = Services()

from app import views
