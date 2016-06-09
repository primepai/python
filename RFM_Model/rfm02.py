# this is a customer segmentation program using RFM model. 
# please note: for import file, must have exactly 3 columns; 1st col must be recency in days, 2nd col
# must be customer id, 3rd col must be amount of purchase; Also, first row must be titles of 
# these 3 variables. 
import csv
import numpy as np
import time
import matplotlib.pyplot as plt
import copy

from collections import Counter
# read csv file.
start_time=time.time()
recency=[]
c_id=[]
amount=[]
with open('rfm08.csv','rb') as f:
    readcsv=csv.reader(f,delimiter=',')
# append csv value to list 
    for row in readcsv:
        recency.append(row[0])
        c_id.append(row[1])
        amount.append(row[2])
    f.close()    
# delete the first element
    del recency[0]
    del c_id[0]
    del amount[0]
# change string to int in array form.    
recency_array=np.array(map(int,recency))
c_id_array=np.array(c_id)
c_id_list=sorted(list(set(c_id_array)))
c_num=len(set(c_id))
c_id_list_row=[]
for t in range(0,c_num):
    c_id_list_row.append(t)


c_id_list2=np.column_stack((c_id_list_row,c_id_list))  
amount_array=np.array(map(float,amount))

# create a matrix containing c_id recency amount value. 
matrix01=np.column_stack((c_id_array,recency_array,amount_array))


# extract a column in a matrix
def column(matrix,i):
    return [row[i] for row in matrix]

# find recency for c_id in c_id_list

c_id_row=[j for j, k in enumerate(column(matrix01,0)) if k==c_id_list[0]]

matrix02=np.zeros((c_num,4))  # matrix02 is the final n by 4 matrix used for classification

# append columns of final summary matrix : matrix02.
for n in range(0,c_num):
    c_id_row=[j for j, k in enumerate(column(matrix01,0)) if k==c_id_list[n]]
    min_list=[]
    thesum=0
    for m in c_id_row:
        min_list.append(matrix01[m][1])
        thesum=thesum+(map(float,column(matrix01,2)))[m]
    min_recency=min(map(int,min_list))
    #append firt col: c_id number
    matrix02[n][0]=int(c_id_list2.tolist()[n][0])  
    #append second col: recency
    matrix02[n][1]=min_recency
    #append third col:frequency
    matrix02[n][2]=column(matrix01,0).count(column(c_id_list2,1)[n])
    matrix02[n][3]=round(thesum,0)
list_add_score_col=np.zeros((c_num,4))
matrix02=np.column_stack((matrix02,list_add_score_col))   
matrix03=map(list,matrix02)



# find the percentile of r, f, m. 
# percentilefind() function is a function returns a list of percentile from 5% to 100%
def percentilefind(list):
    per_list=[]
    for h in range(5,105,5):
        tmp=round(float(np.percentile(list,h)),1)
        per_list.append(tmp)
    return per_list

zz=percentilefind(map(float,column(matrix01,1)))

list_r=map(float,column(matrix03,1))
list_f=map(float,column(matrix03,2))
list_a=map(float,column(matrix03,3))
# note: 33% percentile is [5], 50% percentile is [9], 66% percentile is [12] 

r1=percentilefind(list_r)[5]
r2=percentilefind(list_r)[12]
f1=percentilefind(list_f)[5]
f2=percentilefind(list_f)[12]
a1=percentilefind(list_a)[5]
a2=percentilefind(list_a)[12]
check=[]
check.extend([r1,r2,f1,f2,a1,a2])
# calc r, f, m score for each c_id in matrix03, then append to column 4,5,6,7 of matrix03
for g in range(0,len(matrix03)):
  for z in range(0,3):
      if matrix03[g][z+1]<check[2*z]:
         matrix03[g][z+4]=1
      elif matrix03[g][z+1]<check[2*z+1]:
         matrix03[g][z+4]=2
      else:
         matrix03[g][z+4]=3
  # calc score rating of each customer
  matrix03[g][7]=(4-matrix03[g][4])*100+matrix03[g][5]*10+matrix03[g][6]
