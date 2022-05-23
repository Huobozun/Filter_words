

#PN词判断，与PN是否毫不相干判断，是否是专有名词的判断&其他地方是否存在该词&是否是完整对应首字母的缩写判断，本词与词条其他词关系判断（‘或’‘从属’‘别称’不删），主要部分判断（大于3词的增加MSH/MTH权重）（包括可缺失字典），Google词频50000，UMLS字典词频差距(仅判断低频词）判断

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

class filter_en():

    def __init__(self) -> None:
        file3 = open(path+'/UMLS_library.txt', 'r') #统计词的个数
        js3 = file3.read()
        dic3 = json.loads(js3)   
        #print(dic[0]) 
        file3.close() 
        self.UMLSlibrary=dic3
        file4 = open(path+'/UMLS_fre_dictionary.txt', 'r') #统计词频
        js4 = file4.read()
        dic4 = json.loads(js4)   
        #print(dic[0]) 
        file4.close() 
        self.UMLSdictionary=dic4
        pass


    def googlefre(self,word):#判断想要删掉的词是否在Google词频中出现频率很高
        with open(path+'/frequency-all.txt','r',encoding= 'utf-8',errors='ignore')as fr:
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
        if(rnum<50000):
            return True
        else:
            return False

        
    def pubfre2(self,wordlist,word,l):#判断想要删掉的词的词频是否显著大于本词条的其他词
        #print(word)
        if word not in self.UMLSdictionary:
            return False
        else:
            x=self.UMLSdictionary[word]
        ic=0
        if(int(x)<10):#词本身词频小于10，不删，影响不大
            ic=0
            return False
        px=0
        py=0
        for ii0 in range(0,len(wordlist)):
            if(wordlist[ii0]!=word and l[ii0]!=1):#仅查找不同词以及尚未删掉词的频率差距
                if wordlist[ii0] not in self.UMLSdictionary:#词典没有
                        y=0
                else:
                    y=self.UMLSdictionary[wordlist[ii0]]
                if(int(x)<int(y)):#只比较比该词频率小的词，频率比该词大的词等到判断他自己的时候才有用
                    continue
                py+=1#统计除去相同词和已删掉的词之外，频率比该词小的词的个数
                if(int(x)<=125):
                    if(int(x)-int(y)>100):
                            px+=1#统计差距很大的词的个数
                else:
                    if(int(x)/(int(y)+1)>5):#如果有词频比x的五分之一大，就说明x的词频不是显著高于其他词，就不删。加1是避免0不能当被除数
                            px+=1 #统计差距很大的词的个数
        if(px==py and py!=0):#所有比该词频率小的词的频率差距都很大
            ic=1  
        if(ic==1):#ic=1说明本次比其他所有词频都大于5倍以上,要删
            return True
        else:
            return False   
        
    def dict_normalword(self,word):#构建可缺失字典
        worddict=['s','es','d','ed','ing','a','an','of','the','ting','syndrome','adult','childhood','location','region','structure','Antigen','Antigens','Lymphocyte','Lymphocytes','[EPC]','[EPC','EPC','[TC]','[TC','TC','[APC]','[APC','APC','[brand name]','[brand name','brand name']
        for s in worddict:
            if(s.lower()==word.lower()):
                return True
        
        return False

    def get_Punctuation(self,testword,goodword):#用来获取如果testword在goodword内部时的前后符号，判断是否含有'/''>''()'，以便于关系判断
        A = ahocorasick.Automaton()
        testword2=[]
        testword2.append(testword)

        for index,word in enumerate(testword2):
            A.add_word(word, (index, word))

        A.make_automaton()

        pp=[]

        #每个文件读取查找
        for item in A.iter(goodword):
            p=[]
            y0=item[0]#比对查找结果
            ih=y0+1
            while(ih<len(goodword) and goodword[ih]==' '):
                ih+=1
            if(ih<len(goodword)):
                p.append(goodword[ih])
            else:
                p.append(goodword[len(goodword)-1])

            iq=y0-len(testword)
            while(iq>-1 and goodword[iq]==' '):
                iq-=1
            if(iq>-1):
                p.append(goodword[iq])
            else:
                p.append(goodword[0])
            
            pp.append(p)
        
        return pp



            
    def judge_relationship(self,testword,wordlist):#判断本词与其他词有没有或，上下级，别称的关系。这类词通常是不用删的
        for i0 in range(0,len(wordlist)):
            if(testword.lower() in wordlist[i0].lower()):#testword短    
                
                p0=wordlist[i0].lower().replace(testword.lower(),'')#获取剩余部分
                if(len(p0)>=1):
                    while(p0[len(p0)-1]==' ' or p0[0]==' '):
                        p0=p0.strip(' ')
                p=p0.strip(string.punctuation)#获取去除边缘标点符号的剩余部分
                
                if self.is_unique(testword)==False :#不是专有名词，再去判断是不是别称关系(避免这种情况'HER-2/neu Peptide Vaccine')
                    #['red clover']	['clover red', 'red clover', 'Trifolium pratense / red clover / meadow honeysuckle', 'Trifolium pratense, flower essence']
                    pp=self.get_Punctuation(testword.lower(),wordlist[i0].lower())
                    for ip in range(0,len(pp)):
                        if(pp[ip][0]==r'/' or pp[ip][1]==r'/'):#前后有/
                            return True
                #上面为testword在goodword内部，下面为testword在goodword边上
                    if(p0.replace(p,'')==r'/'):#缺失部分旁边有个'/'说明是别称关系，不删
                        return True
                pp=self.get_Punctuation(testword.lower(),wordlist[i0].lower())
                for ip in range(0,len(pp)):
                    if(pp[ip][0]==r'>' or pp[ip][1]==r'>'):#前后有>
                        return True
                    if(pp[ip][0]==r'(' and pp[ip][1]==r')'):#要求testword被括号包住
                        return True
                if(p0.replace(p,'')==r'>'):#缺失部分旁边有个'>'说明是从属关系，不删
                    return True
                if(p0.replace(p,'')==r'()'):#缺失部分旁边有个'）'说明是别称关系，不删
                    return True
        return False

    def lack_mainfeature(self,testword,goodword,wordlist,wordres):#判断是否缺少主要部分
        if(testword.lower() in goodword.lower()):#testword短    
            
            """if ('MSH' in wordres) or ('MTH' in wordres):#只判断缺失MTH/MSH部分及占比
                wordupdate=[]
                for i0 in range(0,len(wordlist)):
                    if(wordres[i0]=='MTH' or wordres[i0]=='MSH'):
                        wordupdate.append(wordlist[i0])
                wordlist=wordupdate"""
        
            p0=goodword.lower().replace(testword.lower(),'')
            if(len(p0)>=1):
                while(p0[len(p0)-1]==' ' or p0[0]==' '):
                    p0=p0.strip(' ')
            #p=p.replace(' ','')
            p=p0.strip(string.punctuation)
            xp=p.split(' ')
            
            mwordlist=[]
            for i4 in range(0,len(wordlist)):#汇总MTH/MSH词，将与该词一样的词也增加权重
                if(wordres[i4]=='MTH' or wordres[i4]=='MSH'):
                    mwordlist.append(wordlist[i4].lower())

            end=0
            for i in range(0,len(xp)):#判断缺少部分每个词是不是词条的关键部分，如果其中任何一个词是关键部分，那缺少都是不合理的
                if(xp[i] in testword.lower()):#缺失部分在前面的词里面，就不删
                    continue
                if(len(xp[i])==1):#缺失部分就是一个字母，没有意义去查这个字母是否重要
                    continue
                if self.dict_normalword(xp[i]):#缺少部分在可缺少字典里面，就不删
                    continue
                """if(nltk.pos_tag([p])[0][1]=='JJ'):#如果缺少的部分是形容词就留下
                    continue"""
                pan=0
                for i3 in range(0,len(wordlist)):
                    if(xp[i].lower() in wordlist[i3].lower()):#判断缺少的词的出现次数
                        if(len(wordlist)>3):#3个词以上的词条增加MTH/MSH权重，不然三个词只要缺失MTH/MSH部分必然被删，不合理
                            if(wordres[i3]=='MTH' or wordres[i3]=='MSH' or (wordlist[i3].lower() in mwordlist)):#MTH/MSH词增加权重
                                pan+=0.5
                        pan+=1
                if(pan>=len(wordlist)*0.6):#缺少部分是主要成分，要删
                    end=1
                    break
               
            if(end==1):
                return True
            else:
                return False
        else:
            return False
       
    def is_unique(self,word):#判断像不像是特有名词
        if len(word.split(' '))==1:#长度为一个词
            if word[0].isupper() or any(chr0.isupper() for chr0 in str(word)):#首字母大写/中间有大写
                return True
            if any(chr.isdigit() for chr in str(word)):#包含数字
                return True
               
            return False
        else:
            if word.isupper():#长度大于一个词，但全是大写
                return True

            else:
                return False

    def search_others(self,word,wordlist):#判断其他地方是否也出现这个词
        scount=0
        for iword in wordlist:
            if(word==iword):
                scount+=1
        if(self.UMLSlibrary[word]>scount):#统计词典里面的数目大于本词条，说明该词在其他地方也出现过
            return True
        else:
            return False
    
    def is_abbreviation(self,word,wordlist):#判断专有名词是不是完整对应的缩写，如是不删
        for i0 in range(0,len(wordlist)):
            y=wordlist[i0].split(' ')
            z=''
            for i1 in range(0,len(y)):
                z+=y[i1][0]
            if(word.lower()==z.lower()):
                return True
        
        return False
        

    def compare_words(self,word1,word2):#判断两个词是否相关（是否有重叠部分）
        count=0
        for i in range(0,len(word1)):
            for ii in range(0,len(word2)):
                if(word1[i].lower()==word2[ii].lower()):
                    count+=1
        
        if(count==0):
            return False#两词毫不相关
        else:
            return True#两词有关系
    



    def _filter_en_(self,word,type,resouce):
        l=[]
        for i0 in range(0,len(word)):
            l.append(0)
        x=word
        index_pn=None
        for itype in range(0,len(type)):
            if(type[itype]=='PN'):
                index_pn=itype
        for i1 in range(0,len(word)):
            if(index_pn!=None and(i1==index_pn or word[i1].lower()==word[index_pn].lower())):#PN词不删
                continue
            if self.is_unique(word[i1]):#像是特有名词
                if self.search_others(word[i1],word)==False:#其他地方没有该词汇，该词具有独特性，不删
                    continue
                if self.is_abbreviation(word[i1],word):#是与词条完整对应的缩写，不删
                    continue
           
            if self.judge_relationship(word[i1],word):#与本词条中的其他词是‘或’‘别称’‘从属’关系，不删（['Iris douglasiana / iris', 'Iris douglasiana, flower essence', 'iris flower essence', 'iris']）
                continue
            
            if(index_pn!=None and (word[i1].lower() in word[index_pn].lower())):#存在PN词汇，以PN词汇作为基准;并且想要判断的词与PN有关系时
                if self.lack_mainfeature(word[i1],word[index_pn],word,resouce):#缺少主要成分
                    #if self.search_others(word[i1],word):#如果其他地方存在该词，进行下一步判断；其他地方没有该词，可以不删
                    if(len(word[i1].split(' '))==1):
                        if self.googlefre(word[i1]):#判断想要删掉的词的Google词频，如果词频排位比较靠前，说明经常出现，说明不是专有名词，确实要删
                            l[i1]=1
                        if self.pubfre2(word,word[i1],l):#判断想要删掉的词是不是在PubMed中比同词条中其他词出现频率大于5倍以上，如是，则确实要删掉
                            l[i1]=1
                    else:
                        if self.pubfre2(word,word[i1],l):#判断想要删掉的词是不是在PubMed中比同词条中其他词出现频率大于5倍以上，如是，则确实要删掉
                            l[i1]=1
            else:
                if(index_pn!=None and self.compare_words(word[i1],word[index_pn])==False):#存在PN，但是与PN毫不相关的，一般是正确的。
                    continue
                else:#没有PN词汇，或者有PN词但是与需要判断的词的关系不明朗，对整个词条逐个比较

                    for i2 in range(0,len(word)):
                        if self.lack_mainfeature(word[i1],word[i2],word,resouce):#缺少/多余主要成分
                            #if self.search_others(word[i1],word):#如果其他地方存在该词，进行下一步判断；其他地方没有该词，可以不删
                            if(len(word[i1].split(' '))==1):
                                if self.googlefre(word[i1]):#判断想要删掉的词的Google词频，如果词频排位比较靠前，说明经常出现，说明不是专有名词，确实要删
                                    l[i1]=1
                                    break
                                if self.pubfre2(word,word[i1],l):#判断想要删掉的词是不是在PubMed中比同词条中其他词出现频率大于5倍以上，如是，则确实要删掉
                                    l[i1]=1
                                    break
                            else:
                                if self.pubfre2(word,word[i1],l):#判断想要删掉的词是不是在PubMed中比同词条中其他词出现频率大于5倍以上，如是，则确实要删掉
                                    l[i1]=1
                                    break
                    

        return l




if __name__ == "__main__":

    path1 =path+'/words-word/'
    Filelist=os.listdir(path1)
    print(1)
    x_filter=filter_en()
    print(2)
    for i in range(0,len(Filelist)):
        print(Filelist[i])
        ftitle=get_title('words-type/',Filelist[i])#list里类型为str
        fw=get_content('words-word/',Filelist[i])#list里类型为list
        ft=get_content('words-type/',Filelist[i])#list里类型为list
        fr=get_content('words-resouce/',Filelist[i])#list里类型为list
        with open(path+'/filter_result_marker/'+Filelist[i],'w',encoding='utf8',newline='')as ff:
            for i1 in range(0,len(fw)):
                fw1=fw[i1]
                ft1=ft[i1]
                fr1=fr[i1]
                x=x_filter._filter_en_(fw1,ft1,fr1)
                ff.write('%s\t%s\n' %(ftitle[i1],x))

        ff.close()



 
 




