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

totalFunded = 0
totalEnding = 0

def Labouchere():
    global broke_count
    global totalFunded
    global totalEnding
    
    starting_funds = 100
    
    totalFunded += starting_funds

    goal = 10
    system = [1,1,1,1,1,1,1,1,1,1]
    #system =[1,2,2,3,2]
    profit = 0
    
    current_funds = starting_funds
    
    wagerSize = []
    plot_funds = []
    
    not_broke = True
    
    wins = 0
    loses = 0
    
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
            loses += 1
            
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
    totalEnding += current_funds
    
    s1.plot(wagerSize)
    s2.plot(plot_funds)
    
f = plt.figure()
s1 = f.add_subplot(211)
s2 = f.add_subplot(212)

sample_size = 100

for x in range(sample_size):
    Labouchere()
    
print('Broke Percentage: ', (float(broke_count)/sample_size)*100.0)
print('Total Funded: ', totalFunded)
print('Total Ending: ', totalEnding)
#plt.show()
            
#Conclusion:
# Even though you only lose 10% of the time you are risking 100 dollars to win 10 dollars back
# So the amount of times you win 10 dollars and the amounts times you lose and lose 100 dollars you would be braking even
# this means that, with 50/50 odds you would be getting, statistically, the same amount of money you just betted
# using this strategy. 
# Final conclusion, you can't beat 50/50 odds. No matter what strategy you are using. You just can't beat it.
# And another problem, hurting your possibilities, is that most casino games don't insure 50/50.
# Most of the times the house has the highest probability of winning.

# They are there to make money, not to give money away! It's an illusion of easy money.
    
    

