import time
import sys
import numpy as np
import resource
import Queue
import copy
from sets import Set

##global variables
n = 3
goalstate = []
checkedstates = Set()
nodesExp = 0
maxdepth = 0
memreq = 0
maxfringe = 0
solvedida = False
actualdict = []

##State class holds the current state and its parent state also which direction caused to get to that state
class State:
    def __init__(self,l,p,direc,depth):
        self.nums = l
        self.parent = p
        self.direction = direc
        self.depth = depth
        self.hfn = depth + self.calculateManhattan()
    def checkgoal(self):
        if self.nums == goalstate:
            return True
        return False
    def calculateManhattan(self):
        #calculations
        hfn = 0
        for i in range(1,9):
            [a,b] = self.getindex(i)
            [c,d] = self.actualindex(i)
            hfn = hfn+(abs(c-a)+abs(d-b))
        return hfn
    def getindex(self,ind):
        l = self.nums
        for row in l:
            for data in row:
                if data == ind:
                    i = l.index(row)
                    j = l[i].index(data)
                    return [i,j]
    def actualindex(self,i):
        return actualdict[i]
    def getblankindex(self):
        l = self.nums
        for row in l:
            for data in row:
                if data == 0:
                    i = l.index(row)
                    j = l[i].index(data)
                    return [i,j]
class Stack:
     def __init__(self):
         self.items = []

     def isEmpty(self):
         return self.items == []

     def push(self, item):
         self.items.append(item)

     def pop(self):
         return self.items.pop()
##Helper methods
def print_board(li):
    for row in li:
        for r in row:
            print r,'\t',
        print '\n'
def solutionfound(current):
    global nodesExp
    solution = [current.nums]
    directions = [current.direction]
    while current.parent != None:
        current = current.parent
        solution.append(current.nums)
        directions.append(current.direction)
    cost = len(solution)
    return [solution,directions,cost,nodesExp]
def getdirs(i,j):
    checkdirections=['UP','DOWN','LEFT','RIGHT']
    if i==0:
        checkdirections.remove('UP')
    if j==0:
        checkdirections.remove('LEFT')
    if i==n-1:
        checkdirections.remove('DOWN')
    if j==n-1:
        checkdirections.remove('RIGHT')
    return checkdirections
def expandnode(current):
    global nodesExp,maxdepth
    nodesExp = nodesExp+1
##    print current.nums,current.direction,nodesExp
    if current.depth>maxdepth:
        maxdepth = current.depth
    [i,j] = current.getblankindex()
    checkdirections = getdirs(i,j)
    children = []
    for c in checkdirections:
        temp = [row[:] for row in current.nums]
        if c == 'LEFT':
            temp[i][j] = temp[i][j-1]
            temp[i][j-1] = 0
            child = State(temp,current,c,current.depth+1)
            children.append(child)
        elif c == 'RIGHT':
            temp[i][j] = temp[i][j+1]
            temp[i][j+1] = 0
            child = State(temp,current,c,current.depth+1)
            children.append(child)
        elif c == 'UP':
            temp[i][j] = temp[i-1][j]
            temp[i-1][j] = 0
            child = State(temp,current,c,current.depth+1)
            children.append(child)
        elif c == 'DOWN':
            temp[i][j] = temp[i+1][j]
            temp[i+1][j] = 0
            child = State(temp,current,c,current.depth+1)
            children.append(child)
    return children
    
##BFS

def solveBFS(q):
    global checkedstates,maxfringe,maxdepth
    while q.empty() != True:
        current = q.get()
        if current.checkgoal():
            if current.depth>maxdepth:
                maxdepth = current.depth
            return solutionfound(current)
        else:
            children = []
            children.extend(expandnode(current))
            for c in children:
                stringc = str(c.nums)
##                print stringc
                if stringc in checkedstates:
                    continue
                else:
                    q.put(c)
                    checkedstates.add(stringc)
            if q.qsize()>maxfringe:
                maxfringe = q.qsize()
    print 'Cannot be solved'


##DFS

def solveDFS(st):
    global checkedstates,maxfringe,maxdepth
    while st.isEmpty() != True:
        current = st.pop()
        if current.checkgoal():
            if current.depth>maxdepth:
                maxdepth = current.depth
            return solutionfound(current)
        else:
            children = []
            children.extend(expandnode(current))

            for c in reversed(children):
                stringc = str(c.nums)
                if stringc in checkedstates:
                    continue
                else:
                    st.push(c)
                    checkedstates.add(stringc)
            if len(st.items)>maxfringe:
                maxfringe = len(st.items)
    print 'Cannot be solved'

##A*

