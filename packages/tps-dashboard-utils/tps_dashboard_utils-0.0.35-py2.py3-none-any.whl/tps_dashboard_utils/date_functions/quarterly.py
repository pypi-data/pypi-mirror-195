import datetime as dt
from dateutil.relativedelta import relativedelta


def current_quarter():
    """
    Returns the number of the current quarter
    """
    quarters = [4,4,4,1,1,1,2,2,2,3,3,3]
    return quarters[dt.date.today().month]


def start(last=False):
    """
    Returns the first date of the current quarter by default.
    Use last=True to get the first date of the last quarter.
    """
    quarter = 4

    year = dt.date.today().year

    starts = {1: 4, 2: 7, 3: 10, 4: 1}
    if last == False:
        quarter = current_quarter()
    else:
        if current_quarter() > 1:
            quarter == current_quarter() - 1
        else:
            pass

    return dt.date(year, starts[quarter], 1)


def end(last=False):
    """
    Returns the last date of the current quarter by default.
    Use last=True to get the last date of the previous quarter.
    """
    start_date = start(last=last)
    return start_date + relativedelta(months=3, days=-1)

