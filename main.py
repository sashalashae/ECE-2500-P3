'''
Sasha Morgan
ECE 2500
Cache Compiler
'''
#from _future_ import division
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
# def full_assoc(caches, blocks, wp, cachep):

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
                    if (ctype[r3] == "DM"):
                        direct_mapped(csizes[read1], bsizes[r2], wtype[r4],
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
    #stringout = ""
    while (cnt < out):

        stringout = str(outcache[cnt]) + " " + str(outblock[cnt]) + " " + str(
            outmap[cnt]) + " " + str(outwrite[cnt]) + " " + str(
                round(outhr[cnt], 2)) + " " + str(outmc[cnt]) + " " + str(
                    outcm[cnt])

        print(stringout)
        cnt = cnt + 1
        #outfile.write(stringout)
