import itertools
import numpy as np
import sympy

class Tabloid:
    def sort_row(self):
        cnt = 0
        for i in self.shape:
            row = self.p[cnt:cnt+i]
            row.sort()
            self.p[cnt:cnt+i] = row
            cnt += i

    def permut_Ct(self, p, base):
        """
        Action of column stablizer
        """
        new_t = Tabloid(self.shape, self.p)
        for col in range(len(p)):
            for row in range(len(p[col])):
                b = new_t.p.index(base[col][row])
                new_t.p[b] = p[col][row]
        new_t.sort_row()
        return new_t()

    def permut(self, p):
        """
        Action of a permutation
        """
        new_t = Tabloid(self.shape, self.p)
        for i in range(self.n):
            new_t.p[i] = p[new_t.p[i] - 1]
        new_t.sort_row()
        return new_t

    def __init__(self, shape, p):
        self.n = len(p)
        self.shape = shape
        self.p = p
        self.sort_row()

    def __eq__(self, tb2):
        if self.shape != tb2.shape:
            return False
        cnt = 0
        for i in self.shape:
            if self.p[cnt:cnt+i] != tb2.p[cnt:cnt+i]:
                return False
            cnt += i
        return True
    
    def __str__(self) -> str:
        s = ""
        cnt = 0
        for i in self.shape:
            s += str(self.p[cnt:cnt+i]) + "\n"
            cnt += i
        return s[:-1]

class CTabloid:
    def __init__(self):
        self.vect = []
        self.sgn = []

    def add(self, vect:Tabloid, sgn:int):
        self.vect.append(vect)
        self.sgn.append(sgn)

    def permut(self, p):
        for i in range(len(self.vect)):
            self.vect[i] = self.vect[i].permut(p)

def partition(part_list, n, last, part):
    """
    Get the partition of integer n
    n = n1 + n2 + ... + ns
    where n1 <= n2 <= ... <= ns
    """
    if n == 0:
        part_list.append(part)
    for i in range(last, n+1):
        new_part = part.copy()
        new_part.append(i)
        partition(part_list, n - i, i, new_part)

def inversion(inv, p, t, m, n):
    if (m == n): return
    mid = (m+n)>>1

    inversion(inv, p, t, m, mid)
    inversion(inv, p, t, mid + 1, n)

    i = m; j = mid + 1; k = m
    while (i <= mid and j <= n):
        if (p[i] <= p[j]):
            t[k] = p[i]
            k += 1; i += 1
        else:
            t[k] = p[j]
            k += 1; j += 1
            inv[0] += mid - i + 1

    while (i <= mid):
        t[k] = p[i]
        k += 1; i += 1
    while (j <= n):
        t[k] = p[j]
        k += 1; j += 1
    for i in range(m, n+1):
        p[i] = t[i] 

def Ct(t):
    """
    Column stablizer
    """
    shape, p = t.shape, t.p
    col_Ct = []

    col = []
    n = len(p)

    cnt = 0
    for i in shape:
        row = p[cnt:cnt+i]
        for j in range(len(row)):
            if j >= len(col):
               col.append([])
            col[j].append(row[j])
        cnt += i
    
    for i in range(len(col)):
        col_Ct.append(list(itertools.permutations(col[i])))

    if len(col) > 1:
        Ct = list(itertools.product(col_Ct[0], col_Ct[1]))
        for i in range(2, len(col)):
            Ct = list(itertools.product(Ct, col_Ct[i]))
            for j in range(len(Ct)):
                Ct[j] = Ct[j][0] + Ct[j][1:]
    else:
        Ct = col_Ct[0]
    Ct.sort()
    return Ct

def sgn_Ct(p, n):
    sgn = 1
    t = [0] * n
    print('3',p)
    for i in range(len(p)):
        inv = [0]
        inversion(inv, list(p[i]), t, 0, len(p[i])-1)
        inv = inv[0]
        subsgn = (-((inv & 1) << 1)) + 1
        sgn *= subsgn
        print(p[i], subsgn, inv)
    return sgn

def get_et(shape, p, Ct):
    """
    Polyoid
    """
    et = CTabloid()
    base = Ct[0]
    for g in Ct:
        sgn = sgn_Ct(g)
        tb = Tabloid(shape, p)
        tb = tb.permut_Ct(g, base)
        et.add(tb, sgn)

def get_basis(et, n):
    permut = itertools.permutations(list(range(1, n+1)))
    vects = []
    assign = {}
    inv_assign = {}
    n = -1
    for g in permut:
        g_et = et.permut(g)
        vects.append(g_et)

        for vect in g_et.vect:
            vect = tuple(vect)
            if vect not in assign:
                n += 1
                assign[vect] = n
                inv_assign[n] = vect

    mat = np.zeros((n,1))
    for v in vects:
        v_cor = np.zeros((n, 1))
        for tb in range(len(v.vect)):
            v_cor[assign[v.vect[tb]]] = v.sgn(tb)
        mat = np.c_[mat, v_cor]
    
    mat = mat[:, 1:]
    _, basis_idx =  sympy.Matrix(mat).T.rref()
    basis = []
    for idx in basis_idx:
        basis.append([vects[idx]])
    return basis

if __name__ == "__main__":
    n = int(input())
    part_list = []
    partition(part_list, n, 1, [])
    print(f"Partition of {n}\n", part_list, "\n")

    a = Tabloid([3,2], [1, 4, 5, 2, 3])
    b = Tabloid([3,2], [4, 1, 5, 3, 2])
    c = Tabloid([3,2], [1, 2, 3, 4, 5])

    print("T1:")
    print(a, "\n")
    print("T2:")
    print(b, "\n")
    print("T3:")
    print(c, "\n")
    print("T1 == T2", a == b)
    print("T2 == T3", b == c, "\n")

    print("Permutation: (1 2 3)(4 5)")
    p = [2, 3, 1, 5, 4]
    print("Action on T1:")
    print(a.permut(p), "\n")
    
    print('Column stablizer of T1')
    ct = Ct(Tabloid([3, 2], [1,4,5,2,3]))
    print(ct)
    print(sgn_Ct(ct[1], 5))