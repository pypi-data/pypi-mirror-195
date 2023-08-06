'''
Nepal-Stock-Tracker

A python script that gets the stock information as per the company symbol
provided by the user from https://merolagani.com/LatestMarket.aspx. This
script supports for the stock information of Nepal only.

By ghanteyyy https://github.com/ghanteyyy
MIT License

Usage:
    - If you want GUI window then Run NepalStockTracker.py directly

    - To get data of respective company only

        from NepalStockTracker import tracker

        data = tracker('Company Symbol', ShowGUI=False)  # Returns stock information of the given company symbol
        print(data.details)  # Printing the stock information from above returned data
'''


__all__ = ['tracker']
__version__ = '0.4.0'
__author__ = 'ghanteyyy'


from NepalStockTracker import main


def tracker(CompanySymbol='', ShowGUI=False):
    '''
    param:
        CompanySymbol  : abbreviation of company name
        ShowGUI        : True | False
    '''

    nsm = main.StockTracker(CompanySymbol, ShowGUI)

    if nsm:
        return nsm
