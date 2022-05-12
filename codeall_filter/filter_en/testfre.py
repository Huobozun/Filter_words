
def googlefre(word):
    with open('/home/zjg/code2/filter_en/frequency-all.txt','r',encoding= 'utf-8',errors='ignore')as fr:
        #i=0
        for lines in fr:
            num=''
            for i1 in range(0,len(lines)):
                num+=lines[i1]
                if(lines[i1+1]==' '):
                    break
            w=''
            for i1 in range(11,len(lines)):
                w+=lines[i1]
                if(lines[i1+1]==' '):
                    break
            if(w==word):
                #print(num)
                break
        rnum=int(num)
    fr.close()
    return rnum
        #i+=1
        #if(i==20):
            #break

"""
f=open('frequency-all.txt','r',encoding= u'utf-8',errors='ignore')
byt = f.readline(4)

print(byt)"""
x=googlefre('Mild')
print(x)