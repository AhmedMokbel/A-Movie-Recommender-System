#importing libraries
import pandas as pd

#import the Data
Data=pd.read_csv('Dataset\IMDB.csv' ,usecols=range(0,27))
Data =Data[['Title','Genre','Director','Actors','Plot']]

#Data cleaning
import re
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

#initialize
corpus=[]
cleaning=[]
key_words=[]
title_list=[]
Number_of_rows=Data['Title'].count()
Number_of_rows=Number_of_rows+1

for index in range (Number_of_rows):
   
    Genre=re.sub('[^a-zA-Z]',' ',str(Data['Genre'][index]))
    Director=re.sub(r"\s+", "",str(Data['Director'][index]))
    Actors=re.sub(r"\s+", "",str(Data['Actors'][index]))
    plot=re.sub('[^a-zA-Z]',' ',str(Data['Plot'][index]))
    title=re.sub('[^a-zA-Z]',' ',str(Data['Title'][index])).lower()
    title_list.append(title)
    corpus.append(Genre+' '+Director+' '+Actors+' '+plot)
    cleaning.append(re.sub("," , " " ,corpus[index]))
    
for index in cleaning:  
    index=index.lower()
    index=index.split()
    ps= PorterStemmer()
    index=[ps.stem(word) for word in index if not word in set(stopwords.words('english'))]
    index=' '.join(index)
    index=str(index)
    key_words.append(index)
    
    
    
    
Data['bag_of_words']=key_words
Data['Title']=title_list
#Drop column plot
Data.drop(columns=['Genre','Director','Actors','Plot'],inplace=True)

#set title index
Data.set_index(keys='Title' ,inplace=True)

#create Model
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
cv=CountVectorizer()
count_matrix=cv.fit_transform(Data['bag_of_words']).toarray()
cosine_sim=cosine_similarity(count_matrix,count_matrix)

#build Movie recommender system

#getting titles
indices=pd.Series(Data.index)

def recommender(title,cosine_sim=cosine_sim ) :
    recommended_Movies=[]
    
    #Getting the title movie
    try:
         idx_title = indices[indices==title].index[0]
    except IndexError:
          return "The movie you entered does not exist...try another one"
      
    score_series = pd.Series(cosine_sim[idx_title]).sort_values(ascending = False)
    
    top_10_Movies = list(score_series.iloc[1:11].index)
    
    for i in top_10_Movies:
        recommended_Movies.append(list(Data.index)[i])
        
    return recommended_Movies
   
#test our system
#recommender("the godfather")



