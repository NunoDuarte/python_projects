import random
import matplotlib
import matplotlib.pylab as plt
import time

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
 
def double_bettor(funds, initial_wager, wager_count): 
    value = funds
    wager = initial_wager
    
    wX = []
    vY = []
    
    currentWager = 1
    previousWager = 'win'
    previousWagerAmount = initial_wager
    
    while currentWager <= wager_count:
        if previousWager == 'win':
            print ('we won the last wager, great')
            if  rollDice():
                value+=wager
                print (value)
                wX.append(currentWager)
                vY.append(value)
            else:
                value-=wager
                previousWager = 'loss'
                print(value)
                previousWagerAmount = wager
                wX.append(currentWager)
                vY.append(value)
                if value < 0:
                    print('we went broke after ',currentWager, ' bets')
                    break
                    
        elif previousWager == 'loss':
            print('we lost the last one, so we will double it!')
            if rollDice():
                wager = previousWagerAmount * 2
                print ('we won', wager)
                value+=wager
                print (value)
                previousWager = 'win'
                wager = initial_wager
                wX.append(currentWager)
                vY.append(value)
            else:
                wager = previousWagerAmount * 2
                print('we lost!', wager)
                value -=wager
                if value < 0:
                    print('we went broke after ',currentWager, ' bets')
                    break      
                print (value)
                previousWager = 'loss'
                previousWagerAmount = wager
                wX.append(currentWager)
                vY.append(value)
            
        currentWager += 1
        
    print(value)             
    plt.plot(wX, vY)     
 
    
def simple_bettor(funds, initial_wager, wager_count):
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
        
    if value < 0:
        value = 'broke'
        
    plt.plot(wX, vY)

# double_bettor(10000,100,1000)
# plt.show()


x = 0
 
while x < 100:
    double_bettor(10000,100,1000)
     
    x = x + 1
     
plt.ylabel('Account Value')
plt.xlabel('Wager Count')
plt.show()

#The conclusion:
#After some time, the house always wins. 
            