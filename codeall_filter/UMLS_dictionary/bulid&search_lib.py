import os
import json

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

def get_fre(name,file):
    with open(path+'/'+name+file,'r',encoding='utf-8')as ft:
        dataci=[]
        for line in ft:
            dataci.append(line)
        ft.close()
        z=[]
        for ii in range(0,len(dataci)):
            x=dataci[ii]
            y=''
            for i in range(0,len(x)):
                y+=x[i]
            z.append(eval(y))
    return z



class bulid_UMLSdict():
    def __init__(self) -> None:
        self.UMLSdict=dict()
        pass

    def buliddict(self):
        path1=path+'/words-word'
        Filelist=os.listdir(path1)
        for i0 in range(0,len(Filelist)):
            #ftitle=get_title('result-type/',Filelist[i0])#list里类型为str
            fw=get_content('words-word/',Filelist[i0])#list里类型为list
            for i1 in range(0,len(fw)):
                fw1=fw[i1]
                for i2 in range(0,len(fw1)):
                    if fw1[i2] not in self.UMLSdict:
                        self.UMLSdict[fw1[i2]]=0
                    self.UMLSdict[fw1[i2]]+=1
        
        js = json.dumps(self.UMLSdict)   
        file = open(path+'/UMLS_library.txt', 'w')  
        file.write(js)  
        file.close()

        
    def readindict(self):
        file1 = open(path+'/UMLS_library.txt', 'r') 
        js1 = file1.read()
        dic1 = json.loads(js1)   
        #print(dic[0]) 
        file1.close() 
        self.UMLSdict=dic1


if __name__=='__main__':
    x=bulid_UMLSdict()
    x.readindict()
    p=1
    print('开始进行单个词的查找（输入"O"结束查找')
    while(p!='O'):
        print('请输入你想要查找的词:')
        p=input()
        if(p=='O'):
            break
        if p not in x.UMLSdict:
            print('NONE')
        else:
            print(x.UMLSdict[p])



