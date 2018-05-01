'''
Sasha Morgan
ECE 2500
Cache Compiler
'''

import sys
import math
from math import floor

out = 0
outcache = []
outblock = []
outmap = []
outwrite = []
outhr = []
outmc = []
outcm = []
rwaddress = []


class Block:
    def __init__(self):
        self.db = 0
        self.v = 0
        self.t = -1
        self.life = 0


def multiwaymap(caches, blocks, wp, cachep):
    bc = int(floor(caches / blocks))
    hc = 0
    cm = 0
    mc = 0
    ls = 0
    bsets = 0
    if (cachep == "DM"):
        bsets = 1
    if (cachep == "2W"):
        bsets = 2
    if (cachep == "4W"):
        bsets = 4
    if (cachep == "FA"):
        bsets = bc
    sets = int(floor(bc / bsets))
    ssize = int(floor(caches / bsets))
    cho = bsets

    tag = [[-1 for x in range(cho)] for y in range(sets)]
    db = [[0 for x in range(cho)] for y in range(sets)]
    life = [[0 for x in range(cho)] for y in range(sets)]
    validation = [[0 for x in range(cho)] for y in range(sets)]

    count = 0
    while (count < len(rwaddress)):
        tempadd = rwaddress[count][1]  # read word from address
        tempinst = rwaddress[count][0]
        index = int(floor(tempadd / blocks)) % sets
        ctag = int(floor(tempadd / ssize))
        tlist = tag[index]

        hit = 0
        bi = 0

        tt = 0
        while (tt < len(tlist)):
            if (tlist[tt] == ctag):
                bi = tt
                if (validation[index][bi] == 1):
                    hit = 1
                    break
            tt = tt + 1

        if (hit == 1):
            hc = hc + 1
            life[index][bi] = count + 1

            if (tempinst == "write"):
                if (wp == "WB"):
                    db[index][bi] = 1
                if (wp == "WT"):
                    cm = cm + 4
        else:
            mc = mc + blocks
            alist = life[index]
            cnt = 0

            minv = min(life[index])
            while (cnt < len(alist)):
                if (minv == alist[cnt]):
                    bi = cnt
                    break
                cnt = cnt + 1

            tag[index][bi] = ctag
            validation[index][bi] = 1
            life[index][bi] = count + 1
            if (wp == "WB"):
                if (db[index][bi] == 1):
                    cm = cm + blocks
                    db[index][bi] = 0
            if (tempinst == "write"):
                if (wp == "WB"):
                    db[index][bi] = 1
                if (wp == "WT"):
                    cm = cm + 4
        count = count + 1

    pp = 0
    xx = 0
    while (pp < len(db)):
        while (xx < len(db[pp])):
            if (db[pp][xx] == 1):
                cm = cm + blocks
            xx = xx + 1
        xx = 0
        pp = pp + 1

    hr = hc / len(rwaddress)
    outcache.append(caches)
    outblock.append(blocks)
    outmap.append(cachep)
    outwrite.append(wp)
    outhr.append(hr)
    outmc.append(mc)
    outcm.append(cm)


if __name__ == '__main__':

    csizes = [1024, 4096, 65536, 131072]
    bsizes = [8, 16, 32, 128]
    ctype = ["DM", "2W", "4W", "FA"]
    wtype = ["WB", "WT"]

    # The command line argument

    if len(sys.argv) != 3:
        sys.stderr.write("Command line format: python3 main.py <trace file>\n")
        sys.exit(0)

    # reading in the data
    if len(sys.argv) == 3:
        f = (open(sys.argv[1]))
        rows = f.readlines()
        count = 0
        while (count < len(rows)):
            rtempr = rows[count]
            [readorwrite, hexv] = rtempr.split()
            rtemp = int(hexv, 0)
            rwaddress.append((readorwrite, rtemp))
            count = count + 1
    read1 = 0
    r2 = 0
    r3 = 0
    r4 = 0

    while (read1 < len(csizes)):
        while (r2 < len(bsizes)):
            while (r3 < len(ctype)):
                while (r4 < len(wtype)):
                    # Caches c(csizes[read1], bsizes[r2], wtype[r4], ctype[r3])
                    out = out + 1
                    multiwaymap(csizes[read1], bsizes[r2], wtype[r4],
                                ctype[r3])

                    r4 = r4 + 1
                    # End of Wtype
                r4 = 0
                r3 = r3 + 1
                # end of ctype
            r3 = 0
            r2 = r2 + 1
            # end of btype
        read1 = read1 + 1
        r2 = 0
        r3 = 0
        r4 = 0
        # end of
    outfile = open(sys.argv[2], 'w')

    cnt = 0
    stringout = ""

    while (cnt < out):
        stringout = str(outcache[cnt]) + "\t" + str(
            outblock[cnt]) + "\t" + str(outmap[cnt]) + "\t" + str(
                outwrite[cnt]) + "\t" + ("%0.2f" % outhr[cnt]) + "\t" + str(
                    outmc[cnt]) + "\t" + str(outcm[cnt]) + "\n"
        #print(stringout)
        outfile.write(stringout)
        cnt = cnt + 1
