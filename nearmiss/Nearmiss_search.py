#Near miss study
#
#This explores a hopefully simple way to create a regex pattern from user input that attempts to account for spelling errors and other typos
#
#The origin of this idea is from thoughts on how a simple search would work for only file or object titles and 
#from descriptions of ww1/2 naval battles where splashes from shells would be used to correct the aim of naval guns on battleships
#this idea depends on a qwerty keyboard organized like the below which is modeled off of my personal keyboard (Model M reproduction)
# 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 0 | - | =
#   Q | W | E | R | T | Y | U | I | O | P | [ | ] | \
#     A | S | D | F | G | H | J | K | L | : | '
#       Z | X | C | V | B | N | M | < | > | /


class keyboard_key():
    def __init__(self,key, l=None,lu=None,ld=None,r=None,ru=None,rd=None,altkey=None) -> None:
        self.corekey = key          #this is the non-shift modified key ie: 1
        self.corealt = altkey       #this is the shift modified key ie: !
        self.left = l
        self.leftup = lu
        self.leftdown = ld
        self.right = r
        self.rightup = ru
        self.rightdown = rd
    def get_self(self) -> tuple:
        return (self.corekey,self.corealt)
    def get_cluster(self) -> list:  #returns a list of tuples
        ret_set = [x.get_self() for x in [self.left,self.leftup,self.leftdown,self.right,self.rightup,self.rightdown] if x != None] #non-existant keys need to be removed
        return {(self.corekey,self.corealt):ret_set}
    def get_clusteredset(self) -> set:  #this grabs neighboring keys
        ret_set = {self.get_self()[0],self.get_self()[1]}
        working_data = self.get_cluster()
        for i in working_data[self.get_self()]:
            ret_set.add(i[0])
            ret_set.add(i[1])
        ret_set.remove(None)
        return ret_set
    def get_clusteredstr(self) -> str:
        retstr = ""
        for i in self.get_clusteredset():
            retstr += i
        return retstr
    def set_left(self,inp_obj = None):
        if inp_obj == None or type(self) != type(inp_obj):
            return None
        self.left = inp_obj
    def set_leftup(self,inp_obj = None):
        if inp_obj == None or type(self) != type(inp_obj):
            return None
        self.leftup = inp_obj
    def set_leftdown(self,inp_obj = None):
        if inp_obj == None or type(self) != type(inp_obj):
            return None
        self.leftdown = inp_obj
    def set_right(self,inp_obj = None):
        if inp_obj == None or type(self) != type(inp_obj):
            return None
        self.right = inp_obj
    def set_rightup(self,inp_obj = None):
        if inp_obj == None or type(self) != type(inp_obj):
            return None
        self.rightup = inp_obj
    def set_rightdown(self,inp_obj = None):
        if inp_obj == None or type(self) != type(inp_obj):
            return None
        self.rightdown = inp_obj
    def __str__(self) -> str:
        return (self.corekey,self.corealt)

def spawn_keyboard() -> keyboard_key:   #this returns the top left most node in the tree that is intended to represent a physical keyboard.
    def horizon_linker(char_row,key_row):
        for i in char_row:
            key_row.append(keyboard_key(i) if type(i) != tuple else keyboard_key(i[0],altkey=i[1]))
        for i in range(len(key_row)-1):
            if i < len(key_row):
                key_row[i].set_right(key_row[i+1])
                key_row[i+1].set_left(key_row[i])
    t_row = [('`','~'),('1','!'),('2','@'),('3','#'),('4','$'),('5','%'),('6','^'),('7','&'),('8','*'),('9','('),('0',')'),('-','_'),('=','+')]
    trow_key = []
    horizon_linker(t_row,trow_key)
    midup_row = ['q','w','e','r','t','y','u','i','o','p',('[','{'),(']','}'),('\\','|')]
    murow_key = []
    horizon_linker(midup_row,murow_key)
    middown_row = ['a','s','d','f','g','h','j','k','l',(';',':'),('\'','"')]
    mdrow_key = []
    horizon_linker(middown_row,mdrow_key)
    bot_row = ['z','x','c','v','b','n','m',(',','<'),('.','>'),('/','?')]
    brow_key = []
    horizon_linker(bot_row,brow_key)
    def zigzag_linker(top_left,bottom_left):
        def hasnext_step(curtop,curbot,current):
            if (curtop == current_pointer and curbot == None) or (curbot == current_pointer and curtop == None) or current == None:
                return False
            else:
                return True
        #this takes a top left node and a bottom left node and zips their linked lists together starting from top left
        curtop_pointer = top_left
        curbot_pointer = bottom_left
        current_pointer = top_left
        while(hasnext_step(curtop_pointer,curbot_pointer,current_pointer)):
            if curtop_pointer == current_pointer:
                current_pointer.set_rightdown(curbot_pointer)
                curbot_pointer.set_leftup(current_pointer)
                curtop_pointer = curtop_pointer.right
                current_pointer = curbot_pointer
            else:
                current_pointer.set_rightup(curtop_pointer)
                curtop_pointer.set_leftdown(current_pointer)
                curbot_pointer = curbot_pointer.right
                current_pointer = curtop_pointer
    zigzag_linker(trow_key[1],murow_key[0]) #0 is tilde which does not have a downright key associated with it
    zigzag_linker(murow_key[0],mdrow_key[0])
    zigzag_linker(mdrow_key[0],brow_key[0])
    return trow_key[0]

