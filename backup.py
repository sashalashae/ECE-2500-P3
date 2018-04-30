'''
Sasha Morgan
ECE 2500
Cache Compiler
'''

import sys
import math

out = 0
outcache = []
outblock = []
outmap = []
outwrite = []
outhr = []
outmc = []
outcm = []
rwaddress = []


def direct_mapped(caches, blocks, wp, cachep):
    # Block Count
    bc = int(caches / blocks)
    cpr = 1
    hr = 0.00
    hc = 0
    mc = 0
    cm = 0
    tag = []
    validation = []
    dirtybit = []
    j = 0
    while (j < bc):
        tag.append(0)
        validation.append(0)
        dirtybit.append(0)
        j = j + 1

    count = 0
    while (count < len(rwaddress)):
        tempadd = rwaddress[count][1]  # read word from address
        tempinst = rwaddress[count][0]

        # Determine the block index
        index = int(tempadd / blocks)
        index = index % bc
        ctag = int(tempadd / caches)

        if (tempinst == "read"):
            if (tag[index] == ctag):
                hc = hc + 1
            elif (tag[index] != ctag or validation[index] == 0):
                tag[index] = ctag
                mc = mc + blocks
                if (validation[index] == 1):
                    validation[index] = 0
                    cm = cm + blocks
        if (tempinst == "write"):
            if (tag[index] == ctag):
                hc = hc + 1
                if (wp == "WT"):
                    cm = cm + 4
                elif (wp == "WB"):
                    validation[index] = 1
            elif (tag[index] != ctag or validation[index] == 0):
                if (wp == "WT"):
                    tag[index] = ctag
                    mc = mc + blocks
                    cm = cm + 4
                elif (wp == "WB"):
                    mc = mc + blocks
                    tag[index] = ctag
                    if (validation[index] == 1):
                        cm = cm + blocks
                    else:
                        validation[index] = 1
                        dirtybit[index] = 1

        count = count + 1
    inc = 0
    while (inc < len(validation)):
        if (validation[inc] == 1):
            cm = cm + blocks
        inc = inc + 1

    hr = round((hc / len(rwaddress)), 2)
    outcache.append(caches)
    outblock.append(blocks)
    outmap.append(cachep)
    outwrite.append(wp)
    outhr.append(hr)
    outmc.append(mc)
    outcm.append(cm)


# End of Direct Mapped


