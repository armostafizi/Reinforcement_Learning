from numpy import matrix
import numpy as np
from Tkinter import *
import tkFileDialog
import random
#from matplotlib import pyplot as plt

def mdp_input():
    
    global m
    global n
    global r
    global t
    
    print "MDP Text File:"
    fileOpen = Tk()
    fileOpen.withdraw()

    file_path= tkFileDialog.askopenfilename(
        title="Open file", filetypes=[("txt file",".txt"),("All files",".*")])

    fob = open(file_path, 'r')
    n,m = fob.readline().rstrip('\n').split()

    n = int(n)
    m= int (m)

    fob.readline()

    t=[]
    for i in range(m):
        a=[]
        for j in range(n):
            a.append(map(float, fob.readline().rstrip('\n').split()))
        t.append(a)
        fob.readline()

    r = map(float, fob.readline().rstrip('\n').split())
    fob.close()



def do(s,a):
    global r
    global t
    next_state = np.where(np.random.multinomial(1,t[a][s]))[0][0]
    #print s+1,a+1,next_state+1
    reward = r[next_state]
    return next_state, reward

        
def e_greedy_act(q,s):
    eps = 0.1
    index = q[s].index(max(q[s]))
    if random.random() < eps :
        return index
    else:
        keep = q[s][:index] + q[s][(index + 1):]
        rnd = random.choice(keep)
        return q[s].index(rnd)

def min_count_pull(counts,s):
    return counts[s].index(min(counts[s]))

def drive_more(counts,s):
    rnd = random.random()
    if rnd < 0.7:
        return 0
    else:
        return min_count_pull(counts,s)

def initial_state():
    global t
    if random.random() < t[0][n-4][0]:
        return 0
    else:
        return 2


def bellman_backup(v0):
    global t
    global beta
    
    v1 = []
    for j in range(n):
        sums = []
        for k in range(m):
            s = sum(a*b for a,b in zip(v0,t[k][j]))
            sums.append(s)
        mx = max(sums)
        v1.append(r[j] + ( beta * mx))
    return v1

def policy_val(policy):
    sm = 0
    for tr in range(10000):
        rewards = 0
        init = initial_state()
        for i in range(50):
            act = policy[init]
            init, rew = do(init,act)
            rewards += rew
        sm += rewards
        
    return sm / 10000


def optimal_policy():
    eps = 0.0000001
    v = r
    while True:
        w = v
        v = bellman_backup(v)
        dif = []
        for i,j in zip(w,v):
            dif.append(abs(i-j))
        if max(dif) < eps :
            break

    policy = []
    for j in range(n):
        sums = []
        for k in range(m):
            s = sum(a*b for a,b in zip(v,t[k][j]))
            sums.append(s)
        indx = sums.index(max(sums))
        policy.append(indx + 1)
    return policy


def learn():

    global n
    global counts
    global beta
    global alpha
    global rew_list
    
    rew_list = []

    q = []
    counts = []
    q = [[0] * 3 for i in range(n)]
    counts = [[0] * 3 for i in range(n)]
    for k in range(100):
        for i in range(1000):
            init = initial_state()
            for j in range(50):
                #act = e_greedy_act(q,init)
                #act = min_count_pull(counts,init)
                act = drive_more(counts,init)
                next_st,rew = do(init,act)
                counts[init][act] += 1
                q[init][act] = ( q[init][act] + alpha * ( rew + beta * (max(q[next_st])) - q[init][act] ) )
                init = next_st

        policy = [(i.index(max(i))) for i in q]
        val = policy_val(policy)
        rew_list.append(val)
        print val
    #plt.plot(rew_list)
    #plt.show()
    return [(i.index(max(i)) + 1) for i in q]

def how_different(p):
    global opt_p
    not_the_same = 0 
    for i,j in zip(opt_p,p):
        if i != j:
            not_the_same += 1
    print not_the_same
        

#MAIN:

mdp_input()

alpha = 0.1
beta = 0.99

opt_p = optimal_policy()
#print 'Optimal Policy: '
#print opt_p

print

learned_p = learn()
print 'Learned Policy: '
print learned_p

#how_different(learned_p)
