from Tkinter import *
import tkFileDialog

#def bellman_backup():
print "Text File:"

fileOpen = Tk()
fileOpen.withdraw()

file_path = tkFileDialog.askopenfilename(
    title="Open file", filetypes=[("txt file",".txt"),("All files",".*")])

fob = open(file_path, 'r')
n,m = fob.readline().rstrip('\n').split()

n = int(n)
m= int (m)

fob.readline()

T=[]
for i in range(m):
    a=[]
    for j in range(n):
      a.append(map(float, fob.readline().rstrip('\n').split()))
    T.append(a)
    fob.readline()

r = map(float, fob.readline().rstrip('\n').split())
fob.close()

h = input ("H: ")
print

v = [r]
policy = []
for i in range(1, h+1):
    vcell = []
    policycell = []
    for j in range(n):
        sums = []
        for k in range(m):
            s = sum(a*b for a,b in zip(v[i-1],T[k][j]))
            sums.append(s)
        indx = sums.index(max(sums))
        mx = max(sums)
        vcell.append(r[j] + mx)
        policycell.append(indx)
    v.append(vcell)
    policy.append(policycell)

print("Policy:")
for i in range(n):
    for j in range(h):
        print ((policy[j][i])+1),
    print

print

print "Value Function:"
for i in range(n):
    for j in range(h+1):
        print '%.2f' % v[j][i],
    print
