#!/usr/bin/python3
#script used to parse CLC outputs and create a count data input for DESeq2

csvfiles = ["Flower_meristem_RB_01.csv", "Flower_meristem_RB_02.csv", "Flower_meristem_RB_03.csv",
            "IAC_control-48h_01.csv", "IAC_control-48h_02.csv", "IAC_control-48h_03.csv",
            "IAC_inoculation-48h_01.csv", "IAC_inoculation-48h_02.csv", "IAC_inoculation-48h_03.csv",
            "SP_Control-48h_01.csv", "SP_Control-48h_02.csv", "SP_Control-48h_03.csv",
            "SP_inoculation-48h_01.csv", "SP_inoculation-48h_02.csv", "SP_inoculation-48h_03.csv",
            "Whip_RB_R1.csv", "Whip_RB_R2.csv", "Whip_RB_R3.csv"]


acronyms={
'Flower_meristem_RB_01.csv':'flmer1',
'Flower_meristem_RB_02.csv':'flmer2',
'Flower_meristem_RB_03.csv':'flmer3',
'IAC_control-48h_01.csv':'iactr1',
'IAC_control-48h_02.csv':'iactr2',
'IAC_control-48h_03.csv':'iactr3',
'IAC_inoculation-48h_01.csv':'iaino1',
'IAC_inoculation-48h_02.csv':'iaino2',
'IAC_inoculation-48h_03.csv':'iaino3',
'SP_Control-48h_01.csv':'spctr1',
'SP_Control-48h_02.csv':'spctr2',
'SP_Control-48h_03.csv':'spctr3',
'SP_inoculation-48h_01.csv':'spino1',
'SP_inoculation-48h_02.csv':'spino2',
'SP_inoculation-48h_03.csv':'spino3',
'Whip_RB_R1.csv':'whipr1',
'Whip_RB_R2.csv':'whipr2',
'Whip_RB_R3.csv':'whipr3'}

refcounts = {} #final dictionary

#first, feed refcounts dict with all the reference sequence headers
for j in csvfiles:
    with open(j,"r") as set1:
        for i in set1:
            i = i.rstrip()
            i = i.split(";")
            if "Name" not in i and "skipped" not in i:
                ref = i[0].replace("\"","")
                if ref not in refcounts:
                    refcounts[ref] = []

#for each of CSV files, create a variable dict (countsfile) with the number of
#reads for each of the reference sequence headers
seqoffiles = []
for j in csvfiles:
    countsfile = {} #dict for file {header: count}
    with open(j,"r") as set1:
        for i in set1:
            i = i.rstrip()
            i = i.split(";")
            if "Name" not in i and "skipped" not in i and "" not in i:
                ref = i[0].replace("\"","")
                u_reads = i[6].replace("\"","")
                countsfile[ref] = u_reads

        #for each reference header in final dict (refcounts), set the number of
        #counts from current file in the last position of list, which is the dict's value
        for jj in refcounts.items():
            if jj[0] not in countsfile: #if file has not reads for the reference header, set 0
                addzero = refcounts[jj[0]]
                addzero.append("0")
                refcounts[jj[0]] = addzero
            else: #if the file has reads for the reference header, set count
                addreads = refcounts[jj[0]]
                addreads.append(countsfile[jj[0]])
                refcounts[jj[0]] = addreads

        seqoffiles.append(acronyms[j]) #create a list of files to address the order they were read

outtable = open("DESeq2input.csv","w") #open output to write

outtable.write(",".join(seqoffiles) + "\n") #write the header of the table with the files in order

for i in refcounts.items(): #write the values for each reference header
    outtable.write(i[0] + "," + ",".join(i[1]) + "\n")

outtable.close() #close the output file
print ("Done!") #print message on terminal
