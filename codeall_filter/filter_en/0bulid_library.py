import os 
import json
import sys
import time
path=os.getcwd()

def getword(path):
    with open(path, 'r', encoding='utf-8') as f:
        data=[]
        title=[]
        for line in f:
                # 读取一行后，末尾一般会有一个\n，所以用strip函数去掉
                line = line.strip('\n').split('\t')  
                #print(line[0])
                #print(line[1])
                #print(line[2])
                #break
                data.append(line[1])
                title.append(line[0])
        #print(data[0])#此时data中的每个元素就是每行的第二列
        #抽出每行的单词
        data1=[]#将每行单词都排起来
        data2=[]#type
        data3=[]#出处
        for i in range(0,len(data)):
            line0=data[i]
            data1.append([])
            data2.append([])
            data3.append([])
            word=''
            j=0
            b=1
            while(j<len(line0)):
                if(b==1 and line0[j]=='#'and line0[j+1]=='#'and line0[j+2]=='#'):
                    data1[i].append(word)
                    j+=3
                    b=2
                    word=''
                    continue
                if(b==2 and line0[j]=='#'and line0[j+1]=='#'and line0[j+2]=='#'):
                    data2[i].append(word)
                    j+=3
                    b=3
                    word=''
                    continue
                if(b==3 and line0[j]==' 'and line0[j+1]=='['and line0[j+2]=='S'and line0[j+3]=='E'and line0[j+4]=='P'and line0[j+5]==']'and line0[j+6]==' '):
                    data3[i].append(word)
                    j+=7
                    b=1
                    word=''
                    continue
                if(b==3 and j==len(line0)-1):
                    word+=line0[j]
                    data3[i].append(word)
                    j=len(line0)
                    b=1
                    word=''
                    continue
                else:
                    word+=line0[j]  
                    j+=1 
    f.close()
    return title,data1,data2,data3 #title是每行的title的list,对应的，data1是每行的英文单词的集合的list,data2是term type，data3是出处




if __name__ == "__main__":

    path1 =path+'/file/'
    Filelist = os.listdir(path1)
    for i in range(0,len(Filelist)):
        print(Filelist[i])
        ftitle,fw,ft,fr=getword(path1+Filelist[i])#list里类型为str

        with open(path+'/words-word/'+Filelist[i],'w',newline='')as fa:
            for i1 in range(0,len(fw)):
                fa.write('%s\t%s\n' %(ftitle[i1],fw[i1]))
        fa.close()

        with open(path+'/words-type/'+Filelist[i],'w',newline='')as fb:
            for i2 in range(0,len(ft)):
                fb.write('%s\t%s\n' %(ftitle[i2],ft[i2]))
        fb.close()
        
        with open(path+'/words-resouce/'+Filelist[i],'w',newline='')as fc:
            for i3 in range(0,len(fr)):
                fc.write('%s\t%s\n' %(ftitle[i3],fr[i3]))
        fc.close()






