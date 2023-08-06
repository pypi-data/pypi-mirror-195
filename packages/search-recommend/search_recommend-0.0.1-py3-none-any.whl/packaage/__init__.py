import pandas as pd
import numpy as np
from annoy import AnnoyIndex
from sklearn.feature_extraction.text import TfidfVectorizer
import warnings
warnings.filterwarnings('ignore')


class Search_Recommend:
    __name=None
    __df=None
    def __init__(self,l,path):
        self.__lst=l
        self.__tfidf=TfidfVectorizer()
        self.__q=self.__dt()
        self.__path=path

    def __data(self,lst):
        y=[]
        for i in self.__lst:
            x=[]
            y.append(x)
            for j in range(1,len(i)+2):
                #print(i[:j])
                x.append(i[:j])
        return y        
    
    def __dt(self):
        Search_Recommend.__df=pd.DataFrame()
        for i in self.__data(self.__lst):
            Search_Recommend.__df=Search_Recommend.__df.append(pd.DataFrame({"col2":i[:-1],"col1":i[-1]}))
        Search_Recommend.__df.reset_index(drop=True,inplace=True)
        Search_Recommend.__df['col2']=Search_Recommend.__df['col2'].apply(lambda x:x.lower())
        return self.__tfidf.fit_transform(Search_Recommend.__df['col2']).toarray()
    
    def create_and_save_model(self,name,trees=1):
            Search_Recommend.__name=name
            #print(Search_Recommend.__name)
            f = self.__q[0].shape[0]
            t = AnnoyIndex(f, 'angular')
            for i,v in enumerate(self.__q):
                t.add_item(i, v)
            t.build(trees)
            t.save(self.__path+f'/{Search_Recommend.__name}.ann')

    def recommend(self,symp):
            symp=symp.lower()
            arr=self.__tfidf.transform([symp]).toarray().reshape(-1,1)
            f = self.__q[0].shape[0]
            t = AnnoyIndex(f, 'angular')
            t.load(self.__path+f'/{Search_Recommend.__name}.ann') # super fast, will just mmap the file
            re=t.get_nns_by_vector(arr,n=10,search_k=self.__q[0].shape[0],include_distances=True)
            return [ (my_idx:=re[0][i], Search_Recommend.__df.iloc[my_idx]["col1"])[1] for i,v in enumerate(re[1]) if v<1.4142135381698608 ]


#python setup.py bdist_wheel
#twine upload --repository-url https://test.pypi.org/legacy/ dist/*
#usnm=neeraj03
#pas=03@neeraj_joshi
#radshoroud333
#twine upload dist/*