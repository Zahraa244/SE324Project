import threading
import time
import random

# create a class for single bank account management
class bank_account:
    def __init__(self, initial_money=0, owner='sample_account'):

        # initial money in bank account
        self.money = initial_money

        self.owner = owner

        # We will keep each transaction related to money in a text file.
        self.history_file = open('record.txt', 'w')

        self.money_lock = threading.Lock()
        self.printing("\n************************************************************************")
        self.printing('**** %s Account is active with initial balance:%s SAR ***' % (self.owner, self.money))
        self.printing("**************************************************************************\n")

    # function is used to deposit money in a bank account
    def deposit_money(self, total_amount_to_deposit, by='client'):
        self.printing('%s is adding %s SAR in steps on 1 SAR to the account of %s containing %s SAR at the moment' % (
            by, total_amount_to_deposit, self.owner, self.money))
        # run a for loop to add amount in bank account with each transaction of 1 SAR until user completes the total
        # amount deposit.
        for ind in range(0, total_amount_to_deposit):
            # acquire the lock --> no other thread can go beyond this point until lock is released
            self.money_lock.acquire()

            # add +1 in old money in account and print
            old_money = self.money
            self.printing('%s is about to add 1 SAR to account of %s for a new amount of: %s SAR' % (
                by, self.owner, old_money + 1))
            self.money = old_money + 1

            #release the lock
            self.money_lock.release()

            time.sleep(0.01)

    # function is used to withdraw money from a bank account
    def withdraw_money(self, total_amount_to_withdraw, by='user'):
        self.printing('%s is about to withdraw %s SAR in steps of 1 SAR from account of %s containing %s SAR at the '
                      'moment' % (by, total_amount_to_withdraw, self.owner, self.money))
        for ind in range(0, total_amount_to_withdraw):
            if self.money != 0:
                self.money_lock.acquire()

                old_money = self.money
                self.printing('%s is about to withdraw 1 SAR from account of %s for a new amount of: %s SAR' % (
                    by, self.owner, old_money - 1))
                self.money = old_money - 1

                self.money_lock.release()

            #if account has zero balance --> no withdraw is allowed
            else:
                self.printing("%s tried to withdraw 1 SAR, but account of %s has zero balance, so, the transaction is "
                              "unsuccessful\n" % (by, self.owner))

            time.sleep(0.01)


    # function to write operations in text file
    def printing(self, text):
        print(text)
        if self.history_file:
            self.history_file.write(text + "\n")


    def __del__(self):
        self.printing("\nAll threads completed their tasks")
        # show current balance
        self.printing("\n**********************************************")
        self.printing("%s account current Balance:%s" % (self.owner, self.money))
        self.printing("**********************************************")
        #opened file for records, need to be closed
        self.history_file.close()


def main():
    #random number generation
    initial_balance = random.randint(0,100)
    # create an account with name of client
    main_account = bank_account(initial_balance, "Owner")

    # create an empty array of threads
    list_of_threads = []

    print("creating deposit users/threads")
    # create 5 number of users depositing in account simultaneously depositing total of 25 SAR.
    for start_thread in range(1, 6):
        t = threading.Thread(target=main_account.deposit_money, args=(25, 'User_%d' % (start_thread,)))
        list_of_threads.append(t)
        t.start()

    print("creating withdraw users/threads")
    # create 2 number of users each withdrawing 25 SAR from account simultaneously
    for start_thread in range(6, 8):
        t = threading.Thread(target=main_account.withdraw_money, args=(25, 'User_%d' % (start_thread,)))
        list_of_threads.append(t)
        t.start()

    for t in list_of_threads:
        t.join()  # Wait until all thread terminates its task


if __name__ == "__main__":
    main()
