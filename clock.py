from apscheduler.schedulers.blocking import BlockingScheduler
from api.src.common.database import Database
from api.src.models.stocks.stock import Stock
from api.src.models.portfolios.portfolio import Portfolio
import api.src.models.portfolios.constants as PortfolioConstants
import api.src.models.stocks.constants as StockConstants
import datetime

sched = BlockingScheduler()
@sched.scheduled_job('cron', day_of_week='mon-fri', second=55)
def scheduled_job():
    end_date = datetime.datetime.today()
    start_date = end_date - datetime.timedelta(days=1)
    Database.initialize()
    if Portfolio.check_collection("rawdata") == False:
        Stock.push_rawData(PortfolioConstants.START_DATE, end_date)
    Stock.update_mongo_daily(start_date, end_date, PortfolioConstants.TICKERS)

sched.start()