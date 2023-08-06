"""Make path from string!"""

__version__ = "0.2.0"

def path(string):

    def base(num, dst=16, src=10):
        if isinstance(num, str):
            n = int(num, src)
        else:
            n = int(num)
        ab = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        if n < dst:
            return ab[n]
        else:
            return base(n // dst, dst) + ab[n % dst]

    def getCrc(string):
        a = 0xFFFF;
        string = str(string)
        for x in range(len(string)):
            a = a ^ ord(string[x])
            for y in range(8):
                if (a & 0x0001) == 0x0001:
                    a = ((a >> 1) ^ 0xA001)
                else:
                    (a >> 1)
        b = base(a).lower().ljust(4, '0')
        return b[0] + '/' + b[1] + '/' + b[2] + '/' + b[3] + '/'

    return getCrc(str(string))
