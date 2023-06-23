import itertools

class Tabloid:
    def sort_row(self):
        cnt = 0
        for i in self.shape:
            row = self.p[cnt:cnt+i]
            row.sort()
            self.p[cnt:cnt+i] = row
            cnt += i

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

    inversion(m, mid)
    inversion(mid + 1, n)

    i = m; j = mid + 1; k = m
    while (i <= mid and j <= n):
        if (a[i] <= a[j]):
            t[k] = a[i]
            k += 1; i += 1
        else:
            t[k] = a[j]
            k += 1; j += 1
            inv[0] += mid - i + 1

    while (i <= mid):
        t[k] = a[i]
        k += 1; i += 1
    while (j <= n):
        t[k] = a[j]
        k += 1; j += 1
    for i in range(m, n+1):
        a[i] = t[i] 

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
    return Ct

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
    print(Ct(Tabloid([3, 2], [1,4,5,2,3])))