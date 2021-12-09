from api.src.models.stocks.views import stock_blueprint
from api.src.models.portfolios.views import portfolio_blueprint
from api.src.models.users.views import user_blueprint
from flask import Flask, render_template, send_from_directory, request, jsonify
from api.src.common.database import Database
from api.src.models.stocks.stock import Stock
from api.src.models.portfolios.portfolio import Portfolio
import api.src.models.portfolios.constants as PortfolioConstants
import api.src.models.stocks.constants as StockConstants
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS  # comment this on deployment
import datetime
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
import webbrowser
import os


# Initialize Flask app
app = Flask(__name__, static_url_path='', static_folder='frontend/build')
#app.config.from_pyfile("config.py")
# app.config.from_object('config')
app.secret_key = "123"
CORS(app)  # comment this on deployment
api = Api(app)

# Initialize Database before running any other command


@app.before_first_request
def init_db_and_rawdata():
    end_date = datetime.datetime.today()
    start_date = end_date - datetime.timedelta(days=1)
    Database.initialize()
    # if raw data collection does not exist at all, push it
    # if Portfolio.check_collection("rawdata") == False:
    #     Stock.push_rawData(PortfolioConstants.START_DATE, end_date)

    # scheduler = BackgroundScheduler()
    # scheduler.add_job(
    #     func=Stock.update_mongo_daily,
    #     args=[start_date, end_date, StockConstants.TICKERS],
    #     trigger="cron",
    #     hour=4,
    #     minute=54,
    #     id="job",
    # )
    # scheduler.start()
    # atexit.register(lambda: scheduler.remove_job("job"))


# Render home page
@app.route("/")
def home():
    return send_from_directory(app.static_folder,'index.html')


# Register views in Flask app
app.register_blueprint(user_blueprint, url_prefix="/users")
app.register_blueprint(portfolio_blueprint, url_prefix="/portfolios")
app.register_blueprint(stock_blueprint, url_prefix="/stocks")


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    print("yo")
    app.run(debug=True, port=port)