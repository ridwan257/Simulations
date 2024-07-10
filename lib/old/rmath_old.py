import random

def create2Dlist(r,c):
    lst = []
    while r > 0:
        row = []
        j = c
        while j > 0:
            row.append(0)
            j -= 1
        lst.append(row)
        r -= 1
    return lst



def to_int(*nums):
    new_nums = []
    for n in nums:
        new_nums.append(int(n))
    return new_nums



class create_matrix:
    @classmethod
    def random(cls, m, n):
        ans = cls(m, n)
        for i in range(m):
            for j in range(n):
                num = random.randint(-10, 10)
                ans.value[i][j] = num
        return ans

    def __init__(self, m, n):
        self.dim = (m, n)
        self.value = create2Dlist(m,n)

    def render(self):
        txt = ""
        m = self.dim[0]
        for i in range(m):
            txt_list = list(map(lambda n: str(n) if n < 0 else (" "+str(n)), self.value[i]))
            txt1 = "\t".join(txt_list)
            txt += txt1 
            txt += "\n" if not i == m-1 else ""

        return txt

    def __eq__(self, other):
        m1, n1 = self.dim
        m2, n2 = other.dim
        if m1 == m2 and n1 == n2:
            for i in range(m1):
                for j in range(n2):
                    if not self.value[i][j] == other.value[i][j]:
                        return False
        return True

    def __add__(self, other):
        m1, n1 = self.dim
        m2, n2 = other.dim
        if m1 == m2 and n1 == n2:
            ans = create_matrix(m1, n2)
            for i in range(m1):
                for j in range(n2):
                    ans.value[i][j] = self.value[i][j] + other.value[i][j]
            return ans

    def __sub__(self, other):
        m1, n1 = self.dim
        m2, n2 = other.dim
        if m1 == m2 and n1 == n2:
            ans = create_matrix(m1, n2)
            for i in range(m1):
                for j in range(n2):
                    ans.value[i][j] = self.value[i][j] - other.value[i][j]
            return ans
    
    def __mul__(self, other):
        m1, n1 = self.dim
        ans = create_matrix(m1, n1)
        typ = type(other)
        if typ == create_matrix:
            m2, n2 = other.dim
            if n1 == m2:
                for i in range(m1):
                    for j in range(n2):
                        for k in range(n1):
                            ans.value[i][j] += self.value[i][k] * other.value[k][j]
        elif typ == int or typ == float:
            for i in range(m1):
                for j in range(n1):
                    ans.value[i][j] = self.value[i][j] * other
        return ans

    def __neg__(self):
        m, n = self.dim
        ans = create_matrix(m, n)
        for i in range(m):
            for j in range(n):
                num = -1 * self.value[i][j]
                ans.alter(num, i, j)
        return ans
    
    def __abs__(self):
        dim = lambda mtx : (len(mtx), len(mtx[0]))
        def co_fac(mtx, i0, j0):
            m, n = dim(mtx)
            ans = []
            for i in range(m):
                row = []
                for j in range(n):
                    if i != i0 and j != j0:
                        row.append(mtx[i][j])
                ans.append(row)
            ans.remove([])
            return ans

        def find(mtx):
            m = dim(mtx)[0]
            if m == 2:
                d = mtx[0][0] * mtx[1][1] - mtx[0][1] * mtx[1][0]
                return d

            elif m > 2:
                s = 0
                for i in range(m):
                    s += (-1)**i * mtx[0][i] * find(co_fac(mtx, 0, i))
                return s

        if self.dim[0] == self.dim[1]:
            d = find(self.value)
        else :
            d = None
        return d

    def load(self, lst):
        m, n = self.dim
        for i in range(m):
            for j in range(n):
                self.value[i][j] = lst[i][j]

    def get(self):
        return self.value

    def alter(self, num, i, j):
        self.value[i][j] = num


class create_vector:
    @classmethod
    def random2D(cls, lower=-10, upper=10):
        v = cls()
        v.x = random.randint(lower, upper)
        v.y = random.randint(lower, upper)
        return v
    
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z
    
    def __add__(self, other):
        ans = create_vector()
        ans.x = self.x + other.x
        ans.y = self.y + other.y
        ans.z = self.z + other.z
        return ans
    
    def __sub__(self, other):
        ans = create_vector()
        ans.x = self.x - other.x
        ans.y = self.y - other.y
        ans.z = self.z - other.z
        return ans
    
    def __mul__(self, other):
        ans = create_vector()
        if type(other) == create_vector:
            ans.x = self.x * other.x
            ans.y = self.y * other.y
            ans.z = self.z * other.z
        elif type(other) == int or type(other) == float:
            ans.x = self.x * other
            ans.y = self.y * other
            ans.z = self.z * other
        return ans
    
    def __neg__(self):
        ans = create_vector()
        ans.x = -1 * self.x
        ans.y = -1 * self.y
        ans.z = -1 * self.z
        return ans
    
    def __abs__(self):
        r = self.x * self.x + self.y * self.y + self.z * self.z
        return r**0.5

    def get(self):
        return (self.x, self.y, self.z)

    def get2D(self):
        return (self.x, self.y)

    def mag2(self):
        r = self.x * self.x + self.y * self.y + self.z * self.z
        return r

    def copy(self, other):
        self.x = other.x
        self.y = other.y
        self.z = other.z

    def direction(self):
        ans = create_vector()
        r = abs(self)
        ans.x = self.x / r
        ans.y = self.y / r
        ans.z = self.z / r
        return ans
    
    def set_mag(self, n):
        u = self.direction()
        u *= n
        self.copy(u)
    
    def limit(self, n):
        if abs(self) > n:
            self.set_mag(n)

    def constrain2D(self, x1, y1, x2, y2):
        x, y = constrain_rect(self.get2D(), (x1,y1,x2,y2))        
        self.x = x
        self.y = y


def mat(lst):
    m = len(lst)
    n = len(lst[0])
    for l in lst:
        if not len(l) == n:
            return None
    ans = create_matrix(m,n)
    ans.load(lst)
    return ans 
        
def vec(*arr):
    v = create_vector()
    length = len(arr)
    if length == 1:
        typ = type(arr[0])
        if typ == list or typ == tuple:
            v.x = arr[0][0]
            v.y = arr[0][1]
            v.z = 0 if not len(arr) == 3 else arr[0][2]
    elif length == 2:
        v.x = arr[0]
        v.y = arr[1]

    return v


def rmap(value, vi, vf, ri, rf):
    c = (vf - value) / (vf - vi)
    r = rf - (rf - ri) * c
    return r




#checking function
def check_rect(pos, rect_info):
    x, y = pos
    x1, y1, x2, y2 = rect_info
    if x >= x1 and x <= x2:
        if y >= y1 and y <= y2:
            return True
    return False

def constrain_rect(point, rect_info):
    x, y = point
    x1, y1, x2, y2 = rect_info
    if x < x1:
        x = x1
    elif x > x2:
        x = x2
    if y < y1:
        y = y1
    elif y > y2:
        y = y2
    return (x,y)














if __name__ == "__main__":
    a = create_matrix.random(3,2)

    b = create_matrix.random(3,2)

    d = create_matrix(2,3)
    arr = [[-1,3,4], [2,1,3], [-2,5,-7]]
    
    e = -a + b

    pt = vec((-1,16))
    print(pt.get2D())
    pt.constrain2D(0,0,10,15)
    print(pt.get2D())
    