



#整体展示挑选结果到一个文件里

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

def get_index(name,file):
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

def get_word(name,file):
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
            z.append(y)
    return z

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
    total=0
    totaly=0
    with open('/home/zjg/code2/filter_en/6allshow_filteren.tsv','w',newline='')as fa:
        for i in range(0,len(Filelist)):
            x=0
            y=0
            fa.write('%s\n' %(Filelist[i]))
            ftitle=get_title('result-type/',Filelist[i])#list里类型为str
            ft=get_content('result-type/',Filelist[i])#list里类型为list
            fr=get_content('result-resouce/',Filelist[i])#list里类型为list
            fw=get_content('result-word/',Filelist[i])#list里类型为list
            fl=get_content('filter_en/6(google50000)(pubmed10)/',Filelist[i])#list里类型为list
        
            for i1 in range(0,len(ft)):
                sh=[]
                ft1=ft[i1]
                fr1=fr[i1]
                fw1=fw[i1]
                fl1=fl[i1]
                la=0
                for i2 in range(0,len(fl1)):
                    y+=1
                    totaly+=1
                    if(fl1[i2]==1):
                        la=1
                        sh.append(fw1[i2])
                        x+=1
                        total+=1
                if(la==1):
                    shd=fw1
                    fa.write('%s\t%s\t%s\n' %(ftitle[i1],sh,shd))
                
            print(Filelist[i],x,y)
            fa.write('%s\t%s\t%s\n' %(Filelist[i],x,y))
    
        print('total: ',total,totaly)
        fa.write('%s\t%s\n' %(total,totaly))
    fa.close()
        







 