#!/usr/bin/python3
#script used to parse CLC outputs and create a count data input for DESeq2

csvfiles = ["flowering_meristem_01.csv", "flowering_meristem_02.csv", "flowering_meristem_03.csv",
            "iac_ctr_48h_01.csv", "iac_ctr_48h_02.csv", "iac_ctr_48h_03.csv",
            "iac_inoc_48h_01.csv","iac_inoc_48h_02.csv", "iac_inoc_48h_03.csv",
            "rb_whip_01.csv", "rb_whip_02.csv", "rb_whip_03.csv",
            "sp_ctr_48h_01.csv", "sp_ctr_48h_02.csv", "sp_ctr_48h_03.csv",
            "sp_inoc_48h_01.csv", "sp_inoc_48h_02.csv", "sp_inoc_48h_03.csv"]

refcounts = {} #final dictionary

#first, feed refcounts dict with all the reference sequence headers
for j in csvfiles:
    with open(j,"r") as set1:
        for i in set1:
            i = i.rstrip()
            i = i.split(",")
            if "Name" not in i and "skipped" not in i:
                ref = i[0]
                #u_reads = i[6]
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
            i = i.split(",")
            if "Name" not in i and "skipped" not in i and "" not in i:
                ref = i[0]
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

        seqoffiles.append(j) #create a list of files to address the order they were read

outtable = open("DESeq2input.csv","w") #open output to write

outtable.write("reference," + ",".join(seqoffiles) + "\n") #write the header of the table with the files in order

for i in refcounts.items(): #write the values for each reference header
    outtable.write(i[0] + "," + ",".join(i[1]) + "\n")

outtable.close() #close the output file
print ("Done!") #print message on terminal