def find_key(inp_key= 'A',inp_keyboard = spawn_keyboard(),visited_keys = [None]) -> keyboard_key:   #this could use a bit of clean up if I come back to this project
    inp_key = inp_key.lower()
    test_self = inp_keyboard.get_self()
    extend_targ = [x if not x in visited_keys else "-zzz" for x in inp_keyboard.get_self()]
    while "-zzz" in extend_targ: extend_targ.remove("-zzz")
    visited_keys.extend(extend_targ)
    if inp_key in inp_keyboard.get_self():
        return inp_keyboard
    else:                   #this section will create a list of nodes to visit. that list will then be iterated through.
        atts = dir(inp_keyboard)
        adjacent_keys = []
        for i in atts:
            if "__" in i or "set" in i or "get" in i or "core" in i:
                pass
            else:
                targ_key = getattr(inp_keyboard,i)
                if targ_key == None or (targ_key.get_self()[0] in visited_keys and targ_key.get_self()[1] in visited_keys):#this is here due to the alphabetical characters all having none as their alt key
                    pass
                else:
                    adjacent_keys.append(getattr(inp_keyboard,i))
    for i in adjacent_keys:
        cur_i = find_key(inp_key,i,visited_keys)
        if cur_i == None:
            pass
        else:
            return cur_i
    return None

def find_keycluster(inp_key, string= False):            #find a single key, return it and its neighbors
    if type(inp_key) != str and len(inp_key) != 1:
        return False
    else:
        grab_key = find_key(inp_key,visited_keys=[])
        if not string:
            return grab_key.get_cluster() if grab_key != None else False
        else: 
            return grab_key if grab_key != None else False

def find_stringcluster(inp_string,string = False):      #find the keys and neighbors of each key in a cluster
    if type(inp_string) != str:
        return False
    clustered_string = []
    for i in inp_string:
        i_grab = find_keycluster(i,True)
        if not i_grab == False:
            if string:
                clustered_string.append(i_grab.get_clusteredstr())
            else:
                clustered_string.append(i_grab.get_clusteredset())
    return clustered_string

def find_stringregex(inp_str,mysql=False):              #similar to find_stringcluster, but instead returns a regex pattern
    if type(inp_str) != str:
        return False
    ret_str = r""
    for i in find_stringcluster(inp_str,True):
        if not mysql:
            ret_str += r'['+i+r'\s]{1,2}'       #currently having it looking for missing and duplicated characters just in case. i might remove the ,2 in favor of ,1
        else:
            ret_str += (r'['+i+r':space:]{1,2}')     
    ret_str = ret_str.replace(r'-',r'\-').replace(r'^',r'\^')    #can't use '-' without being escaped because it's the range operator
    return ret_str

def get_regexcompiledregex(inp_str):                    #find_stringregex but returns a regex object that's already compiled and ready to use
    if type(inp_str) != str:
        return False
    import re
    return re.compile(find_stringregex(inp_str),flags=(0 ^ re.IGNORECASE ^ re.MULTILINE))

def get_regexcompiledregex_mysql(inp_str):              #get_regexcompiledregex but returns a mysql/mariadb compliant output from that function. this is from a specific use case where this module was used in another project involving django and mariadb
    if type(inp_str) != str:
        return False
    import re
    return re.compile(find_stringregex(inp_str,True),flags=(0 ^ re.IGNORECASE ^ re.MULTILINE))



