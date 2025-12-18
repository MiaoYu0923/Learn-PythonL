#CUBS Banking Limited transaction systems
#Student name: Miao Yu
#DDDB module#: IS6143

class CurrencyConverter:
# this class is for converting among different currencies. Euro is the base currency relative to other currencies.
    def __init__(self):
        #use list to store the currency codeS and their exchange rates relative to EURO
        self.currency_codes = ["EURO", "DOLLAR", "POUND"]
        self.exchange_rates = [1.0, 1.1, 0.9]

    def get_currency_index(self, currency):
        #this is for getting the index of the currency code
        currency = currency.upper()
        for i in range(len(self.currency_codes)):
            if self.currency_codes[i] == currency:
                return i
        #if this currency is not in the current currency tuple, return -1 to show it cannot be found
        return -1

    def convert_currency(self, amount, from_currency, to_currency):
        #this is for converting currencies based on different exchange rates
        if amount < 0:
            # amount cannot be negative, so use ValueError to raise an error
            raise ValueError("Amount cannot be negative")
        #get the currency codes
        from_index = self.get_currency_index(from_currency)
        to_index = self.get_currency_index(to_currency)

        if from_index == -1 or to_index == -1:
        # if either index is -1, it cannot be converted then
            raise ValueError("Invalid currency code")

        #convert via EURO as a base currency
        amount_in_euro = amount / self.exchange_rates[from_index]
        converted_amount = amount_in_euro * self.exchange_rates[to_index]
        return converted_amount


    def calculate_fee(self, amount_euro_equivalent):
        # this is for calculating the fee based on the amount of euro
        if amount_euro_equivalent < 100:
            # less than 100 euro, fee rate is 1%
            return amount_euro_equivalent * 0.01
        elif amount_euro_equivalent <= 500:
            # 100 to 500 euro, fee rate is 2%
            return amount_euro_equivalent * 0.02
        else:
            # more than 500 euro, fee rate is 3%
            return amount_euro_equivalent * 0.03


    def add_currency(self, new_currency_name, exchange_rate_to_euro):
        # this is for adding a new currency and its exchange rate
        #convert the currency name to capital letter to in line with the currency codes
        new_currency_name = new_currency_name.upper()

        #if the new currency's index is in the existing currency index list, it means this currency is not new
        if self.get_currency_index(new_currency_name) != -1:
            print(new_currency_name + " already exists, no need to add")
            return

        # check if exchange-rate is positive, it cannot be negative
        if exchange_rate_to_euro <= 0:
            raise ValueError("Exchange rate to euro cannot be negative")

        #add new currency and its exchange rate
        self.currency_codes.append(new_currency_name)
        self.exchange_rates.append(exchange_rate_to_euro)

        print("New currency " + new_currency_name + " is added, the exchange rate is " + str(exchange_rate_to_euro))


