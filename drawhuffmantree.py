import sys
import turtle as t
from collections import defaultdict
import heapq
import copy

writecodingflag = 0

class node :
    def __init__(self,rate,name,pos=(0,0),isnode=False):
        self.name = name
        self.rate = rate
        self.pos = pos
        self.is_node = isnode
        self.left = None
        self.right = None

    def __lt__(self,other) :
        return self.rate < other.rate

    def __gt__(self,other) :
        return self.rate > other.rate


def drawnode(nodex):
    t.penup()
    t.goto(nodex.pos)
    if nodex.name :
        t.write(nodex.name)
    else :
        t.write(nodex.rate)
    t.pendown()
    t.circle(20)
    t.penup()

def connectnode(node1,node2) :
    t.penup()
    t.goto((node1.pos[0],node1.pos[1]+10*4))
    t.pendown()
    t.goto((node2.pos[0],node2.pos[1]))
    t.penup()

def writecoding(nodehead,coding) :
    global writecodingflag
    t.penup()
    if writecodingflag :
        t.goto((nodehead.pos[0]-5,nodehead.pos[1]-40))
        writecodingflag = 1 - writecodingflag
    else :
        t.goto((nodehead.pos[0]-5,nodehead.pos[1]+40))
        writecodingflag = 1 - writecodingflag
    t.pendown()
    t.write(coding)
    t.penup()

def drawhuffmancoding(nodehead,coding) :
    if nodehead :
        writecoding(nodehead,coding)
    else :
        return 
    drawhuffmancoding(nodehead.left,coding+"0")
    drawhuffmancoding(nodehead.right,coding+"1")    


def build_tree(huffmanstring) : 
    sym2freq = defaultdict(int)
    for i in huffmanstring :
        sym2freq[i] += 1

    heap = []
    for key , rate in sym2freq.items() :
        heapq.heappush(heap,node(rate,key,(0,0),True))

    time = 0

    drawlist = []

    while (len(heap)>1) :
        node1 = heapq.heappop(heap)
        node2 = heapq.heappop(heap)

        if node1.is_node :
            node1.pos = (time*100,node1.pos[1])
            time += 1
        if node2.is_node :
            node2.pos = (time*100,node2.pos[1])
            time += 1

        tempnode = node(node1.rate+node2.rate,"")
        tempnode.left = node1
        tempnode.right = node2

        drawlist.append(node1)
        drawlist.append(node2)
        drawlist.append(tempnode)

        heapq.heappush(heap , tempnode)
        
    tree_head = heapq.heappop(heap)
    tree_height = get_tree_height(tree_head) - 1
    floor_height = int((1500-40) / (tree_height))
    floor_node_distance = 1500/(2**tree_height-1) * (2**(tree_height - 2))
    set_pos_for_everynode(tree_head,1500/2,1500-40,floor_height,floor_node_distance)

    for i in range(0,len(drawlist),3) :
        a , b , c = drawlist[i:i+3]
        if a.is_node :drawnode(a)
        if b.is_node :drawnode(b)
        drawnode(c)
        connectnode(a,c)
        connectnode(b,c)

    return tree_head

def get_tree_height(tree_head) :
    if not tree_head :
        return 0
    return max(get_tree_height(tree_head.left)+1 , get_tree_height(tree_head.right)+1)

def get_node_heap(tree_head , heap) :
    if not tree_head :
        return 
    if tree_head.is_node :
        copynode = copy.copy(tree_head)
        heapq.heappush(heap,copynode) 
    get_node_heap(tree_head.left,heap)
    get_node_heap(tree_head.right,heap)



def set_pos_for_everynode(tree_head,posx,posy,floor_height,floor_node_distance):
    if not tree_head :
        return 
    tree_head.pos = (posx,posy)
    set_pos_for_everynode(tree_head.left,posx-floor_node_distance,posy - floor_height,
        floor_height,int(floor_node_distance/2))
    set_pos_for_everynode(tree_head.right,posx+floor_node_distance,posy-floor_height,
        floor_height,int(floor_node_distance/2))

def debug(nodehead) :
    if not nodehead :
        return
    # print("nodename : %s  noderate: %d nodepos: %d %d"%(nodehead.name , nodehead.rate , nodehead.pos[0] , nodehead.pos[1]))
    debug(nodehead.left)
    debug(nodehead.right)

def drawtree(tree_head,prenode) :
    if not tree_head :
        return
    if tree_head.is_node:
        drawnode(tree_head)
        connectnode(tree_head,prenode)
    drawtree(tree_head.left,tree_head)
    drawtree(tree_head.right,tree_head)


class huffman :
    def __init__(self):
        self.recivced_data = None
        self.origin_content = None

    def dealwithrecived(self) :
        data = self.recivced_data
        data = data.split("\r\n")
        coding = data[1:-1]
        content = data[-1]
        codingmap = {}

        for i in coding :
            symbol ,_, code = i.split('\t')
            codingmap[code] = symbol[1]
        content = content[9:-2]
        content = content.strip().split(' ')

        origin_content = ""
        for i in content :
            origin_content += codingmap[i]
        self.origin_content = origin_content
        return origin_content


if __name__ == "__main__":
    if len(sys.argv) <= 1 :
        print("You need to input a string to draw a tree")
        exit()

    origin_content = ''.join(sys.argv[1:])

    t.setworldcoordinates(0,0,1500,1500)
    node_head = build_tree(origin_content)
    drawhuffmancoding(node_head,"0")
    t.done()
    debug(node_head)
