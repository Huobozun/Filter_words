
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

class filter_en():

    def __init__(self) -> None:
        file = open('/home/zjg/code2/filter_en/word_library_1words.txt', 'r') 
        js = file.read()
        dic = json.loads(js)   
        #print(dic[0]) 
        file.close() 
        self.publibrary=dic
        pass


    def googlefre(self,word):
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

    def pubfre(self,wordlist,word):
        #print(word)
        if word not in self.publibrary:#pubmed词典没有本次，不删
            return 0
        else:
            x=self.publibrary[word]
            ic=1
            for ii0 in range(0,len(wordlist)):
                if(wordlist[ii0]!=word):
                    #print(wordlist[ii0])
                    if wordlist[ii0] not in self.publibrary:#词典没有
                        y=0
                    else:
                        y=self.publibrary[wordlist[ii0]]
                    
                    if(int(x)/(int(y)+1)<10):#加1是避免0不能当被除数
                            ic=0
            
            return ic#返回1说明本次比其他所有词频都大于10倍以上
        

        


    def _filter_en_(self,word):
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
                        xg=self.googlefre(x[i2])#判断想要删掉的词的Google词频，如果词频排位比较靠前，说明经常出现，说明不是专有名词，确实要删
                        if(xg<50000):
                            xgg=self.pubfre(word,x[i2])#判断想要删掉的词是不是在PubMed中比同词条中其他词出现频率大于100倍以上，如是，则确实要删掉
                            if(xgg==1):

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
    print(1)
    x_filter=filter_en()
    print(2)
    for i in range(0,len(Filelist)):
        print(Filelist[i])
        ftitle=get_title('result-type/',Filelist[i])#list里类型为str
        fw=get_content('result-word/',Filelist[i])#list里类型为list
        with open('/home/zjg/code2/filter_en/6(google50000)(pubmed10)/'+Filelist[i],'w',encoding='utf8',newline='')as ff:
            for i1 in range(0,len(fw)):
                fw1=fw[i1]
                x=x_filter._filter_en_(fw1)
                ff.write('%s\t%s\n' %(ftitle[i1],x))

        ff.close()



 
 




