0.这是一个过滤词条中不符合本词条内容的过程  
1.首先，你需要在文件夹路径下建立'words-word''words-type''words-resouce'三个文件来运行过滤程序。也可以在文件路径下用'file'文件夹存储字典原内容，然后运行'0bulid_library.py'来生成上述三个文件夹。  
2.文件也需要'frequency-all.txt'谷歌1-gram词频库，'UMLS_fre_dictionary.txt'UMLS的PUBMED词频库，'UMLS_library.txt'UMLS词条出现次数统计。  
3.'words-word''words-type''words-resouce'分别保存了词条、词条类型、词条来源，过滤程序需要根据这三个文件夹进行。当这三个文件夹准备就绪，就可以运行过滤文件'1_filter_en.py'了。  
4.'1_filter_en.py'运行结果是生成一个'filter_result_marker'文件夹，这里面记录了过滤结果，其中标‘1’的表示要被过滤的词，标‘0’表示保留的词  
5.'2show_filteringword_total.py'是展示过滤效果的文件，仅仅摘出过滤掉的词条，让你判断过滤效果  
6.'3get_newUMLS.py'是将最后过滤结果再以原UMLS字典的形式存储的运行文件  