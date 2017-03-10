from numpy import matrix
import numpy as np
from Tkinter import *
import tkFileDialog
import random


def mdp_input():
    
    global n
    global m
    global t
    global r
    global file_path
    
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


def get_action_1(p,s):
    if s%2 == 1:
        return 2
    else:
        if random.random() < p :
            return 1
        else:
            return 0

def get_action_2(p,s):
    if s%2 == 1:
        return 2
    elif s%4 == 2 or s%4 == 3:
        return 0
    else:    
        if random.random() < p :
            return 1
        else:
            return 0


def get_action_3(s):
    global t
    if s%2 == 1:
        return 2
    elif s%4 == 2 or s%4 == 3:
        return 0
    elif s == 80:
        return 2
    elif s == 81:
        return 1
    else:    
        if random.random() < t[0][(s - s%4)][((((s - s%4)/4) + 1) * 4)%80] :
            return 0
        else:
            return 1

def get_action_4(s):
    if s%2 == 1:
        return 2
    elif s%4 == 2 or s%4 == 3:
        return 0
    else:    
        return 1



def val_policy1():
    print "Value of Policy 1: "
    print 'MDP: ' + file_path
    p = input('P: ')
    sm = 0
    for tr in range(1000):
        rewards = 0
        if random.random() < t[0][n-4][0]:
            init = 0
        else:
            init = 2
        for i in range(50):
            act = get_action_1(p,init)
            init, rew = do(init,act)
            rewards += rew
        sm += rewards
    
    print sm / 1000



def val_policy2():
    print "Value of Policy 2: "
    print 'MDP: ' + file_path
    p = input('P: ')
    sm = 0
    for tr in range(1000):
        rewards = 0
        if random.random() < t[0][n-4][0]:
            init = 0
        else:
            init = 2
        for i in range(50):
            act = get_action_2(p,init)
            init, rew = do(init,act)
            rewards += rew
        sm += rewards
    
    print sm / 1000



def val_policy3():
    print "Value of Policy 3: "
    print 'MDP: ' + file_path
    sm = 0
    for tr in range(1000):
        rewards = 0
        if random.random() < t[0][n-4][0]:
            init = 0
        else:
            init = 2
        for i in range(50):
            act = get_action_3(init)
            init, rew = do(init,act)
            rewards += rew
        sm += rewards
    
    print sm / 1000


def val_policy4():
    print "Value of Policy 4: "
    print 'MDP: ' + file_path
    sm = 0
    for tr in range(1000):
        rewards = 0
        if random.random() < t[0][n-4][0]:
            init = 0
        else:
            init = 2
        for i in range(50):
            act = get_action_4(init)
            init, rew = do(init,act)
            rewards += rew
        sm += rewards
    
    print sm / 1000


#MAIN

mdp_input()

val_policy1()
raw_input()
val_policy2()
raw_input()
val_policy3()
raw_input()
val_policy4()
