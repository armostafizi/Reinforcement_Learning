from Tkinter import *
import tkFileDialog
import random
import math
import numpy as np

def max_func(l):
    mx = 0
    for i in l:
        if i - mx > 0.001:
            mx = i
    return mx

def read_bandit():
    print "Text File:"
    fileOpen = Tk()
    fileOpen.withdraw()

    file_path= tkFileDialog.askopenfilename(
        title="Open file", filetypes=[("txt file",".txt"),("All files",".*")])

    fob = open(file_path, 'r')
    m = int(fob.readline())

    fob.readline()

    arms = []
    for i in range(m):
        r,p = fob.readline().rstrip('\n').split()
        r = float(r)
        p = float(p)
        arms.append((r,p))

    return arms

def numarms(arms):
    return len(arms)

def pull(arms, i):
    if random.random() < arms[i][1] :
        return arms[i][0] 
    else:
        return 0
    
def uniform(arms):
    avgs = []
    counts = []
    cregs = [0]
    sregs = []
    creg = 0
    for i in range(numarms(arms)):
        avgs.append(0)
        counts.append(0)
        
    n = input('N? ')
    #n = 1000
    w = n / numarms(arms)
    for i in range(w+1):
        for j in range(numarms(arms)):
            print j + 1,
            counts[j] += 1
            avgs[j] = (pull(arms,j) + ((counts[j] - 1) * (avgs[j]))) / (counts[j])
            print avgs.index(max_func(avgs)) + 1,

            #Cumulative Regret
            creg += (1 - avgs[j])
            cregs.append(creg)
            print creg,
            
            
            #Simple Regret:
            sregs.append (1 - max_func(avgs))
            print (1 - max_func(avgs))
            if sum(counts) == n:
                break
        if sum(counts) == n:
            break
    print counts
    return sregs, cregs
        
def ucb_arm(arms, n, avgs, counts):
    a = []
    for i in range(numarms(arms)):
        a.append( avgs[i] + math.sqrt((2 * np.log(n+1)) / (counts[i] + 0.0000001 )) )
    return a.index(max(a))
        

def ucb(arms):
    avgs = []
    counts = []
    creg = 0
    cregs = [0]
    sregs = []
    for i in range(numarms(arms)):
        avgs.append(0)
        counts.append(0)
        
    n = input('N? ')
    #n = 1000
    for i in range(n):
        an = ucb_arm(arms, i, avgs, counts)
        print an + 1,
        counts[an] += 1
        avgs[an] = (pull(arms, an) + ((counts[an] - 1) * (avgs[an]))) / (counts[an])
        print avgs.index(max_func(avgs)) + 1,

        #Cumulative Regret
        creg += (1 - avgs[an])
        cregs.append(creg)
        print creg,
            
            
        #Simple Regret:
        sregs.append ( 1 - max_func(avgs))
        print 1 - max_func(avgs)
         
    print counts
    return sregs, cregs

def eps_arm(avgs, e):
    index = avgs.index(max_func(avgs))
    if random.random() < e :
        return index
    else:
        keep = avgs[:index] + avgs[(index+1):]
        rnd = random.choice(keep)
        return avgs.index(rnd)
    

def eps_greedy(arms):
    avgs = []
    counts = []
    creg = 0
    cregs = [0]
    sregs = []
    for i in range(numarms(arms)):
        avgs.append(0)
        counts.append(0)
        
    n = input('N? ')
    e = input('Epsilon? ')
    #n= 1000
    #e= 0.5
    for i in range(n):
        an = eps_arm(avgs, e)
        print an + 1,
        counts[an] += 1
        avgs[an] = (pull(arms, an) + ((counts[an] - 1) * (avgs[an]))) / (counts[an])
        print avgs.index(max_func(avgs)) + 1,

        #Cumulative Regret
        creg += (1 - avgs[an])
        cregs.append(creg)
        print creg,
            
            
        #Simple Regret:
        sregs.append ( 1 - max_func(avgs))
        print 1 - max_func(avgs)       
    print counts
    return sregs, cregs


def cr_curve_uniform():
    cregs = [0]
    for i in range (1000):
        cregs.append(0)
    for i in range (100):    
        creg_u = uniform(arms)
        cregs = [x + y for x, y in zip(cregs, creg_u)]
    mean = [int(x / 100) for x in cregs]
    for i in mean:
        print i

def cr_curve_ucb():
    cregs = [0]
    for i in range (1000):
        cregs.append(0)
    for i in range (100):    
        creg_u = ucb(arms)
        cregs = [x + y for x, y in zip(cregs, creg_u)]
    mean = [int(x / 100) for x in cregs]
    for i in mean:
        print i

def cr_curve_eps():
    cregs = [0]
    for i in range (5000):
        cregs.append(0)
    for i in range (100):    
        creg_e = eps_greedy(arms)
        cregs = [x + y for x, y in zip(cregs, creg_e)]
    mean = [int(x / 100) for x in cregs]
    for i in mean:
        print i
    

def sr_curve_uniform():
    sregs = []
    for i in range (1000):
        sregs.append(0)
    for i in range (100):    
        sreg_u = uniform(arms)
        sregs = [x + y for x, y in zip(sregs, sreg_u)]
    mean = [(x / 100) for x in sregs]
    for i in mean:
        print '%.2f' % i

def sr_curve_ucb():
    sregs = []
    for i in range (1000):
        sregs.append(0)
    for i in range (100):    
        sreg_u = ucb(arms)
        sregs = [x + y for x, y in zip(sregs, sreg_u)]
    mean = [(x / 100) for x in sregs]
    for i in mean:
        print '%.2f' %i

def sr_curve_eps():
    sregs = []
    for i in range (5000):
        sregs.append(0)
    for i in range (100):    
        sreg_e = eps_greedy(arms)
        sregs = [x + y for x, y in zip(sregs, sreg_e)]
    mean = [(x / 100) for x in sregs]
    for i in mean:
        print '%.2f' %i

def algorithm(arms):
    inp = raw_input('UNI = uniform - UCB for UCB - EPS for E-Greedy? ')
    if inp == 'UNI':
        uniform(arms)
    if inp == 'UCB':
        ucb(arms)
    if inp == 'EPS':
        eps_greedy(arms)
        

#MAIN
    
arms = read_bandit()

algorithm(arms)

#cr_curve_uniform()
#cr_curve_ucb()
#cr_curve_eps()

#sr_curve_uniform()
#sr_curve_ucb()
#sr_curve_eps()


