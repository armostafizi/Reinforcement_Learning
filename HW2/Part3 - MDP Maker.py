import sys

n= input('N (>3): ')
c_dr = input('COST of Driving (+): ')
c_ac = input('COST of Accident (+): ')
c_hc = input('FINE for ADA Spot (+): ')
p_hc = input('Probability of ADA spot NOT being occupied (0-1): ')
max_rew = input('Reward for the closest spots (NOT THE ADA) (+): ')
min_rew = input('Reward for the farthest spots (+): ')
min_prob = input('Probability of the closest sport NOT being occupied (0-1): ')
max_prob = input('Probability of the farthest spot NOT being occupied (0-1): ')

filename = raw_input('Output File Name: ')
filename = filename + '.txt'
f = open (filename, 'w')

orig_stdout = sys.stdout
f = file(filename, 'w')
sys.stdout = f

#Number of States and Actions
print 8*n + 1, 3
print

dif_prob = (max_prob - min_prob)/(n-2)
prob = max_prob - dif_prob

#DRIVE:
for i in range(n-2):
    for j in range (8*n):
        if 4*(i+1) == j :
            print prob,
        elif 4*(i+1) + 2 == j:
            print 1-prob,
        else:
            print 0,
    print 0

    for j in range (8*n):
            print 0,
    print 0

    for j in range (8*n):
        if 4*(i+1) == j :
            print prob,
        elif 4*(i+1) + 2 == j:
            print 1-prob,
        else:
            print 0,
    print 0

    for j in range (8*n):
            print 0,
    print 0

    prob -= dif_prob
    


for j in range (8*n):
    if 4*(n-1) == j :
        print p_hc,
    elif 4*(n-1)+2 == j:
        print 1-p_hc,
    else:
        print 0,
print 0

for j in range (8*n):
        print 0,
print 0

for j in range (8*n):
    if 4*(n-1) == j :
        print p_hc,
    elif 4*(n-1)+2 == j:
        print 1-p_hc,
    else:
        print 0,
print 0

for j in range (8*n):
        print 0,
print 0


for j in range (8*n):
    if 4*(n) == j :
        print p_hc,
    elif 4*(n)+2 == j:
        print 1-p_hc,
    else:
        print 0,
print 0

for j in range (8*n):
        print 0,
print 0

for j in range (8*n):
    if 4*(n) == j :
        print p_hc,
    elif 4*(n)+2 == j:
        print 1-p_hc,
    else:
        print 0,
print 0

for j in range (8*n):
        print 0,
print 0

prob += dif_prob

for i in range(n,2*n-1):
    for j in range (8*n):
        if 4*(i+1) == j :
            print prob,
        elif 4*(i+1) + 2 == j:
            print 1-prob,
        else:
            print 0,
    print 0

    for j in range (8*n):
            print 0,
    print 0

    for j in range (8*n):
        if 4*(i+1) == j :
            print prob,
        elif 4*(i+1) + 2 == j:
            print 1-prob,
        else:
            print 0,
    print 0

    for j in range (8*n):
            print 0,
    print 0

    prob += dif_prob

prob -= dif_prob

for j in range (8*n):
    if 0 == j :
        print prob,
    elif 2 == j:
        print 1-prob,
    else:
        print 0,
print 0

for j in range (8*n):
        print 0,
print 0

for j in range (8*n):
    if 0 == j :
        print prob,
    elif 2 == j:
        print 1-prob,
    else:
        print 0,
print 0

for j in range (8*n):
        print 0,
print 0

for i in range(8*n):
    print 0,
print 0


print

#PARK:


for i in range(8*n):
    if i%2 == 0 :
        for j in range(8*n):
            if j == i + 1:
                print 1,
            else:
                print 0,
        print 0
    else:
        for j in range(8*n):
            print 0,
        print 0

for i in range(8*n):
    print 0,

print 0
print

#EXIT:

for i in range(8*n):
    if i%2 == 1 :
        for j in range(8*n):
            print 0,
        print 1
    else:
        for j in range(8*n):
            if j == i:
                print 1,
            else:
                print 0,
        print 0

for i in range(8*n):
    print 0,
print 1
    
print

#Rewards

dif_rew = (max_rew - min_rew)/(n-2)

for i in range(n-1):
    print -c_dr,
    print min_rew,
    print -c_dr,
    print -c_ac,
    min_rew += dif_rew

print -c_dr,
print -c_hc,
print -c_dr,
print -c_ac,

print -c_dr,
print -c_hc,
print -c_dr,
print -c_ac,


for i in range(n-1):
    print -c_dr,
    print max_rew,
    print -c_dr,
    print -c_ac,
    max_rew -= dif_rew

print 0.001,

sys.stdout = orig_stdout
f.close()

print ('MDP input generated: ' + filename)
