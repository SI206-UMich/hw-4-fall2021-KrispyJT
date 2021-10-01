# Name: Jasper Tinoco
# UMID: 37685125
# Unique Name: jasperth
# Partners: Oresti Dine, Tyler Phillips

import unittest

# The Customer class
# The Customer class represents a customer who will order from the stalls.
class Customer: 
    def __init__(self, name, wallet = 100):
        self.name = name
        self.wallet = wallet

    # Reload some deposit into the customer's wallet.
    def reload_money(self, deposit):
        self.wallet += deposit

    # The customer orders the food and there could be different cases   
    def validate_order(self, cashier, stall, item_name, quantity):
        if not(cashier.has_stall(stall)):
            print("Sorry, we don't have that vendor stall. Please try a different one.")
        elif not(stall.has_item(item_name, quantity)):  
            print("Our stall has run out of " + item_name + " :( Please try a different stall!")
        elif self.wallet < stall.compute_cost(quantity): 
            print("Don't have enough money for that :( Please reload more money!")
        else:
            bill = cashier.place_order(stall, item_name, quantity) 
            self.submit_order(cashier, stall, bill) 
    
    # Submit_order takes a cashier, a stall and an amount as parameters, 
    # it deducts the amount from the customer’s wallet and calls the receive_payment method on the cashier object
    def submit_order(self, cashier, stall, amount): 
        self.wallet -= amount
        cashier.receive_payment(stall, amount)
        
    # The __str__ method prints the customer's information.    
    def __str__(self):
        return "Hello! My name is " + self.name + ". I have $" + str(self.wallet) + " in my payment card."

# The Cashier class represents a cashier at the market. 
class Cashier:

    # Constructor
    def __init__(self, name, directory =[]):
        self.name = name
        self.directory = directory[:] # make a copy of the directory

    # Whether the stall is in the cashier's directory
    def has_stall(self, stall):
        return stall in self.directory

    # Adds a stall to the directory of the cashier.
    def add_stall(self, new_stall):
        self.directory.append(new_stall)

    # Receives payment from customer, and adds the money to the stall's earnings.
    def receive_payment(self, stall, money):
        stall.earnings += money

    # Places an order at the stall.
	# The cashier pays the stall the cost.
	# The stall processes the order
	# Function returns cost of the order, using compute_cost method
    def place_order(self, stall, item, quantity):
        stall.process_order(item, quantity)
        return stall.compute_cost(quantity) 
    
    # string function.
    def __str__(self):

        return "Hello, this is the " + self.name + " cashier. We take preloaded market payment cards only. We have " + str(sum([len(category) for category in self.directory.values()])) + " vendors in the farmers' market."

## Complete the Stall class here following the instructions in HW_4_instructions_rubric
class Stall:
    
    def __init__(self, name, inventory, cost = 7, earnings = 0):
        self.name = name
        self.inventory = inventory
        self.cost = cost
        self.earnings = earnings

    def has_item(self, name, quantity):
        if name in self.inventory.keys() and self.inventory[name] >= quantity: #checks if name in the self inventory AND if the key is greater than or equal to the quantity 
            return True
        else:
            return False
    
    def process_order(self, name, quantity):
        if self.has_item(name, quantity):
            self.inventory[name] -= quantity
            self.earnings += self.cost * quantity
            print("Your order has been processed!") #maybe should be return?
        else:
            pass

    def stock_up(self, name, quantity):
        if name in self.inventory.keys():
            self.inventory[name] += quantity
        else:
            self.inventory[name] = quantity

    def compute_cost(self, quantity):
        return quantity * self.cost

    def __str__(self):
        return "Hello, we are " + self.name + ". This is the current menu " + ", ".join(self.inventory.keys()) + ". We charge $" + str(self.cost) + " per item. We have $" + str(self.earnings) + " in total."


