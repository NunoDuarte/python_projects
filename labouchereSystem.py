import random
import time
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import style

#How does Labouchere work?
#You have some startingFunds and you separate in different amount like so: [1 2 2 3 2] (like an array of values that sun up to your
#starting total funds (here is 10)
#And you start betting the total amount of your outside array, so 1+2=3
# If you win, you continue betting but now you've scratched those amounts and you move on to the inside amounts of your array
# so now it would be 2+3=5
# If you lose, you add the amount you've lost (so 3) to the end of your array and your next bet will be the sum of your new outside 
# array (your new array [1 2 2 3 2 3]), so 1+3=4. And you do this until your are finished with your array
# The Labouchere system states that when you are done and you have a empty array then you have won the initial total amount, 
# in our case, 10!

style.use('ggplot')

broke_count = 0

def Labouchere():
    global broke_count
    
    starting_funds = 100
    goal = 10
    system = [1,1,1,1,1,1,1,1,1,1]
    #system =[1,2,2,3,2]
    profit = 0
    
    current_funds = starting_funds
    
    wagerSize = []
    plot_funds = []
    
    not_broke = True
    
    wins = 1
    loses = 1
    
    while profit < goal and not_broke:
        
        if len(system) > 1:
            size = system[0] + system[-1]
            wagerSize.append(size)  
            plot_funds.append(current_funds)
            
        else:
            size = system[0]
            wagerSize.append(size)
            plot_funds.append(current_funds)
            
        if current_funds <= 0:
            not_broke = False
            broke_count += 1
            
        elif current_funds - size <= 0:
            size = current_funds
            not_broke =  False
            broke_count += 1
            
        dice = random.randrange(1,101) #randrange hits every number from 1 to 101 but it does not reach 101, so it's from 1 to 100
        
        if dice < 51:
            loses += 1
            system.append(size)
            current_funds -= size
            profit =  current_funds - starting_funds 
            
        else:
            wins += 1
            current_funds += size
            profit =  current_funds - starting_funds
            
            if profit != goal:
                try:
                    del system[0]
                    del system[-1]
                except:
                    pass
            
    wagerSize.append(size)
    plot_funds.append(current_funds)
    
    s1.plot(wagerSize)
    s2.plot(plot_funds)
    
f = plt.figure()
s1 = f.add_subplot(211)
s2 = f.add_subplot(212)

sample_size = 100

for x in range(sample_size):
    Labouchere()
    
print('Broke Percentage: ', (float(broke_count)/sample_size)*100.0)
plt.show()
            
    
    

