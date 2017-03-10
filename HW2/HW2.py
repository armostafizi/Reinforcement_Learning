from numpy import matrix
import numpy as np
from Tkinter import *
import tkFileDialog

def bellman_backup(v0):
    global t
    global b
    v1 = []
    for j in range(n):
        sums = []
        for k in range(m):
            s = sum(a*b for a,b in zip(v0,t[k][j]))
            sums.append(s)
        mx = max(sums)
        v1.append(r[j] + ( b * mx))
    return v1

print "Text File:"
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

b = input ("Beta (0-1): ")
print

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

#Vg
opt_t = []

for i in range(n):
    t_row = []
    for j in range(n):
        t_row.append(t[policy[i]-1][i][j])
    opt_t.append(t_row)

r_mat = []
for i in r:
    r_mat.append([i])

vg = ((np.subtract((np.identity(len(opt_t))), matrix(opt_t)*b)).I) * r_mat
vg = vg.tolist()

    
print("Greedy Policy:")
for i in policy:
    print i,
print
print

print("Greedy Value Function (Vg):")
for i in vg:
    print '%.4f' % i[0],
print
print
#print "Value Function: Vk"
#print v