class TestAllMethods(unittest.TestCase):
    
    def setUp(self):
        inventory = {"Burger":40, "Taco":50}
        inventory5 = {"Krabby patty": 25, "chum bucket": 50}
        self.f1 = Customer("Ted")
        self.f2 = Customer("Morgan", 150)
        self.s1 = Stall("The Grill Queen", inventory, cost = 10)
        self.s2 = Stall("Tamale Train", inventory, cost = 9)
        self.s3 = Stall("The Streatery", inventory, cost= 8)
        self.s5 = Stall("Noodles", inventory5)
        self.c1 = Cashier("West")
        self.c2 = Cashier("East")
        self.c3 = Cashier("South")
        #the following codes show that the two cashiers have the same directory
        for c in [self.c1, self.c2]:
            for s in [self.s1,self.s2,self.s3]:
                c.add_stall(s)

	## Check to see whether constructors work
    def test_customer_constructor(self):
        self.assertEqual(self.f1.name, "Ted")
        self.assertEqual(self.f2.name, "Morgan")
        self.assertEqual(self.f1.wallet, 100)
        self.assertEqual(self.f2.wallet, 150)

	## Check to see whether constructors work
    def test_cashier_constructor(self):
        self.assertEqual(self.c1.name, "West")
        #cashier holds the directory - within the directory there are three stalls
        self.assertEqual(len(self.c1.directory), 3) 

	## Check to see whether constructors work
    def test_truck_constructor(self):
        self.assertEqual(self.s1.name, "The Grill Queen")
        self.assertEqual(self.s1.inventory, {"Burger":40, "Taco":50})
        self.assertEqual(self.s3.earnings, 0)
        self.assertEqual(self.s2.cost, 9)

	# Check that the stall can stock up properly.
    def test_stocking(self):
        inventory = {"Burger": 10}
        s4 = Stall("Misc Stall", inventory)

		# Testing whether stall can stock up on items
        self.assertEqual(s4.inventory, {"Burger": 10})
        s4.stock_up("Burger", 30)
        self.assertEqual(s4.inventory, {"Burger": 40})
        
    def test_make_payment(self):
		# Check to see how much money there is prior to a payment
        previous_customer_wallet = self.f2.wallet
        previous_earnings_stall = self.s2.earnings
        
        self.f2.submit_order(self.c1, self.s2, 30)

		# See if money has changed hands
        self.assertEqual(self.f2.wallet, previous_customer_wallet - 30)
        self.assertEqual(self.s2.earnings, previous_earnings_stall + 30)

	# Check to see that the server can serve from the different stalls
    def test_adding_and_serving_stall(self):
        c3 = Cashier("North", directory = [self.s1, self.s2])
        self.assertTrue(c3.has_stall(self.s1))
        self.assertFalse(c3.has_stall(self.s3)) 
        c3.add_stall(self.s3)
        self.assertTrue(c3.has_stall(self.s3))
        self.assertEqual(len(c3.directory), 3)

	# Test that computed cost works properly.
    def test_compute_cost(self):
        #what's wrong with the following statements?
        #can you correct them?
        self.s1.compute_cost(5)
        self.assertEqual(self.s1.compute_cost(5), 50)
        self.s3.compute_cost(6)
        self.assertEqual(self.s3.compute_cost(6), 48)

	# Check that the stall can properly see when it is empty
    def test_has_item(self):
        # Set up to run test cases
        # Test to see if has_item returns True when a stall has enough items left
        self.s1.has_item("Burger", 5)
        self.assertEqual(self.s1.has_item("Burger", 5), True)
        # Please follow the instructions below to create three different kinds of test cases 
        # Test case 1: the stall does not have this food item:
        self.s1.has_item("Fish", 10) 
        self.assertEqual(self.s1.has_item("Fish", 10), False)
        # Test case 2: the stall does not have enough food item: 
        self.s2.has_item("Taco", 100)
        self.assertEqual(self.s2.has_item("Taco", 100), False)
        # Test case 3: the stall has the food item of the certain quantity: 
        self.s2.has_item("Taco", 50)
        self.assertEqual(self.s2.has_item("Taco", 50), True)

	# Test validate order
    def test_validate_order(self):
        # inventory = {"Burger" : 15}
        # s5 = Stall("Another Stall", inventory)
		# case 1: test if a customer doesn't have enough money in their wallet to order
        jacks_wallet = self.f1.wallet

        self.f1.validate_order(self.c1, self.s1, "Burger", 30)
        self.assertEqual(jacks_wallet, self.f1.wallet)
        # should return "Dont have enough money for that :( please reload the money"
		# case 2: test if the stall doesn't have enough food left in stock
        self.f1.validate_order(self.c1, self.s1, "Burger", 3000)
        self.assertEqual(jacks_wallet, self.f1.wallet)
        # should return "Our stall has run out of that ___ please try a different stall" 
		# case 3: check if the cashier can order item from that stall
        self.f1.validate_order(self.c3, self.s1, "Burger", 2)
        self.assertEqual(jacks_wallet, self.f1.wallet)
        # should return "sorry we dont have that vendor stall, please try a different one"
    # Test if a customer can add money to their wallet
    def test_reload_money(self):
        jacks_wallet = self.f1.wallet
        self.f1.reload_money(50) #f1 starts out with 100, after reload_money its now 150
        new_amount = 50 + jacks_wallet
        self.assertEqual(new_amount, self.f1.wallet)
      
    
