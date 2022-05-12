
import nltk
import os 
import json
import sys
import time
sys.path.append('/home/zjg/code2/')
def get_title(name,file):
    with open('/home/zjg/code2/'+name+file,'r',encoding='utf-8')as ft:
        dataci=[]
        for line in ft:
            dataci.append(line)
        ft.close()
        z=[]
        for ii in range(0,len(dataci)):
            x=dataci[ii]
            y=''
            for i in range(0,8):
                y+=x[i]
            z.append(y)
    return z


def get_content(name,file):
    with open('/home/zjg/code2/'+name+file,'r',encoding='utf-8')as ft:
        dataci=[]
        for line in ft:
            dataci.append(line)
        ft.close()
        z=[]
        for ii in range(0,len(dataci)):
            x=dataci[ii]
            y=''
            for i in range(9,len(x)):
                y+=x[i]
            z.append(eval(y))
    return z

def googlefre(word):
    with open('/home/zjg/code2/filter_en/frequency-all.txt','r',encoding= 'utf-8',errors='ignore')as fr:
        i=0
        for lines in fr:
            i+=1
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
            if(i>50000):
                break
        rnum=int(num)
    fr.close()
    return rnum

def _filter_en_(word):
    l=[]
    for i0 in range(0,len(word)):
        l.append(0)
    x=word
    for i1 in range(0,len(word)):
        for i2 in range(0,len(x)):
            if(x[i2] in word[i1] and i2!=i1):
                p=word[i1].replace(x[i2],'')
                p=p.replace(' ','')
                p=p.replace('(','')
                p=p.replace(')','')
                if(p==''or p=='s' or len(p)<3):
                    continue
                if(nltk.pos_tag([p])[0][1]=='JJ'):#如果缺少的部分是形容词就留下
                    pan=0
                else:
                    pan=0
                    for i3 in range(0,len(x)):
                        if(p.lower() in x[i3].lower() and i3!=i1):#判断缺少的词的出现次数
                            pan+=1
                if(pan>len(word)/2):
                    xg=googlefre(x[i2])#判断想要删掉的词的Google词频，如果词频排位比较靠前，说明经常出现，说明不是专有名词，确实要删
                    if(xg<50000):
                        l[i2]=1
    return l

def get_filelist(dir):#依次遍历.json文件
 
    Filelist = []
 
    for home, dirs, files in os.walk(path):
 
        for filename in files:
 

            # 文件名列表，包含完整路径
            #Filelist.append(os.path.join(home, filename))
            # # 文件名列表，只包含文件名
            Filelist.append( filename)
    return Filelist


if __name__ == "__main__":

    path ='/home/zjg/code2/result-word/'
    Filelist = get_filelist(dir)
    for i in range(7,len(Filelist)):
        print(Filelist[i])
        ftitle=get_title('result-type/',Filelist[i])#list里类型为str
        fw=get_content('result-word/',Filelist[i])#list里类型为list
        with open('/home/zjg/code2/filter_en/4(50000)/'+Filelist[i],'w',encoding='utf8',newline='')as ff:
            for i1 in range(0,len(fw)):
                fw1=fw[i1]
                x=_filter_en_(fw1)
                ff.write('%s\t%s\n' %(ftitle[i1],x))

        ff.close()



 
 




