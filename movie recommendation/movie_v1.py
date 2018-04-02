import pandas as pd
from scipy.spatial.distance import cosine
from collections import OrderedDict #for sort key
import operator
movie_id_unseen=6

u_cols = ['user_id', 'age', 'sex', 'occupation', 'zip_code']
users = pd.read_csv('H:\\01_self study_\
flash drive\\AAAschulich\\beyond_schulich\\practice\\2018\\udemy_hadoop\\2018_python3_\
study\\movie_2018\\ml-100k\\u.user', sep='|', names=u_cols,encoding='latin-1')
#print (type(users),"shape is: ",users.shape)


r_cols=['user_id','item_id','rating','time_stamp']
ratings=pd.read_csv('H:\\01_self study_\
flash drive\\AAAschulich\\beyond_schulich\\practice\\2018\\udemy_hadoop\\2018\
_python3_study\\movie_2018\\ml-100k\\u.data', sep='\t', names=r_cols,encoding='latin-1')


#print (type(ratings),ratings.shape)
#print (ratings.head())

i_cols=['item_id','item_title','release_date','video_release_date','imdb_url',
'unknown','action','adventure','animi','children','comedy','crime','documen','drama',
'fantasy','film-noir','horror','musical','myestery','romance','sci-fic','thriller',
'war','western']
items=pd.read_csv('H:\\01_self study_flash drive\\AAAschulich\\beyond_schulich\\practice\\2018\\udemy_hadoop\\2018_\
python3_study\\movie_2018\\ml-100k\\u.item', sep='|', names=i_cols,encoding='latin-1')
#print (items.head())
'''
# merge data sets
user_rating=users.merge(ratings,left_on='user_id',right_on='user_id',how='inner')

user_rating_item=user_rating.merge(items,left_on='item_id',right_on='item_id',
how='inner')
#print(user_rating_item.head())

# group by item_title
print(user_rating_item.groupby("item_title").size().head())
'''
#user ratings for each movie:
#u_r=(ratings.loc[ratings['item_id']==242])[['user_id','rating']]

#use item_u_r class to find similarity between two items.
class item_simi(object):
    def __init__(self, item_no1,item_no2): 
        self.item_no1, self.item_no2=item_no1, item_no2
    def simi(self):
        df1=(ratings.loc[ratings['item_id']==self.item_no1])[['user_id','rating']]
        df2=(ratings.loc[ratings['item_id']==self.item_no2])[['user_id','rating']]
        df3=df1.merge(df2,left_on='user_id',right_on='user_id',how='inner')
        df4=df3[['rating_x']].values.tolist()
        df5=df3[['rating_y']].values.tolist()
        return 1-cosine(df4,df5)
        
c=item_simi(242,302)
#print ("similarity between movie %g and %g is: %g" %(c.item_no1,c.item_no2 , c.simi())) 

     
  
# class for returning any item's most similar items order from high to low
class item_simi_list(object):
    def __init__(self,item_no):
        self.item_no=item_no
    def simi_list(self):
        x=items[['item_id']].values.tolist()
        
        dic_simi={}
        for i in range(0,len(x)-1):
            c=item_simi(self.item_no,x[i][0])
            #list.append(c.simi())
            #temp=x[i][0]
            dic_simi[str(x[i][0])]=c.simi()
        simi2=sorted(dic_simi.items(), key=operator.itemgetter(1),reverse=True)
        y=[]
        for pair in simi2:
            if pair[1]!="nan":
               y.append(pair)
        # top 40 similar movies 
        return y[0:40]

        
#b=item_simi_list(242) 
#print(b.simi_list())

#class for finding a user's top rating movies and finding a user's not rated movie ids.
class user_rateinfo(object):
    global movie_id_unseen
    def __init__(self, user_id):
        self.user_id=user_id
    def user_toprate(self):
        out=ratings.loc[ratings['user_id']==self.user_id].sort_values\
        (by=['rating'],ascending=False).head(n=10)
        return out
    def user_unseen(self):
        rated=ratings.loc[ratings['user_id']==self.user_id]['item_id'].values.tolist()
        norate_out=list(set(ratings['item_id'].values.tolist())-set(rated))
        return norate_out
        #item_simi_list(norate_out[0]).simi_list()
    def user_unseen_rate(self,movie_id_unseen):
        rated_movid=ratings.loc[ratings['user_id']==self.user_id]['item_id'].values.tolist()
        rated_rate=ratings.loc[ratings['user_id']==self.user_id]['rating'].values.tolist()
        #get from item_simi_list only rated by self.user_id 
        #check 6th movie with user 196!
        simi_list2=item_simi_list(movie_id_unseen).simi_list()
        simi_list3=[];i=-1
       
        for pair in simi_list2:
            i=i+1
            if int(pair[0]) in rated_movid:
               #simi_list3 is a list combination of [movie_id, similarity, rating]
               #movie_id is similar movie to Z, similarity is cosine score.
               simi_list3.append([int(pair[0]),round(float(pair[1]),2),rated_rate[i]])
        #calculate new ratings using historical ratings:
        denominator=0;numerator=0
        for id_simi_rate in simi_list3:
            denominator=denominator+id_simi_rate[1]
            numerator=numerator+id_simi_rate[1]*id_simi_rate[2]
        if denominator==0:  
           new_rate="NA"
        else:
            new_rate=round(numerator/denominator,2)
            simi_list3.append(new_rate)
        simi_list4=[movie_id_unseen]
        for item in simi_list3:
            simi_list4.append(item)
        return simi_list4
        
    def user_unseen_all(self):              
        simi_list5=[]
        norate_out2=user_test.user_unseen()
        for i in [6,7,9,10,11,12,14,15,16,17,18,19,20]:
            test_empty=user_test.user_unseen_rate(i)
            if len(test_empty)!=1:              
                simi_list5.append(test_empty)
        
        #exchange col2 with last col(estimated rating) in order to sort by estimated_rating
        for i in simi_list5:
            length=len(i)
            i[1],i[length-1]=i[length-1],i[1]
        simi_list5.sort(key=lambda x: x[1],reverse=True)
        return simi_list5
user_id_test=196        
user_test=user_rateinfo(user_id_test)
print("user %g 's top rated movies:" %(user_id_test))
print(user_test.user_toprate())
print("user %g 's unseen movies:" %(user_id_test))
print(user_test.user_unseen())
#print("user %g 's estimate rating for movie %g is: " %(user_id_test,movie_id_unseen))
#print(user_test.user_unseen_rate(movie_id_unseen))
print(user_test.user_unseen_all())