### Write main function
def main():
    # Made 2 dictionaties with at least 3 food types and cost per item (INVENTORY)
    inventory_1 = {"grilled cheese": 5, "soup and salad": 10, "lobster": 15, "nuggets": 4, "steak" : 80, "crab legs" : 45}
    inventory_2 = {"lasagna": 50, "boneless wings": 7, "stirfry": 9, "pizza": 30, "quesadilla" : 25, "brownie" : 8}

    # Made 3 different objects (customers with unique name, amount of money in wallet) (CUSTOMERS)
    customer_1 = Customer("Jax", wallet=75)
    customer_2= Customer("Squidward", wallet=100)
    customer_3 = Customer("Jasper", wallet=50)

    # Create two stall objects with unique name, inventory, and cost (STALLS)
    stall_1 = Stall("Food R Us", inventory_1, 10)
    stall_2 = Stall("Food Time", inventory_2, 15)

    # Create two cashiers with unique name and directory (CASHIERS)
    cashier_1 = Cashier("Kelly", [stall_1])
    cashier_2 = Cashier("Ketashia", [stall_2])

    #Try all cases in the validate_order function
    #Below you need to have *each customer instance* try the four cases
    # CASE 1: the cashier does not have the stall 
    customer_1.validate_order(cashier_1, stall_2, "lasagna", 1) # will return "sorry we dont have that vendor stall"
    customer_2.validate_order(cashier_1, stall_2, "stirfry", 1) # will return "sorry we dont have that vendor stall"
    customer_3.validate_order(cashier_1, stall_2, "grilled cheese", 1) # will return "sorry we dont have that vendor stall"
    print('CASE 1 ^ \n')
    # CASE 2: the casher has the stall, but not enough ordered food or the ordered food 
    customer_1.validate_order(cashier_1, stall_1, "grilled cheese", 11) # will return "our stall has run out __ please try a different stall"
    customer_2.validate_order(cashier_1, stall_1, "nuggets", 13) # will return "our stall has run out __ please try a different stall"
    customer_3.validate_order(cashier_2, stall_2, "stirfry", 20) # will return "our stall has run out __ please try a different stall"
    print("CASE 2 ^\n")
    # CASE 3: the customer does not have enough money to pay for the order: 
    customer_1.validate_order(cashier_1, stall_1, "steak", 12) # should return " Dont have enough money for that please reload more!"
    customer_2.validate_order(cashier_2, stall_2, "quesadilla", 8) # should return " Dont have enough money for that please reload more!"
    customer_3.validate_order(cashier_1, stall_1, "steak", 15) # should return " Dont have enough money for that please reload more!"
    print("CASE 3^\n")
    # # CASE 4: the customer successfully places an order
    customer_1.validate_order(cashier_1, stall_1, "grilled cheese", 1) # should return your order has been processed
    customer_2.validate_order(cashier_2, stall_2, "pizza", 2)   # should return your order has been processed
    customer_3.validate_order(cashier_1, stall_1, "crab legs", 1)   # should return your order has been processed
    print("CASE 4 ^\n")
 

if __name__ == "__main__":
	main()
	print("\n")
	unittest.main(verbosity = 2)
