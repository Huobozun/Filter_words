


import nltk
import os 
import json
import sys
import string
import time
import ahocorasick

path=os.getcwd()


def get_title(name,file):
        with open(path+'/'+name+file,'r',encoding='utf-8')as ft:
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
    with open(path+'/'+name+file,'r',encoding='utf-8')as ft:
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









if __name__=='__main__':
    path1 =path+'/words-word/'
    Filelist=os.listdir(path1)
    for i0 in range(0,len(Filelist)):
        print(Filelist[i0])
        ftitle=get_title('words-type/',Filelist[i0])#list里类型为str
        fw=get_content('words-word/',Filelist[i0])#list里类型为list
        ft=get_content('words-type/',Filelist[i0])#list里类型为list
        fr=get_content('words-resouce/',Filelist[i0])#list里类型为list
        fm=get_content('filter_result_marker/',Filelist[i0].replace('zh-',''))#list里类型为list
        with open(path+'/filter_en_result/Filtered_'+Filelist[i0],'w',encoding='utf-8',newline='')as ff:
            x=0
            for i1 in range(0,len(fm)):
                fw1=fw[i1]
                ft1=ft[i1]
                fr1=fr[i1]
                fm1=fm[i1]
                ib=0
                fword=''
                for i2 in range(0,len(fm1)):
                    if ib==1 and fm1[i2]==0:
                        fword+=' [SEP] '
                    if fm1[i2]==0 :
                        ib=1
                        fword+=fw1[i2]+'###'+ft1[i2]+'###'+fr1[i2]
                    else:
                        x+=1
                ff.write('%s\t%s\n' %(ftitle[i1],fword))
        ff.close()
        print(x)

                


                    