class User:
    # this class is used for managing user's information and accounts of different currencies, and handling all kinds of users' operations, including making deposits, withdrawals, currency conversions and transfers.
    def __init__(self, name, email, country, account_id):
        #this is for showing all the basic info of the users
        #attributes: user's name + email + country + account id
        self.name = name
        self.email = email
        self.country = country
        self.account_id = account_id
        #create a currency converter
        self.converter = CurrencyConverter()
        #show the balance of each currency, and initialize the balance to zero
        self.balance = [0.0] * len(self.converter.currency_codes)
        #show transaction history
        self.transaction_history = []

    def get_currency_index(self, currency):
        # to get the index of each currency
        return self.converter.get_currency_index(currency)

    def display_balance(self, currency = None):
        # to display one currency and its balance
        if currency:
            currency_index = self.get_currency_index(currency)
            if currency_index != -1:
                print("The balance of " + currency.upper() + " : " + str(round(self.balance[currency_index],2)))
            else:
                print("This currency is not available")
        else:
            print("All balances: ")
            for i in range(len(self.converter.currency_codes)):
                print(" " + self.converter.currency_codes[i] + " : " + str(round(self.balance[i],2)))
            print()

    def deposit(self, amount, currency):
        # deposit an amount of money to the certain currency account
        currency_index = self.get_currency_index(currency)
        if currency_index == -1:
            raise ValueError("Invalid currency code")
        if amount <= 0:
            raise ValueError("the deposit amount must be positive")

        # record balance
        self.balance[currency_index] += amount

        # record the transaction
        transaction_text = "Operation: Deposit " + " | amount: +" + str(round(amount, 2)) + " " + currency.upper() + " | balance: " + str(round(self.balance[currency_index],2)) + " " + currency.upper()
        self.transaction_history.append(transaction_text)

        print(str(amount) + " " + currency.upper() + " is deposited successfully.")
        self.display_balance(currency)

    def withdraw(self, amount, currency):
        # this is for withdrawing money from one currency account
        currency_index = self.get_currency_index(currency)
        if currency_index == -1:
            raise ValueError("Invalid currency code")
        if amount <= 0:
            raise ValueError("The withdrawal amount must be positive")
        if amount > self.balance[currency_index]:
            raise ValueError("The withdrawal amount exceeds the balance")
        # if no above error, the amount can be deducted from the balance
        self.balance[currency_index] -= amount

        transaction_text = "Operation: Withdraw | amount: -" + str(round(amount, 2)) + " " + currency.upper() + " | balance: " + str(round(self.balance[currency_index], 2)) + " " + currency.upper()
        self.transaction_history.append(transaction_text)

        print(str(amount) + " " + currency.upper() + " is withdrawn successfully.")
        self.display_balance(currency)

    def convert_funds(self, amount, from_currency, to_currency, fee_mode = 1):
        # this is for converting an amount from one currency to another currency with a fee deduction
        # check if the currency exists
        from_index = self.get_currency_index(from_currency)
        to_index = self.get_currency_index(to_currency)

        if from_index == -1 or to_index == -1:
            raise ValueError("Invalid currency code")
        if amount <= 0:
            raise ValueError("The convert amount must be positive")
        if amount > self.balance[from_index]:
            raise ValueError("The convert amount exceeds the balance")

        #calculate the amount of euro to do the further calculation
        from_rate = self.converter.exchange_rates[from_index]
        amount_in_euro = amount / from_rate
        fee_in_euro = self.converter.calculate_fee(amount_in_euro)
        fee_in_from_currency = fee_in_euro * from_rate

        # two modes to deduct the fee
        if fee_mode == 1:
            # mode 1: the fee will be additional, the receiver will receive the exact amount that the user wants to transfer
            total_cost = amount + fee_in_from_currency
            if self.balance[from_index] < total_cost:
                raise ValueError("The convert amount exceeds the balance")

            converted_amount = self.converter.convert_currency(amount, from_currency, to_currency)
            self.balance[from_index] -= total_cost
            self.balance[to_index] += converted_amount

        else:
            # mode 2: the fee will be deducted from the amount, so that the receiver will receive less than the transferred amount
            if self.balance[from_index] < amount:
                raise ValueError("The convert amount exceeds the balance")

            amount_after_fee = amount - fee_in_from_currency
            if amount_after_fee <= 0:
                raise ValueError("The amount after fee exceeds the amount, it cannot be operated.")

            converted_amount = self.converter.convert_currency(amount_after_fee, from_currency, to_currency)
            self.balance[from_index] -= amount
            self.balance[to_index] += converted_amount

        #record the transaction history
        mode_text = "Mode 1: fee will be additional" if fee_mode == 1 else "Mode 2: fee will be deducted from the amount"
        transaction_text = "Operation: Currency exchange(" + mode_text + ")" + " | amount: " + str(round(amount, 2)) + " " + from_currency.upper() + " -> " + str(round(converted_amount, 2)) + " " + to_currency.upper() + " | fee: " + str(round(fee_in_from_currency, 2)) + " " + from_currency.upper() + " | balance: " + str(round(self.balance[from_index], 2)) + " " + from_currency.upper()
        self.transaction_history.append(transaction_text)

        print(str(amount) + " " + from_currency.upper() + " to " + str(round(converted_amount, 2)) + " " + to_currency.upper() + " is converted successfully.")
        print("The fee is " + str(round(fee_in_from_currency, 2)) + " " + from_currency.upper() + " (it is equivalent to " + str(round(fee_in_euro, 2)) + " euro.)")
        self.display_balance()

    def transfer(self, other_user, amount, from_currency, to_currency, fee_mode = 1):
        #this is for transferring funds between users
        if to_currency is None:
            to_currency = from_currency

        print("Transfer: " + self.name + " -> " + other_user.name)

        from_index = self.get_currency_index(from_currency)
        to_index = other_user.get_currency_index(to_currency)

        if from_index == -1 or to_index == -1:
            raise ValueError("Invalid currency code")
        if amount <= 0:
            raise ValueError("The transfer amount must be positive")

        #calculate the fee
        from_rate = self.converter.exchange_rates[from_index]
        amount_in_euro = amount / from_rate
        fee_in_euro = self.converter.calculate_fee(amount_in_euro)
        fee_in_from_currency = fee_in_euro * from_rate

        if fee_mode != 1 and fee_mode != 2:
            raise ValueError("Fee mode must be 1 or 2")

        #fee mode 1: the fee will be deducted additionally
        if fee_mode == 1:
            total_cost = amount + fee_in_from_currency
            if self.balance[from_index] < total_cost:
                raise ValueError("The transfer amount exceeds the balance. Please note that the fee is additional")

            converted_amount = self.converter.convert_currency(amount, from_currency, to_currency)
            self.balance[from_index] -= total_cost
            other_user.balance[to_index] += converted_amount

            print("The transfer(mode 1) is successful!")
            print("Amount from your account: " + str(round(total_cost, 2)) + " " + from_currency.upper() + " (the fee " + str(
                round(fee_in_from_currency, 2)) + " is included)")
            print("The receiver will receive: " + str(round(converted_amount, 2)) + " " + to_currency)

        #mode 2: deduct the fee from the amount directly
        else:
            if self.balance[from_index] < amount:
                raise ValueError("The transfer amount exceeds the balance")

            amount_after_fee = amount - fee_in_from_currency
            if amount_after_fee <= 0:
                raise ValueError("The amount after fee exceeds the amount, it cannot be operated.")

            converted_amount = self.converter.convert_currency(amount_after_fee, from_currency, to_currency)
            self.balance[from_index] -= amount
            other_user.balance[to_index] += converted_amount

            print("The transfer(mode 2) is successful!")
            print("Amount from your account: " + str(round(amount, 2)) + " " + from_currency)
            print("The fee is deducted from the amount: " + str(round(fee_in_from_currency, 2)) + " " + from_currency.upper())
            print("The receiver will receive: " + str(round(converted_amount, 2)) + " " + to_currency.upper())

        #record the transaction history for both parties
        if fee_mode == 1:
            amount_str = str(round(-total_cost, 2))
            mode_str = "Mode 1: fee will be additional"
        else:
            amount_str = str(round(-amount, 2))
            mode_str = "Mode 2: fee will be deducted from the amount"

        tx_from_str = "Operation: Transfer out(" + mode_str + ")" + " | amount: " + amount_str + " " + from_currency.upper() + " | balance: " + str(round(self.balance[from_index], 2)) + " " + from_currency.upper()

        self.transaction_history.append(tx_from_str)

        tx_to_str = "Operation: Transfer in" + " | amount: +" + str(round(converted_amount, 2)) + " " + to_currency.upper() + " | balance: " + str(round(other_user.balance[to_index], 2)) + " " + to_currency.upper()
        other_user.transaction_history.append(tx_to_str)

    def display_transaction_history(self):
        #this is for showing the transaction history of users
        if not self.transaction_history:
            print("User " + self.name + " has no transaction")
            return

        print("All transaction history of " + self.name + ": ")
        for i in range(len(self.transaction_history)):
            print("  " + self.transaction_history[i])
        print("-" * 80)

    def add_new_currency(self, new_currency, exchange_rate_to_euro):
        #add a new currency to both converter and user account balances
        self.converter.add_currency(new_currency, exchange_rate_to_euro)
        self.balance.append(0.0)
        print("Add new account for " + new_currency.upper() + " with a balance 0.0")