def solveA(pq):
    global maxfringe,maxdepth
    current = pq.get()[1]
    visitedstates = {}
    stringc = str(current.nums)
    visitedstates[stringc] = current.hfn
    pq.put((current.hfn,current))
    while pq.empty() != True:
        current = pq.get()[1]
        if current.checkgoal():
            if current.depth>maxdepth:
                maxdepth = current.depth
##            print current.nums,nodesExp
            return solutionfound(current)
        else:
            children = []
            children.extend(expandnode(current))
            for c in children:
                stringc = str(c.nums)
                if stringc in visitedstates:
                    old = visitedstates[stringc]
                    if old<=c.hfn:
                        continue
                else:
                    pq.put((c.hfn,c))
                    visitedstates[stringc] = c.hfn
            if len(pq.queue)>maxfringe:
                maxfringe = len(pq.queue)
    print 'Cannot be solved'


##IDA*

def solveIDA(pq,depthlimit):
    global maxfringe,maxdepth,solvedida
    current = pq.get()[1]
    visitedstates = {}
    stringc = str(current.nums)
    visitedstates[stringc] = current.hfn
    pq.put((current.hfn,current))
    while pq.empty() != True:
        current = pq.get()[1]
        if current.checkgoal():
            solvedida = True
            if current.depth>maxdepth:
                maxdepth = current.depth
##            print current.nums,nodesExp
            return solutionfound(current)
        else:
            if current.depth == depthlimit:
                print 'No solution at depth = ',depthlimit
                return [0,0,0,0]
            children = []
            children.extend(expandnode(current))
            for c in children:
                stringc = str(c.nums)
                if stringc in visitedstates:
                    old = visitedstates[stringc]
                    if old<=c.hfn:
                        continue
                else:
                    pq.put((c.hfn,c))
                    visitedstates[stringc] = c.hfn
            if len(pq.queue)>maxfringe:
                maxfringe = len(pq.queue)


def main():
    global n,maxdepth,maxfringe,checkedstates,solvedida,actualdict,goalstate
    n = int(sys.argv[1])
    for i in range(n):
            for j in range(n):
                actualdict.append([i,j])
    goalstate = [[i+n*j for i in range(n)] for j in range(n)]
    k=2
    initial = [x[:] for x in [[0]*n]*n]
    for i in range(n):
        for j in range(n):
            initial[i][j] = int(sys.argv[k])
            k = k+1
            
    method = sys.argv[k]
##    print method

##    initial=[[1,2,5],[3,4,0],[6,7,8]]     #easy
##    initial=[[1,4,2],[7,5,8],[3,0,6]]       #medium
##    initial=[[0,8,7],[6,5,4],[3,2,1]]       #hard
    initialstate = State(initial,None,'Start',1)
    stringc = str(initial)
    checkedstates.add(stringc)
##    method = 'A*'
    if method == 'BFS':
        print 'BFS\n\n'
        print 'Initial State: ',initial
        q = Queue.Queue()
        t1 = time.time()
        q.put(initialstate)
        [solution,directions,cost,nodesExp] = solveBFS(q)
        t2 = time.time()
        timereq = t2-t1
        sq = 'Queue'
    if method == 'DFS':
        print 'DFS\n\n'
        print 'Initial State: ',initial
        st = Stack()
        t1 = time.time()
        st.push(initialstate)
        [solution,directions,cost,nodesExp] = solveDFS(st)
        t2 = time.time()
        timereq = t2-t1
        sq = 'Stack'
    if method == 'A*':
        print 'A*\n\n'
        print 'Initial State: ',initial
        pq = Queue.PriorityQueue()
        t1 = time.time()
        pq.put((initialstate.hfn,initialstate))
        [solution,directions,cost,nodesExp] = solveA(pq)
        t2 = time.time()
        timereq = t2-t1
        sq = 'Priority Queue'

    if method == 'IDA*':
        print 'IDA*\n\n'
        print 'Initial State: ',initial
        depthlimit = 0
        while solvedida != True:
            depthlimit = depthlimit+1
            pq = Queue.PriorityQueue()
            t1 = time.time()
            pq.put((initialstate.hfn,initialstate))
            [solution,directions,cost,nodesExp] = solveIDA(pq,depthlimit)
            t2 = time.time()
            timereq = t2-t1
            sq = 'Priority Queue'
        
    print '{',
    for i in xrange(cost):
        print directions.pop(),',',
##        print_board(solution.pop()),'\n\n'
    print 'GOAL REACHED }'
    print 'The Cost of the solution is: ', cost-1
    print 'The number of nodes expanded are: ',nodesExp
    print 'Maximum depth of ',sq,' is: ',maxdepth
    print 'Maximum fringe size is: ',maxfringe
    memreq = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024
    print 'Memory requirement is: ',memreq
    print 'Running time is: ',timereq

if __name__=='__main__':
    main()
