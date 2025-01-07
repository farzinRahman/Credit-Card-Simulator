"""

Credit Card Simulator starter code provided by Michael Guerzhoy. The following functions implemented by Farzin:
date_same_or_later(day1, month1, day2, month2)
all_three_different(c1, c2, c3)
purchase(amount, day, month, country)
amount_owed(day, month)
pay_bill(amount, day, month)

"""


def initialize():
    global cur_balance_owing_intst, cur_balance_owing_recent
    global last_update_day, last_update_month
    global last_country, last_country2
    global card_disabled
    
    cur_balance_owing_intst = 0
    cur_balance_owing_recent = 0
    
    
    last_update_day, last_update_month = -1, -1
    
    last_country = None
    last_country2 = None
    
    card_disabled = False   
    
    MONTHLY_INTEREST_RATE = 0.05

def date_same_or_later(day1, month1, day2, month2):
    ''' Return True iff the date(day1, month1) is the same as the date(day2, month2), or occurs later than (day2, month2) for all valid dates in the year 2020. '''
    
    if month1 > month2:
        return True
    
    if month1 < month2:
        return False
    
    if day1 >= day2:
        return True
    
    return False
        
    
    
def all_three_different(c1, c2, c3):
    ''' Return true iff the values of the three strings c1, c2, and c3 are all different from each other '''
    
    if c1 == None or c2 == None or c3 == None:
        return False
    
    if c1 != c2 and c2 != c3 and c3 != c1:
        return True
    
    return False
    
        
def purchase(amount, day, month, country):
    ''' Simulate a purchase of amount, on the date (day, month), in the country, assumming the amount is greater than 0 and country is a valid country name. Return the string "error" if there was a simlulation operation on a date later than (day, month) or the card is disabled/becoming disabled '''
    
    global cur_balance_owing_intst, cur_balance_owing_recent
    global last_update_day, last_update_month
    global last_country, last_country2
    global card_disabled
    
    if card_disabled:
        return "error"
    
    if all_three_different(country, last_country, last_country2):
        card_disabled = True
        return "error"
    
    if date_same_or_later(day, month, last_update_day, last_update_month) == False:
        return "error"
    
    if month == last_update_month:
        cur_balance_owing_recent += amount
        
    elif month > last_update_month:
        cur_balance_owing_intst = cur_balance_owing_intst * (1.05 ** (month - last_update_month)) + cur_balance_owing_recent * (1.05 ** (month - last_update_month - 1))
        cur_balance_owing_recent = 0
        cur_balance_owing_recent += amount
        
    
    last_country2 = last_country
    last_country = country
        
    last_update_day = day
    last_update_month = month
    
    
    
def amount_owed(day, month):
    ''' Return the amount owed as of the date (day, month). Return the string "error" if there was a simlulation operation on a date later than (day, month) '''
    
    global cur_balance_owing_intst, cur_balance_owing_recent
    global last_update_day, last_update_month
    global last_country, last_country2
    global card_disabled
    
    
    if date_same_or_later(day, month, last_update_day, last_update_month) == False:
        return "error"
    
    if month > last_update_month:
        cur_balance_owing_intst = cur_balance_owing_intst * (1.05 ** (month - last_update_month)) + cur_balance_owing_recent * (1.05 ** (month - last_update_month - 1)) 
        cur_balance_owing_recent = 0
        
    last_update_day = day
    last_update_month = month
    
    return cur_balance_owing_recent + cur_balance_owing_intst
    
    
def pay_bill(amount, day, month):
    ''' Simulate a payment of the amount owed on the date (day, month), assuming the amount is greater than 0. Return the string "error" if there was a simlulation operation on a date later than (day, month) '''
    
    global cur_balance_owing_intst, cur_balance_owing_recent
    global last_update_day, last_update_month
    global last_country, last_country2
    global card_disabled
    
        
    if date_same_or_later(day, month, last_update_day, last_update_month) == False:
        return "error"
    
    
    if month == last_update_month:
        if amount > (cur_balance_owing_intst + cur_balance_owing_recent):
            return "error"
        
        if amount == (cur_balance_owing_intst + cur_balance_owing_recent):
            cur_balance_owing_intst = 0
            cur_balance_owing_recent = 0
        
        elif amount <= cur_balance_owing_intst:
            cur_balance_owing_intst = cur_balance_owing_intst - amount
            
        elif amount > cur_balance_owing_intst:
            cur_balance_owing_recent = cur_balance_owing_recent - (amount - cur_balance_owing_intst)
            cur_balance_owing_intst = 0
        
        
    elif month > last_update_month:
        cur_balance_owing_intst = cur_balance_owing_intst * (1.05 ** (month - last_update_month)) + cur_balance_owing_recent * (1.05 ** (month - last_update_month - 1))
        cur_balance_owing_recent = 0
        
        if amount > cur_balance_owing_intst:
            return "error"
        
        if amount <= cur_balance_owing_intst:
            cur_balance_owing_intst = cur_balance_owing_intst - amount

    
    last_update_day = day
    last_update_month = month
    
        

# Initialize all global variables outside the main block.
initialize()		
    
if __name__ == '__main__':
    # Describe your testing strategy and implement it below.
    # What you see here is just the simulation from the handout, which
    # doesn't work yet.
    initialize()
    purchase(80, 8, 1, "Canada")
    print("Now owing:", amount_owed(8, 1))      # 80.0                              (Test1)
    pay_bill(50, 2, 2)
    print("Now owing:", amount_owed(2, 2))      # 30.0     (=80-50)                 (Test2)
    print("Now owing:", amount_owed(6, 3))      # 31.5     (=30*1.05)               (Test3)
    purchase(40, 6, 3, "Canada")
    print("Now owing:", amount_owed(6, 3))      # 71.5     (=31.5+40)               (Test4)
    pay_bill(30, 7, 3)
    print("Now owing:", amount_owed(7, 3))      # 41.5     (=71.5-30)               (Test5)
    print("Now owing:", amount_owed(1, 5))      # 43.65375 (=1.5*1.05*1.05+40*1.05) (Test6)
    purchase(40, 2, 5, "France")
    print("Now owing:", amount_owed(2, 5))      # 83.65375                          (Test7)
    print(purchase(50, 3, 5, "United States"))  # error    (3 diff. countries in    (Test8)
                                                #          a row)
                                                
    print("Now owing:", amount_owed(3, 5))      # 83.65375 (no change, purchase     (Test9)
                                                #           declined)
    print(purchase(150, 3, 5, "Canada"))        # error    (card disabled)          (Test10)
    print("Now owing:", amount_owed(1, 6))      # 85.8364375                        (Test11)
                                                # (43.65375*1.05+40)
                                            
                                            

    
    
    
    
    
    
    
    
    
    
    
    