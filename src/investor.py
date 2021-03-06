import time
import math

class Post:

    """
    This is a Post class that stores information
    on one submission from Investment class instance

    Attributes:
    1. ID - submission id

    2. upvotes - the initial number of upvotes

    """
    
    def __init__(self, ID, upvotes):
        self.ID = ID
        self.upvotes = upvotes

    # GET METHODS
        
    def get_ID(self):
        return self.ID

    def get_upvotes(self):
        return int(float(self.upvotes))

    # SET METHODS

    def set_ID(self, i):
        self.ID = i

    def set_upvotes(self, ups):
        self.upvotes = ups
    
class Investment:

    """
    This class holds data for only 1 investment.
    The following attributes are:
    
    1. post - is the submission's id
    
    2. upvotes - is the amount of upvotes during 
    the time of object allocation

    3. name - is the name (user id) of the investor
    who owns the following investment

    4. amount = is the amount of memecoint the 
    Investor class instance invested in the post

    """
    
    def __init__(self, postID, commentID, upvotes, name, amount):
        self.post = Post(postID, upvotes)
        self.comment = commentID
        self.name = name
        self.amount = amount
        self.time = time.time()
        
    def check(self):
        change = time.time() - self.get_time()

        # 6 hours of waiting
        if (change > 6 * 60 * 60):
            return True
        return False

    # GET METHODS
    
    def get_ID(self):
        return self.post.get_ID()

    def get_comment(self):
        return self.comment
    
    def get_upvotes(self):
        return int(float(self.post.get_upvotes()))
    
    def get_name(self):
        return self.name
    
    def get_amount(self):
        return int(float(self.amount))
    
    def get_time(self):
        return int(float(self.time))

    # SET METHODS

    def set_ID(self, i):
        self.post.set_ID(i)

    def set_comment(self, commentID):
        self.comment = commentID
        
    def set_upvotes(self, ups):
        self.post.set_upvotes(ups)

    def set_name(self, nam):
        self.name = nam
        
    def set_amount(self, amoun):
        self.amount = amoun

    def set_time(self, tim):
        self.time = tim
    
class Investor:

    """
    This is a class Investor where 1 instance stores data
    on one individual meme investor.
    The following attributes are defined when Investor
    class instance is created:

    1. name - this is the user's unique subreddit name
    or in common, the reddit user id. u/

    2. balance - the amount of memecoins the user 
    currently has in his bank.

    3. completed - the number of completed investments.
    Doesn't matter, successful or unsuccessful.

    4. invests - is the array of Investment class
    instances that holds every data on every investment
    that the user made.

    For each attribute there is an appropriate GET method.
    """
    
    def __init__(self, name, balance):
        self.name = name
        self.balance = balance
        self.active = 0
        self.completed = 0
        self.invests = []

    def enough(self, amount):
        if (self.get_balance() < amount):
            return False
        return True
        
    def invest(self, postID, upvotes, commentID, amount):
        self.set_balance(self.get_balance() - amount)
        inv = Investment(postID, commentID, upvotes, self.name, amount)
        self.invests.append(inv)
        self.set_active(self.get_active() + 1)
        return inv
        
    def calculate(self, investment, upvotes):
        du = upvotes - investment.post.get_upvotes()
        win = 0
        
        """
        Investment return multiplier was previously determined with a block of if statements.
        Performed a linear fit to a log-log plot of mutliplier vs upvotes based on the original values for the if block.
        Used the gradient/intercept to generate a power function that approximates (and extends) the original mutliplier
        calculation to all upvote values.
        
        Functional form: y = (10^c)x^m ;
          y = multiplier,
          x = du (change in upvotes),
          m = gradient of linear fit to log-log plot (= 0.2527),
          c = intercept of linear fit to log-log plot (= -0.7603).
        """
        #Allow custom upper du limit to cap maximum investment profit multiplier (set as desired)
        success_cap = 100000
        
        #Safeguard: if du is -ve function cannot be evaluated and mult remains zero.
        mult = 0
        if (du >= 0):
            mult = 0.17366 * math.pow(du, 0.2527)
        
        #Failure is defined as a profit multiplier less than 1.
        if (mult < 1):
            return self.profit(investment, False, mult)
        
        #Return multiplier value for du upper limit if du is at or above the limit
        elif (du >= success_cap):
            capped_mult = 0.17366 * math.pow(success_cap, 0.2527)
            return self.profit(investment, True, capped_mult)
        
        else:
            return self.profit(investment, True, mult)
        
        #OLD METHOD:
        '''           
        if (du >= 1000 and du < 1500):
            return self.profit(investment, True, 1)
        
        if (du >= 1500 and du < 2500):
            return self.profit(investment, True, 1.10)
            
        if (du >= 2500 and du < 5000):
            return self.profit(investment, True, 1.25)
            
        if (du >= 5000 and du < 10000):
            return self.profit(investment, True, 1.50)
            
        if (du >= 10000 and du < 15000):
            return self.profit(investment, True, 1.75)
            
        if (du >= 15000):
            return self.profit(investment, True, 2.00)
        '''
        
    def profit(self, investment, success, multiplier):
        self.set_completed(self.get_completed() + 1)
        self.set_active(self.get_active() - 1)
        investment.done = 1
        
        if (not success):
            return 0

        orig = self.get_balance()
        self.set_balance(self.get_balance() + investment.amount)
        self.set_balance(self.get_balance() * multiplier)
        change = self.get_balance() - orig
        return change

    # GET METHODS
        
    def get_name(self):
        return self.name
    
    def get_balance(self):
        return int(float(self.balance))

    def get_active(self):
        return int(float(self.active))

    def get_completed(self):
        return int(float(self.completed))

    def get_invests(self):
        return self.invests

    # SET METHODS
    
    def set_balance(self, balanc):
        self.balance = balanc

    def set_name(self, nam):
        self.name = nam

    def set_active(self, activ):
        self.active = activ    
    
    def set_completed(self, complete):
        self.completed = complete

    def add_investment(self, investment):
        self.invests.append(investment)