# Start of Fully associative
def full_assoc(caches, blocks, wp, cachep):
    bc = int(caches / blocks)
    hr = 0.00
    hc = 0
    mc = 0
    cm = 0
    ls = 0
    sets = 0
    cho = 0
    comps = 0

    # Write Bits Arry
    # Age Array
    if (cachep == "FA"):
        sets = 1
        cho = bc
    if (cachep == "2W"):
        sets = bc
        sets = int(sets / 2)
        cho = 2
    if (cachep == "4w"):
        sets = bc
        sets = int(sets / 4)
        cho = 4
    # Tags Array
    tag = [[-1 for x in range(sets)] for y in range(cho)]
    wrb = [[0 for x in range(sets)] for y in range(cho)]
    life = [[0 for x in range(sets)] for y in range(cho)]
    ii = 0
    count = 0
    while (count < len(rwaddress)):
        tempadd = rwaddress[count][1]  # read word from address
        tempinst = rwaddress[count][0]
        index = int(tempadd / blocks)
        index = index % sets
        ctag = int((tempadd / blocks) / sets)
        if (tempinst == "read"):
            hit = 0
            ff = 0
            cnt = 0
            while (cnt < cho):
                # Hit
                if (tag[cnt][index] == ctag):
                    hc = hc + 1
                    life[cnt][index] = ls
                    ls = ls + 1
                    hit = 1
                    break
                cnt = cnt + 1
            if (hit != 1):
                cnt = 0
                while (cnt < cho):
                    if (tag[cnt][index] == -1):
                        tag[cnt][index] = ctag
                        life[cnt][index] = ls
                        ls = ls + 1
                        mc = mc + blocks
                        ff = 1
                        break
                    cnt = cnt + 1
            if (ff == 0 and hit == 0):
                cnt = 0
                tmp = 0
                while (cnt < (cho - 1)):
                    if (life[tmp][index] < life[cnt + 1][index]):
                        tmp = cnt
                    else:
                        tmp = cnt + 1
                    cnt = cnt + 1
                if (wrb[tmp][index] == 0 or wrb[tmp][index] == 1):
                    tag[tmp][index] = ctag
                    if (wrb[tmp][index] == 1):
                        cm = cm + (blocks)
                    wrb[tmp][index] = 0
                    mc = mc + blocks
                    life[tmp][index] = ls
                    ls = ls + 1
        if (tempinst == "write"):
            cnt = 0
            hit = 0
            ff = 0
            while (cnt < cho):
                if (tag[cnt][index] == ctag):
                    hc = hc + 1
                    life[cnt][index] = ls
                    if (wp == "WB"):
                        wrb[cnt][index] = 1
                    if (wp == "WT"):
                        cm = cm + 4
                    ls = ls + 1
                    hit = 1
                    break
                cnt = cnt + 1
            if (hit != 1):
                cnt = 0
                while (cnt < cho):
                    if (tag[cnt][index] == -1):
                        tag[cnt][index] = ctag
                        if (wp == "WB"):
                            wrb[cnt][index] = 1
                        if (wp == "WT"):
                            wrb[cnt][index] = 0
                        life[cnt][index] = ls
                        ls = ls + 1
                        mc = mc + blocks
                        if (wp == "WT"):
                            cm = cm + 4
                        ff = 1
                        break
                    cnt = cnt + 1
            if (ff == 0 and hit == 0):
                cnt = 0
                tmp = 0
                while (cnt < (cho - 1)):
                    if (life[tmp][index] < life[cnt + 1][index]):
                        tmp = cnt
                    else:
                        tmp = cnt + 1
                    cnt = cnt + 1
                if (wp == "WT"):
                    tag[tmp][index] = ctag
                    wrb[tmp][index] = 0
                    mc = mc + blocks
                    cm = cm + 4
                    life[tmp][index] = ls
                    ls = ls + 1
                if (wp == "WB"):
                    tag[tmp][index] = ctag
                    if (wrb[tmp][index] == 1):
                        cm = cm + blocks
                    wrb[tmp][index] == 1
                    mc = mc + blocks
                    life[tmp][index] = ls
                    ls = ls + 1

        count = count + 1
    inc = 0
    inr = 0
    if (wp == "WB"):
        while (inc < cho):
            while (inr < sets):
                cm = cm + (wrb[inc][inr] * blocks)
                inr = inr + 1
            inc = inc + 1
            inr = 0

    hr = round((hc / len(rwaddress)), 2)
    outcache.append(caches)
    outblock.append(blocks)
    outmap.append(cachep)
    outwrite.append(wp)
    outhr.append(hr)
    outmc.append(mc)
    outcm.append(cm)


# End of Fully Associative

if __name__ == '__main__':

    csizes = [1024, 4096, 65536, 131072]
    bsizes = [8, 16, 32, 128]
    ctype = ["DM", "2W", "4W", "FA"]
    wtype = ["WB", "WT"]

    # The command line argument

    if len(sys.argv) != 2:
        sys.stderr.write("Command line format: python3 main.py <trace file>\n")
        sys.exit(0)

    # reading in the data
    if len(sys.argv) == 2:
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
                    '''
                    if (ctype[r3] == "DM"):
                        direct_mapped(csizes[read1], bsizes[r2], wtype[r4],
                                      ctype[r3])
                                      '''
                    if (ctype[r3] == "FA"):
                        full_assoc(csizes[read1], bsizes[r2], wtype[r4],
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
    # outfile = open("mytest1.result", 'w')

    cnt = 0
    te = 9.99
    stringout = ""
    while (cnt < out):
        stringout = str(outcache[cnt]) + " " + str(outblock[cnt]) + " " + str(
            outmap[cnt]) + " " + str(outwrite[cnt]) + " " + str(
                round(outhr[cnt], 2)) + " " + str(outmc[cnt]) + " " + str(
                    outcm[cnt])
        print(stringout)
        cnt = cnt + 1
outfile.write(stringout)
