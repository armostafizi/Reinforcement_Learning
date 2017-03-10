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
    reward = r[next_state]
    return next_state, reward

        
def e_greedy_act(q,s,eps):
    #eps = 0.1
    index = q[s].index(max(q[s]))
    if random.random() < eps :
        return index
    else:
        keep = q[s][:index] + q[s][(index + 1):]
        rnd = random.choice(keep)
        return q[s].index(rnd)

def e_greedy_act_mb(p,s,eps):

    global m
    
    if random.random() < eps:
        return p[s]
    else:
        a=range(m)
        a.remove(p[s])
        return random.choice(a)
    

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

def opt_bellman_backup(v0,cnt):
    global t
    global beta
    
    v1 = []
    for j in range(n):
        sums = []
        for k in range(m):
            if cnt[j][k] < 3:
                s = 1000
            else:
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


def optimal_policy(to,ro):

    global n
    global m

    eps = 0.0000001
    v = ro
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
            s = sum(a*b for a,b in zip(v,to[k][j]))
            sums.append(s)
        indx = sums.index(max(sums))
        policy.append(indx)
    return policy

def optimistic_opt_policy(to,ro,cnt):

    global n
    global m

    eps = 0.0000001
    v = ro
    while True:
        w = v
        v = opt_bellman_backup(v,cnt)
        dif = []
        for i,j in zip(w,v):
            dif.append(abs(i-j))
        if max(dif) < eps :
            break

    policy = []
    for j in range(n):
        sums = []
        for k in range(m):
            s = sum(a*b for a,b in zip(v,to[k][j]))
            sums.append(s)
        indx = sums.index(max(sums))
        policy.append(indx)
    return policy


def fix_lt(lt):
    lt_temp = []
    for i in lt:
        oo = []
        for j in i:
            sm = sum(j)
            if sm !=0:
                o = [1.*x/sm for x in j]
                oo.append(o)
            else:
                oo.append(j)
        lt_temp.append(oo)

    return lt_temp


def fix_lr(lr,cnts):
    lr_temp = []
    for i,j in zip(lr, cnts):
        if j != 0:
            lr_temp.append(1.*i/j)
        else:
            lr_temp.append(0)
    return lr_temp


def learn():

    global n
    global m
    global counts
    global beta
    global alpha
    global rew_list
    global vals
    global lt_temp
    global lr_temp

    vals = []
    
    lt = []
    for i in range(m):
            lt.append([[0]*n for j in range(n)])

    lr = []
    lr = [0]*n

    lr_count = [0]*n
    
    q = []
    counts = []
    q = [[0] * 3 for i in range(n)]
    counts = [[0] * 3 for i in range(n)]
    pol = optimal_policy(lt,lr)

    z = 100
    x = 100
    eps = 1
    for k in range(z):
        #print '#### ', k, ' ###'
        for i in range(x):
            #print i
            init = initial_state()
            for j in range(20):
                #act = e_greedy_act(q,init,eps)
                #act = drive_more(counts,init)
                act = e_greedy_act_mb(pol,init,eps)
                
                next_st,rew = do(init,act)
                counts[init][act] += 1
                lr_count[next_st] += 1
                lt[act][init][next_st] += 1
                lr[next_st] += rew
                init = next_st

            eps -= (1.0/(z*x))

            lt_temp = fix_lt(lt)
            lr_temp = fix_lr(lr,lr_count)
            
            pol = optimistic_opt_policy(lt_temp, lr_temp, counts)
    
        pol = optimal_policy(lt_temp,lr_temp)
        val = policy_val(pol)
        vals.append(val)
        print val
        
    #plt.plot(vals)
    #plt.show()        
    return vals,lt_temp, lr_temp
    

def how_different(p):
    global opt_p
    not_the_same = 0 
    for i,j in zip(opt_p,p):
        if i != j:
            not_the_same += 1
    print not_the_same
        

#MAIN:

mdp_input()

beta = 0.99

opt_p = optimal_policy(t,r)
print 'Optimal Policy Value: ',
print policy_val(opt_p)

print

vals, learned_t, learned_r = learn()
opt_p_new = optimal_policy(learned_t,learned_r)

#how_different(opt_p_new)

#for i,j in zip(opt_p,opt_p_new):
#    print i,j
