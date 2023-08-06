"""Make path from string!"""

__version__ = "0.2.2"


def path(string):
    """Make path from string!"""

    def base(num, dst=16, src=10):
        """Init base"""
        if isinstance(num, str):
            _n = int(num, src)
        else:
            _n = int(num)
        _ab = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        if _n < dst:
            return _ab[_n]
        return base(_n // dst, dst) + _ab[_n % dst]

    def get_crc(string):
        """Move chars"""
        _a = 0xFFFF
        string = str(string)
        _l = len(string)
        for _x in range(_l):
            _a = _a ^ ord(string[_x])
            for _y in range(8):
                if (_a & 0x0001) == 0x0001:
                    _a = (_a >> 1) ^ 0xA001
                # else:
                # (_a >> 1)
        _b = base(_a).lower().ljust(4, "0")
        return _b[0] + "/" + _b[1] + "/" + _b[2] + "/" + _b[3] + "/"

    return get_crc(str(string))
