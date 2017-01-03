import random
import matplotlib
import matplotlib.pylab as plt
import time

lower_busts = 31.235
higher_profit = 63.208

sampleSize = 100
startingFunds = 10000
wagerSize = 100
wagerCount = 1000

def rollDice():
    roll = random.randint(1, 100)
    
    if roll == 100:
        #print( roll, 'roll was 100, you lose. What are the odds?! Play again!')
        return False
    elif roll <= 50:
        #print(roll, 'roll was 1-50, you lose. Play again!')
        return False
    
    elif 100 > roll > 50:
        #print(roll, 'roll was 51-99, you win! *pretty lights flash* Play more!')
        return True
 
def double_bettor(funds, initial_wager, wager_count, color): 
    value = funds
    wager = initial_wager
    
    global double_busts
    global double_profit
    wX = []
    vY = []
    
    currentWager = 1
    previousWager = 'win'
    previousWagerAmount = initial_wager
    
    while currentWager <= wager_count:
        if previousWager == 'win':
            #print ('we won the last wager, great')
            if  rollDice():
                value+=wager
                #print (value)
                wX.append(currentWager)
                vY.append(value)
            else:
                value-=wager
                previousWager = 'loss'
                #print(value)
                previousWagerAmount = wager
                wX.append(currentWager)
                vY.append(value)
                if value <= 0:
                    #print('we went broke after ',currentWager, ' bets')
                    double_busts +=1
                    break
                    
        elif previousWager == 'loss':
            #print('we lost the last one, so we will double it!')
            if rollDice():
                wager = previousWagerAmount * 2
                
                if (value - wager < 0):
                    wager = value
                #print ('we won', wager)
                value+=wager
                #print (value)
                previousWager = 'win'
                wager = initial_wager
                wX.append(currentWager)
                vY.append(value)
            else:
                wager = previousWagerAmount * 2
                if (value - wager < 0):
                    wager = value                
                #print('we lost!', wager)
                value -=wager
                previousWager = 'loss'
                previousWagerAmount = wager
                wX.append(currentWager)
                vY.append(value)
                if value <= 0:
                    #print('we went broke after ',currentWager, ' bets')
                    double_busts +=1
                    break      
                #print (value)

        currentWager += 1
        
    #print(value)             
    plt.plot(wX, vY, color)
    if value > funds:
        double_profit +=1  
        
def multiple_bettor(funds, initial_wager, wager_count, random_multiple):  
    global multiple_busts
    global multiple_profit
    
    value = funds
    wager = initial_wager
    wX = []
    vY = []
    
    currentWager = 1
    previousWager = 'win' 
    previousWagerAmount = initial_wager
    
    while currentWager <= wager_count:
        if previousWager == 'win':
            if  rollDice():
                value+=wager
                wX.append(currentWager)
                vY.append(value)
            else:
                value-=wager
                previousWager = 'loss'
                previousWagerAmount = wager
                wX.append(currentWager)
                vY.append(value)
                if value <= 0:
                    multiple_busts +=1
                    break
                    
        elif previousWager == 'loss':
            if rollDice():
                wager = previousWagerAmount * random_multiple
                if (value - wager < 0):
                    wager = value
                value+=wager
                previousWager = 'win'
                wager = initial_wager
                wX.append(currentWager)
                vY.append(value)
            else:
                wager = previousWagerAmount * random_multiple
                if (value - wager < 0):
                    wager = value                
                value -=wager
                previousWager = 'loss'
                previousWagerAmount = wager
                wX.append(currentWager)
                vY.append(value)
                if value <= 0:
                    multiple_busts +=1
                    break      

        currentWager += 1
                  
    plt.plot(wX, vY)
    if value > funds:
        multiple_profit +=1
        
         
def simple_bettor(funds, initial_wager, wager_count, color):
    global simple_busts
    global simple_profit
    value = funds
    wager = initial_wager
    
    wX = []
    vY = []
    
    currentWager = 1
    
    while currentWager <= wager_count:
        if rollDice():
            value += wager
            wX.append(currentWager)
            vY.append(value)
        else:
            value -=wager
            wX.append(currentWager)
            vY.append(value)
            
        currentWager += 1
        
    if value <= 0:
        value = 0
        simple_busts +=1
        #value = 'broke'
        
    plt.plot(wX, vY,color)
    if value > funds:
        value = 0
        simple_profit+=1 


while True:
    multiple_busts = 0.0
    multiple_profit = 0.0
    multipleSampSize = 10000
    currentSample = 1
    
    random_multiple = random.uniform(1.0, 2.0)
    
    while currentSample <= multipleSampSize:
        multiple_bettor(startingFunds,wagerSize,wagerCount, random_multiple)
        currentSample+=1
        
    if (((multiple_busts/multipleSampSize)*100.00 < lower_busts) and ((multiple_busts/multipleSampSize)*100.00 > higher_profit)):
        print ('###########################')
        print ('Found a winner, the multiple was: ' ,random_multiple)
        print ('###########################')
        print ('Higher profit rate to beat: ' ,higher_profit)
        print('bust rate: ', (multiple_busts/multipleSampSize)*100.00)
        print('Profit rate: ', (multiple_profit/multipleSampSize)*100.00)
        print ('###########################')
    else:
        print ('###########################')
        print ('Found a loser, the multiple was: ' ,random_multiple)
        print ('###########################')
        print ('Higher profit rate to beat: ' ,higher_profit)
        print('bust rate: ', (multiple_busts/multipleSampSize)*100.00)
        print('Profit rate: ', (multiple_profit/multipleSampSize)*100.00)
        print ('###########################')
    

        


#Conclusion:

#even though in the simple_bettor you never go broke and you have a better chance of profiting
#its the double _bettor that has the most meaningful profit. Although it is riskier because you
# can go broke.