# matrix04 get rid of individual score for r, f, m but only keep total score rating. 
matrix04=map(list,(np.array(matrix03))[:,[0,1,2,3,7]])

#score=map(int,sorted(list(set(column(matrix04,4))),reverse=1))
score=map(int,sorted(list(set(column(matrix04,4)))))
score_to_count=map(list,(np.array(matrix03))[:,[7]])
score_count_result=[0]*len(score)
u=0
#count each score rating frequency
for num in score: 
    score_count_result[u]=score_to_count.count([num])
    u=u+1
score_to_count2=[]
for shu in score_to_count:
    score_to_count2.append(shu[0]) 

score2=[]
for x in range(1,len(score)+1):
    score2.append(x)
    

print ("time used: %r seconds") %round(time.time()-start_time,1)
print ("No. of transaction analyzed: %r ") %(len(matrix01))
print ("No. of customer analyzed: %r ") %(c_num)


max_score=max(score_count_result)

plt.ylim(0, max_score*1.2)

plt.bar(score2,score_count_result,color='pink')

if len(score)>18:
    for v in score2:
        plt.text(v+0.002*max_score, score_count_result[v-1]+0.03*max_score, score[v-1], fontsize=11,color='blue')
else:
    for v in score2:
        plt.text(v+0.002*max_score, score_count_result[v-1]+0.03*max_score, score[v-1], fontsize=13,color='blue')   

        # find top 3 category customer segmentation, use sorted(a, key=labmda test: test[0]) function.
score_count_result2=np.column_stack((score_count_result,range(0,len(score_count_result))))
score_count_result2=sorted(score_count_result2,key=lambda test: test[0],reverse=1)
ranks=['1st','2nd','3rd','4th','5th','6th','7th','8th','9th','10th']
for i2 in range(0,5):
    plt.text(score_count_result2[i2][1]+1+0.002*max_score,score_count_result2[i2][0]+0.09*max_score,ranks[i2],fontsize=13,color='green')
  
plt.title('RFM Customer Segmentation  (No. of customer : ' + str(c_num)+' )')
plt.xlabel('RFM Type', fontsize=13)
plt.ylabel('Frequency', fontsize=13)
plt.show()
#analyzing customers by segmentation
churn=[133,132,123] #high value customer who are likely to leave if we do nothing.
upsell=[332,322,232]# mid-value customers we need to up-sell.
best=[333,323,233]  # '333' '323' '233' type customers.
customer_churn=[]
customer_upsell=[]
customer_best=[]
matrix05=copy.deepcopy(matrix04)
for i3 in matrix05:
    if int(i3[4]) in churn:
       customer_churn.append(i3)
    elif int(i3[4]) in upsell:
       customer_upsell.append(i3)
    elif int(i3[4]) in best:
       customer_best.append(i3)

# add customer id to each customer segmentation     
def customer_add_id(lista):
    listb=lista
    for i4 in listb:
        i4.extend([c_id_list2[i4[0]][1]])
    order=np.argsort([1,3,4,5,2,0])
    listc=[]
    listd=[]
    listc=np.array(listb)
    if lista==[]:
       listd=listc
    else:
        listd=listc[:,order]    
    return listd

file_name=['customer_churn.csv','customer_upsell.csv','customer_best.csv'] 

# output customer segmentation to csv. 
for i5 in file_name:
    with open(i5, "w") as output:
        writer = csv.writer(output, lineterminator='\n')
        if i5=='customer_churn.csv':
            writer.writerows(customer_add_id(customer_churn))        
        elif i5=='customer_upsell.csv':
            writer.writerows(customer_add_id(customer_upsell))
        elif i5=='customer_best.csv':
            writer.writerows(customer_add_id(customer_best))
  
    
 

 
    
