from os import listdir

boilerplate="""File type = "ooTextFile"
Object class = "TextGrid"

xmin = 0 
xmax = %.3f
tiers? <exists> 
size = 1
item []: 
    item [1]:
        class = "IntervalTier" 
        name = "syllable" 
        xmin = 0
        xmax = %.3f 
        intervals: size = %d""" 

interval="""intervals [%d]:
            xmin = %.3f 
            xmax = %.3f 
            text = %s
            """


def print_txgd(filename):
    output=""
    f=open(filename,'r')
    t=f.read()

    rows=t.split('\n')
    data=[]
    for row in rows:
        if row!='':
            items=row.split(' ')
            data.append(items)

    xmax=data[-1][1]
    interval_size=len(data)
    #print xmax,interval_size,len(data)


    output+= boilerplate %(float(xmax),float(xmax),interval_size)
    for i in range(len(data)):
        row=data[i]
        output+= "        "+interval %(i+1,float(row[0]),float(row[1]),'"'+row[2]+'"')
    return output


def write_file(out_name,content):
    f=open(out_name,'w')
    f.write(content)
    f.close()


path="test/"
onlyfiles = [ f for f in listdir(path) if f.endswith(".phons")]
print onlyfiles
for phons_file in onlyfiles:
    output=print_txgd(path+phons_file)
    outname=path+phons_file.split('.')[0]+".TextGrid"
    write_file(outname,output)



#print_txgd("CHJ000014.phons")
