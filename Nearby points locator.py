class Linked_list():  
    pass
    class Node_ll():
        def __init__(self,x):
            self._x = x
            self._prev = None
            self._next = None

    def __init__(self):    # maintained head and last for the linked list . 
        self._head = None
        self._last = None

    def is_Empty(self):
        if self._head == None :
            return True 
        else :
            return False

    def push(self,y):
        ptr = self.Node_ll(y)
        if self._head == None:
            self._head = ptr
            self._last = ptr
        else :
            self._last._next = ptr
            ptr._prev = self._last
            self._last = ptr

    def pop_first(self):       # pops the first element which is the head of the list .
        if Linked_list.is_Empty(self) == False :
            popped = self._head
            self._head = self._head._next
            if self._head != None:
                self._head._prev = None
            return popped._x   

class AVL_tree():     # Created a class for a balanced BST .
    pass
    class Node():
        def __init__(self,x):
            self._L1 = Linked_list()
            self._x = x
            self._second_structure = None   # will store the reference of the root of the balanced BST of y points of the leaf nodes of the subtree rooted at this node.
            self._parent = None
            self._left = None
            self._right = None

    def __init__(self):
        self._root = None


    def build_balanced_tree_y(self,A,B,i,j,L):   # balanced BST wrt y coordinates. 
        if j==i:
            leaf_node = self.Node((B[i]))
            return leaf_node
        else:
            median = (i+j)//2   
            
            left_node =  self.build_balanced_tree_y(A,B,i,median,L)
            right_node = self.build_balanced_tree_y(A,B,median+1,j,L)
            node = self.Node((0,B[median][1]))     # since I am storing the point in leaf , for making the other nodes tuple I just made the 1st element of the tuple as 0 and the second as the y coordinate.
            node._left = left_node
            left_node._parent = node
            node._right = right_node
            right_node._parent = node
            self._root = node
            return node

    def build_balanced_tree_x(self,A,B,i,j,L):     # The main balanced BST on x-coordinate. 
        if len(A) == 0:
            return 
        B_l = B[i:j+1]
        B_n = sorted(B_l,key = lambda t:t[1])

        root_of_structure = self.build_balanced_tree_y(A,B_n,0,len(B_n)-1,L)  
        
        if j==i:
            leaf_node = self.Node((A[i]))
            leaf_node._second_structure = root_of_structure
            return leaf_node
        else:
            median = (i+j)//2
            
            left_node =  self.build_balanced_tree_x(A,B,i,median,L)
            right_node = self.build_balanced_tree_x(A,B,median+1,j,L)
            node = self.Node((A[median]))
            node._left = left_node
            left_node._parent = node
            node._right = right_node
            right_node._parent = node
            self._root = node
            node._second_structure = root_of_structure    # attached the y-tree to this node
            return node

class PointDatabase() :
    
    def __init__(self,pointlist):
        self._pointlist = pointlist
        self._x_list = []
        self._y_list = []
        self._link = Linked_list()

        self._x_list = sorted(self._pointlist,key = lambda t:t[0])  # sorted the list on x-coordinate
        self._y_list = sorted(self._pointlist,key = lambda t:t[0])
        self._T1 = AVL_tree()
        
        self._T1.build_balanced_tree_x(self._x_list,self._y_list,0,len(self._x_list)-1,self._link)

    def inorder_helper(self,p,list):    # Since points are stored in leaves of the y-tree , I will use it to append the points which are to be present in the final list .
        if p != None:
            self.inorder_helper(p._left,list)
            if p._left == None and p._right == None:
                list.append(p._x)
            self.inorder_helper(p._right,list)

    def inorder(self,p):
        if p != None:
            self.inorder(p._left)
            if p._left == None and p._right == None:
                print(p._x)
            self.inorder(p._right)
        
    def searchNearby(self,q,d):
        L1 = Linked_list()
        L2 = Linked_list()
        xo1 = q[0] - d
        xo2 = q[0] + d
        yo1 = q[1] - d
        yo2 = q[1] + d
        result_list = []
        splitting  = None
        x_val = self._T1._root
        if self._pointlist == None:
            return result_list
        while x_val!= None:      # To find the node where the splitting happened .
                if xo1 <= x_val._x[0] <= xo2:
                    splitting = x_val
                    break
                if x_val._x[0] < xo1:
                        x_val = x_val._right
                        
                elif x_val._x[0] > xo2:
                        x_val = x_val._left
                

        if splitting == None:    
            return result_list
        
        u = splitting._left   
        v = splitting._right
        while u != None:        
            if u._left == None and u._right == None and xo1<=u._x[0]<=xo2:
                L1.push(u)
            
            if u._x[0] < xo1:
                u = u._right
            else:
                if u._right != None:
                    L1.push(u._right)
                u = u._left
    
        while v != None:
            if v._left == None and v._right == None and xo1<=v._x[0]<=xo2:
                L1.push(v)
                
            if v._x[0] > xo2:
                v = v._left
            else:
                if v._left != None:
                    L1.push(v._left)
                v = v._right
        
        cur = L1._head

        
        while cur != None: # the nodes in the list stores reference of the nodes of the x-tree whose y-tree(second_structure) needs to be searched for finding the required points.
           
            y_val = cur._x._second_structure
            split_y = None
            while y_val != None:  # finding the split node .
                
                if yo1 <= y_val._x[1] <= yo2:
                    split_y = y_val
                    break

                if y_val._x[1] < yo1:
                    y_val = y_val._right
                    
            
                elif y_val._x[1] > yo2:
                    y_val = y_val._left
                    
            
            if split_y == None:
                cur = cur._next
                continue
             

            u_1 = split_y._left
            v_1 = split_y._right
        
            if u_1 == None and v_1 == None:
                result_list.append(split_y._x)
            

            
            while u_1 != None:
                if u_1._left == None and u_1._right == None and yo1<=u_1._x[1]<=yo2:
                    L2.push(u_1)
                   
                if u_1._x[1] < yo1:
                    u_1 = u_1._right
                else:
                    if u_1._left != None:
                        L2.push(u_1._right)
                    u_1 = u_1._left
                
            while v_1 != None:
                if v_1._left == None and v_1._right == None and yo1<=v_1._x[1]<=yo2:
                    L2.push(v_1)
            
                if v_1._x[1] > yo2:
                    v_1 = v_1._left
                else:
                    if v_1._left != None:
                        L2.push(v_1._left)
                    v_1 = v_1._right
                
            y_subtrees_traverse_for_ans = L2._head     # the inorder_helper traversal will give the leaf points which are inside the rectangular region.
            while y_subtrees_traverse_for_ans != None:
                
                self.inorder_helper(y_subtrees_traverse_for_ans._x,result_list)
                L2.pop_first()   # appending the element to the result list and removing from the L2 linked list so that in the next iteration of the next node of the L1 linked list , I won't need to traverse and append the already included part.
                y_subtrees_traverse_for_ans = L2._head
                
            cur = cur._next

        no_repeat = list(set(result_list))  # removing any sort of repeatation in the final list.
        return no_repeat



