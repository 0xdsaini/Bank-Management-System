#!/usr/bin/env python
"""Bank Accounts Management System."""

import time
import json

def save(name, balance, ac_type, last_interest_time):
    """Persist data on external media.
    The order of data will be same as parameters order."""

    #Will save data on 'accounts' file.
    try:
        with open('accounts', 'w') as accounts:
            json.dump([name, balance, ac_type, last_interest_time], accounts)

        return True

    except IOError: 
        return False

def load():
    """Load data saved by _save_ function."""

    #Will read accounts data from 'accounts' file.
    return json.load(open('accounts'))

class Manage(object):
    """Class for managing deposit, withdraw, interest and
       for getting balance details.

       For eg:-

       >>> my_name = Manage("Your Name", 100000)
       
       >>> my_name.get_balance()
       100000
       
       >>> my_name.deposit(5000)
       >>> my_name.get_balance()
       105000

       >>> my_name.withdraw(15000)
       >>> my_name.get_balance()
       95000

       >>> my_name._save_()
       True

       Now, after 1 day, if you check for balance...

       >>> my_name = Manage(None, migrate=True)
       >>> my_name.get_balance()
       95095

       This is what it also manages "interest".

       """

    def __init__(self, name, init_balance=0, ac_type=1, migrate=None):

        if migrate: #Migrating data from account file.

            name, init_balance, ac_type, last_interest_time = load()

        #----------------------------------------

        self.name = name #Name of AC Holder.

        if isinstance(init_balance, (int, long, float)):
            #Changing type to "float" assures for more precise calculations.
            self.main_balance = float(init_balance) #Initial balance in account.

        else:
            raise Exception("Cannot create account! \
                Invalid initial balance "+type(init_balance))

        self.ac_type = ac_type #Type of accounts i.e. 1="Savings Account".

        ##Types of interests i.e 1="Simple", 2="Compound".
        # self.__interest_type__ = interest_type

        self.interest = 0 #Total interest of amount.

        if self.ac_type == 1: #ac_type "1" is "Savings Account".

            #Interest per month (30 days) in percentage.
            self.interest_rate = 3 

        #----------------------------------------

        #If this is migration from file then get time from file's time.
        try:
            self.last_interest_time = last_interest_time
        #else this should be the new account creation. So, store current time.
        except NameError:
            self.last_interest_time = time.time() 

    def _save_(self):
        """Calls the save function(in global scope) to save data on file."""

        self._update_()

        output = save(self.name, self.main_balance, self.ac_type,
                      self.last_interest_time)

        return output

    def _load_(self):
        """No need of load method because
           accounts data are needed be loaded on instantiation,
           no reason to do that after instantiation."""

        pass

    def _interest_(self):
        """Calculates and return interest on the basis of "main_balance",
        "interest_rate" and "last_interest_time."""

        new_interest_time = time.time()

        #Time difference between last interest time and current time.
        diff_time = new_interest_time - self.last_interest_time

        #Updating the last interest time with current time.
        self.last_interest_time = new_interest_time 

        #days = No. of days(24 hrs) passed from last_interest_time till now.
        days = diff_time//(60*60*24)

        #Interest rate today on 'day' basis.
        interest_rate = float(self.interest_rate)/float(30) * days

        self.interest = (self.main_balance/100) * interest_rate

        return self.interest

    def _update_(self):
        """Updates main balance on demand."""

        self.main_balance += self._interest_()

    def deposit(self, amount):
        """Adds amount into account's main balance"""

        self._update_()

        if isinstance(amount, (int, long, float)):
            self.main_balance += amount

        else:
            raise ValueError("Invalid amount.")

    def withdraw(self, amount):
        """Subtracts amount from account's main balance"""

        self._update_()

        if isinstance(amount, (int, long, float)):
            self.main_balance -= amount

        else:
            raise ValueError("Invalid amount.")

    def get_bal(self):
        """Returns current main balance"""

        self._update_()
        
        return self.main_balance

    def __str__(self):

        return "AC_Manage<%s>" % (self.name)

    __repr__ = __str__
