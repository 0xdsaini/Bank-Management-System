#!/usr/bin/env python
"""Bank Accounts Management System."""

import time

class Manage(object):
    """Class for managing deposit, withdraw and for getting balance details."""

    def __init__(self, name, init_balance=0, ac_type=1):

        self.name = name #Name of AC Holder.
        self.main_balance = init_balance #Initial Balance in Account.
        self.ac_type = ac_type #Type of Account i.e. 1="Savings Account".
        self.time_of_creation = time.time() #Stores time to calculate interests.

        self.interest = 0 #Total interest of amount.

        if self.ac_type == 1: #ac_type "1" is "Savings Account".

            self.interest_rate = 3 #Interest per month(30days) in percentage.

    def _interest_(self):
        """Calculates and return interest on the basis of "main_balance",
        "interest_rate" and "time_of_creation."""

        #Time difference between creation time and today's time.
        diff_time = time.time() - self.time_of_creation

        #No. of days passed from time_of_creation till now.
        days = diff_time//(60*60*24)

        #Interst rate today on 'day' basis.
        interest_rate = float(self.interest_rate)/float(30) * days

        self.interest = (self.main_balance/100) * interest_rate

        return self.interest

    def _update_(self):
        """Updates main balance on demand."""

        self.main_balance += self._interest_()

    def deposit(self, amount):
        """Adds amount into account's main balance"""

        self._update_()

        if isinstance(amount, int):
            self.main_balance += amount

        else:
            raise ValueError("Invalid amount.")

    def withdraw(self, amount):
        """Substracts amount from account's main balance"""

        self._update_()

        if isinstance(amount, int):
            self.main_balance -= amount

        else:
            raise ValueError("Invalid amount.")

    def get_balance(self):
        """Returns current main balance"""

        self._update_()
        
        return self.main_balance

    def __str__(self):

        return "AC_Manage<%s>" % (self.name)

    __repr__ = __str__
    
