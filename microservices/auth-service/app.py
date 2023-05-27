import os
from flask import Flask, redirect, url_for, render_template
from flask_dance.contrib.google import make_google_blueprint, google
from dotenv import load_dotenv
import logging


load_dotenv()


app = Flask(__name__)

client_id = os.getenv("GOOGLE_CLIENT_ID")
client_secret = os.getenv("GOOGLE_CLIENT_SECRET")
app.secret_key = os.getenv("SECRET_KEY")

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'

blueprint = make_google_blueprint(
    client_id=client_id,
    client_secret=client_secret,
    reprompt_consent=True,
    scope=["profile", "email"],
    redirect_to="https://buttowsk-effective-halibut-vjqjgq46x6jhwrg4-8081.preview.app.github.dev/login/google/authorized"
)


app.register_blueprint(blueprint, url_prefix="/login")

@app.route("/")
def index():
    google_data = None
    
    user_info_endpoint = "/oauth2/v2/userinfo"
    
    if google.authorized:
        google_data = google.get(user_info_endpoint).json()
        
        
    return render_template("index.j2", google_data=google_data, fetch_url=google.base_url+user_info_endpoint)
        
        
@app.route("/login")
def login():
    return redirect(url_for("google.login"))

@app.route("/login/google/authorized")
def authorized():
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8081)        