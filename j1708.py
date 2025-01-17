class Message:
    def __init__(self, mid,content,checksum,pos,length):
        self.mid= mid
        self.content = content
        self.length = length
        self.pos = pos
        self.checksum = checksum
    def checksum(self,array): #requires refactoring!
        checksum = 0
        for x in range(0, (len(array)-1)):
            checksum += array[x]
        checksum &= 255
        checksum = 256 - checksum
        return checksum
    def __eq__(self,other):
        return self.content == other.content
    def __hash__(self):
        return hash(('content',str(self.content)))
    

def to_dec(string):
    array = []
    n = 2
    array = [string[i:i+n] for i in range(0,len(string),n)]
    array = [int(x, 16) for x in array]
    return array

def checksum(array):
    """Calculate J1708 checksum."""
    return (256 - sum(array[:-1]) % 256) & 0xFF
    
    
    # checksum = 0
    # for x in range(0, (len(array)-1)):
    #     checksum += array[x]
    # checksum &= 255
    # checksum = 256 - checksum
    # return checksum