def get_valid_input(prompt, input_type, valid_range = None):
    #this is for validating the user's input is correct, set a valid range for the data if necessary, if out of the range, it will raise error
    while True:
        try:
            user_input = input(prompt)

            # convert to the right data type
            if input_type == int:
                value = int(user_input)
            elif input_type == float:
                value = float(user_input)
            elif input_type == str:
                value = user_input
            else:
                raise ValueError("Invalid input type")

            #check allowed range
            if valid_range is not None:
                valid_list = []
                for i in valid_range:
                    valid_list.append(i)

                allowed = False
                for x in valid_list:
                    if value == x:
                        allowed = True
                        break

                if not allowed:
                    raise ValueError("Invalid input range")

            return value

        except ValueError:
            print("Invalid input, please try again. ")
        except Exception as e:
            print("Error: " + str(e))

def main():
    # main function to provide an interactive menu interface
    print("Welcome to CUBS Bank Limited System")
    print()
    print("Step 1: Please create the 1st user")
    # this is for storing all users
    users = []

    def display_main_menu():
        # Menu display
        print()
        print("Main Menu:")
        print("=" * 70)
        print(" 1. Create new account")
        print(" 2. Make a deposit")
        print(" 3. Make a withdrawal")
        print(" 4. Currency exchange")
        print(" 5. Transfer between different users")
        print(" 6. Add new currency")
        print(" 7. Check the balance")
        print(" 8. Check the transaction history")
        print(" 9. Exit the system")
        print("=" * 70)

    def select_user(prompt_text="Please select the user"):
        # this is for selecting the user to proceed
        if not users:
            print("No user in the system! Please create a new user first.")
            return None

        print(prompt_text + ": ")
        for i in range(len(users)):
            idx = i + 1
            user = users[i]
            print("  " + str(idx) + ". " + user.name + " (ID: " + user.account_id + ")")

        valid_list = []
        for i in range(1, len(users) + 1):
            valid_list.append(i)


        choice = get_valid_input("Please select the user#: ", int, valid_list)
        return users[choice - 1]

    while True:
        #to make a loop to return to the menu after each transaction until the user selects to exit the system
        display_main_menu()
        choice = get_valid_input("Please select item (1-9): ", int, [1,2,3,4,5,6,7,8,9])

        # create a new account
        if choice == 1:
            print("--- Create a new account ---")
            try:
                name = get_valid_input("Please enter the name: ", str, None)
                email = get_valid_input("Please enter the email: ", str, None)
                country = get_valid_input("Please enter the country: ", str, None)
                account_id = get_valid_input("Please enter the account ID: ", str, None)

                # to check if the ID exists
                id_exists = False
                for i in range(len(users)):
                    if users[i].account_id == account_id:
                        id_exists = True
                        break

                if id_exists:
                    print("Current ID exists. Please use another ID！")
                    continue

                user = User(name, email, country, account_id)
                users.append(user)
                print("User '" + name + "' is created successfully!")

            except Exception as e:
                print("Failed: " + str(e))

        # 2. Make the deposit
        elif choice == 2:

            user = select_user("Please select the user to make the deposit")

            if not user:
                continue

            print("Select " + user.name + " to deposit")

            try:
                print("Currency: " + str(user.converter.currency_codes))

                currency = get_valid_input("Currency of the deposit: ", str, None)

                amount = get_valid_input("Amount: ", float, None)

                user.deposit(amount, currency)

            except Exception as e:
                print("Failed: " + str(e))

        #withdraw the money
        elif choice == 3:
            user = select_user("Please select the user to make withdrawal")
            if not user:
                continue

            print("For " + user.name + " to make withdrawal")
            try:
                print("Currency: " + str(user.converter.currency_codes))
                currency = get_valid_input("Currency: ", str, None)
                amount = get_valid_input("Amount: ", float, None)

                user.withdraw(amount, currency)

            except Exception as e:
                print("Failed: " + str(e))

        #currency exchange
        elif choice == 4:
            user = select_user("Please select the user")
            if not user:
                continue

            print("For " + user.name + " to make the currency exchange")
            try:
                print("Currency: " + str(user.converter.currency_codes))
                from_currency = get_valid_input("From currency: ", str, None)
                to_currency = get_valid_input("To currency: ", str, None)
                amount = get_valid_input("Amount: ", float, None)

                print("Fee mode:")
                print("  1. The fee will be additional")
                print("  2. The fee will be deduct from the amount")
                fee_mode = get_valid_input("Select mode (1 or 2): ", int, [1,2])

                user.convert_funds(amount, from_currency, to_currency, fee_mode)

            except Exception as e:
                print("Failed: " + str(e))

        # 5. Transfer between different users
        elif choice == 5:
            if len(users) < 2:
                print("Need at least two users to transfer. Please create another user first")
                continue

            from_user = select_user("Please select the user to make the transfer")
            if not from_user:
                continue

            # Please select the receiver
            to_user = None
            while to_user is None:
                temp_user = select_user("Please select the receiver")
                if temp_user is None:
                    break
                if temp_user != from_user:
                    to_user = temp_user
                else:
                    print("Two users cannot be the same one")

            if not to_user:
                continue

            print("Transfer from: " + from_user.name + " → " + to_user.name)
            try:
                print("Currency: " + str(from_user.converter.currency_codes))
                from_currency = get_valid_input("Currency from: ", str, None)
                to_currency_input = get_valid_input("Currency to: ", str, None)

                if to_currency_input == "":
                    to_currency = from_currency
                else:
                    to_currency = to_currency_input

                amount = get_valid_input("Amount: ", float, None)

                print("Fee mode:")
                print("  1. The fee will be additional")
                print("  2. The fee will be deducted from the amount")
                fee_mode = get_valid_input("Select (1 or 2): ", int, [1,2])

                from_user.transfer(to_user, amount, from_currency, to_currency, fee_mode)

            except Exception as e:
                print("Failed: " + str(e))

        # 6. Add new currency
        elif choice == 6:
            if not users:
                print("No account exists. Please create an account first")
                continue

            print("Add new currency")
            try:
                currency_name = get_valid_input("New currency name: ", str)
                exchange_rate = get_valid_input("The exchange rate to EURO: ", float)

                #check if the new currency exists
                currency_exists = False
                for user in users:
                    if user.converter.get_currency_index(currency_name) != -1:
                        currency_exists = True
                        break

                if currency_exists:
                    print(currency_name.upper() + " already exists in the system, no need to add")
                    continue

                for user in users:
                    #add the new currency to converter
                    user.converter.currency_codes.append(currency_name.upper())
                    user.converter.exchange_rates.append(exchange_rate)
                    #add the balance
                    user.balance.append(0.0)

                print("New currency " + currency_name.upper() + " is added. The exchange rate is " + str(exchange_rate))
                print(currency_name.upper() + " is successfully added for all users!")

            except Exception as e:
                print("Failed: " + str(e))

        # Check the balances
        elif choice == 7:
            user = select_user("Select the user ")
            if not user:
                continue

            print("The balance of " + user.name + " : ")
            user.display_balance()

        # Check the transaction history
        elif choice == 8:
            user = select_user("Select the user")
            if not user:
                continue

            print("The transaction history of " + user.name + " : ")
            user.display_transaction_history()

        # Exit the system
        elif choice == 9:
            print()
            print("Thanks for using CUBS Banking System. Bye! ")
            print()
            break

        if choice != 9:
            input("Press 'Enter' to continue...")

#run the main()
if __name__ == "__main__":
    main()







