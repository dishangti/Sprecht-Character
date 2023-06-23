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

def Ct(shape, p):
    """
    Column stablizer
    """
    Ct = []
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
        Ct.append(itertools.permutations(col[i]))
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

    Ct([3, 2], [1,4,5,2,3])