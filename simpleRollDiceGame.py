import random
import matplotlib
import matplotlib.pylab as plt
import time

lower_busts = 31.235
higher_profit = 63.208

sampleSize = 1000
startingFunds = 100000
wagerSize = 10
wagerCount = 1000

def rollDice():
    #Now the odds are 50/50
    roll = random.randint(1, 100)

    if roll <= 50:
        #print(roll, 'roll was 1-50, you lose. Play again!')
        return False
    
    elif roll >= 51:
        #print(roll, 'roll was 51-99, you win! *pretty lights flash* Play more!')
        return True

def dAlembert(funds, initial_wager, wager_count):
    global Ret
    global da_busts 
    global da_profit 
    
    value = funds
    wager = initial_wager
    currentWager = 1
    previousWager = 'win'
    previousWagerAmount = initial_wager
    
    while currentWager <= wager_count:
        if previousWager == 'win':
            if wager == initial_wager:
                pass
            else:
                wager -= initial_wager
            
            #print ('current wager:', wager, 'value', value)
            if rollDice():
                previousWagerAmount = wager
                #print ('we won, current value:', value)
                value += wager
            else: 
                previousWagerAmount = wager
                value -= wager
                #print ('we lost, current value:', value)
                previousWager = 'loss'
                
                if value <= 0:
                    da_busts +=1
                    break
                
        elif previousWager == 'loss':
            wager = previousWagerAmount + initial_wager
            if (value - wager <= 0):
                wager = value
            
            #print('lost the last wager, current wager:', wager, 'value', value)
                
            if rollDice():
                previousWagerAmount = wager
                value += wager
                #print ('we won, current value:', value)
                previousWager  = 'win'
            else:
                value -= wager
                previousWagerAmount = wager
                #print ('we lost, current value:', value)
                
                if (value <= 0):
                    da_busts +=1
                    break       
        currentWager += 1
    if (value > funds):
        da_profit +=1
    
    #print('value', value)
    Ret += value
            
            
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

Ret = 0.0
da_busts = 0
da_profit = 0
da_SampSize = 10000


counter = 1
while counter <= da_SampSize:
    dAlembert(startingFunds, wagerSize, wagerCount)
    counter +=1
    
print ('Total invested ', da_SampSize*startingFunds)
print('Total Return ', Ret)
print('ROI ', Ret - (da_SampSize*startingFunds))
print('Bust Rate: ', (da_busts/da_SampSize)*100.00)
print('Profit rate: ', (da_profit/da_SampSize)*100.00)

#Conclusion:
# d'Alembert alternative works on the long run for 50/50 odds if there is a good relation between your total amount of funds
# and the size of each wager. If the wager is too big than the probability of d'Alembert making you lose money is high.