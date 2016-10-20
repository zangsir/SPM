import pandas as pd
import numpy as np
import random
import matplotlib.pylab as plt
from saxpy import SAX



def euclid_dist(t1,t2):
    return np.sqrt(sum((t1-t2)**2))
    
#objective Functions
#first with euclidean distance
def objectFunction(data,centroids,assignments):
    cum_all=0
    for cluster in range(len(assignments)):
        #print "cluster:",cluster
        cum_all=cum_all+cumDist(data,centroids[cluster],assignments[cluster])
    #print "total objective function value=",cum_all
    return cum_all
    
    
        
def cumDist(data,centroid,assignment):        
    cum_dist=0
    for i in assignment:
        cum_dist=cum_dist+euclid_dist(centroid,data[i])**2
    
    #print 'cum_dist_euclid=',cum_dist
    return cum_dist
        

    
def LB_Keogh(s1,s2,r):
    LB_sum=0
    for ind,i in enumerate(s1):
        
        lower_bound=min(s2[(ind-r if ind-r>=0 else 0):(ind+r)])
        upper_bound=max(s2[(ind-r if ind-r>=0 else 0):(ind+r)])
        
        if i>upper_bound:
            LB_sum=LB_sum+(i-upper_bound)**2
        elif i<lower_bound:
            LB_sum=LB_sum+(i-lower_bound)**2
    
    return np.sqrt(LB_sum)
    

def DTWDistance(s1, s2,w):
    DTW={}
    
    w = max(w, abs(len(s1)-len(s2)))
    
    for i in range(-1,len(s1)):
        for j in range(-1,len(s2)):
            DTW[(i, j)] = float('inf')
    DTW[(-1, -1)] = 0
  
    for i in range(len(s1)):
        for j in range(max(0, i-w), min(len(s2), i+w)):
            dist= (s1[i]-s2[j])**2
            DTW[(i, j)] = dist + min(DTW[(i-1, j)],DTW[(i, j-1)], DTW[(i-1, j-1)])
		
    return np.sqrt(DTW[len(s1)-1, len(s2)-1])
    
    




    

	
	

import random

def k_means_clust_DTW_LBK(data,num_clust,num_iter,w=5):
    centroids=random.sample(data,num_clust)
    counter=0
    old_centroids=None
    cost_log=[]
    for n in range(num_iter):
        
        counter+=1
        #print "iteration",counter
        
        
        if np.array_equal(old_centroids,centroids):
            return centroids, assignments,cost_log
        #else:
            #print "old!=new"
        assignments={}
        #assign data points to clusters
        for ind,i in enumerate(data):
            min_dist=float('inf')
            closest_clust=None
            #here the min_dist is the min_dist to centroid: which centroid is closest to this point?
            for c_ind,j in enumerate(centroids):
                #only if the LB_Keogh distance is smaller than the min_dist, then we compute the DTW distance
                if LB_Keogh(i,j,5)<min_dist:
                    cur_dist=DTWDistance(i,j,w)
                    if cur_dist<min_dist:
                        min_dist=cur_dist
                        closest_clust=c_ind
            if closest_clust in assignments:
                assignments[closest_clust].append(ind)
            else:
                assignments[closest_clust]=[]
                #print "not in:",ind
                
        old_centroids=centroids[:]
        cost=objectFunction(data,centroids,assignments)
        cost_log.append(cost)
        
        
        #recalculate centroids of clusters
        for key in assignments:
            clust_sum=0
            for k in assignments[key]:
                clust_sum=clust_sum+data[k]
            if not np.array_equal(clust_sum,0):
                centroids[key]=[m/len(assignments[key]) for m in clust_sum]
            else:
                centroids=random.sample(data,num_clust)
                break
        
    return centroids, assignments,cost_log
        

#euclidean distance kmeans
def k_means_clust_euclid(data,num_clust,num_iter):
    centroids=random.sample(data,num_clust)
    #print "random init:",centroids
    counter=0
    old_cent=None
    cost_log=[]
    for n in range(num_iter):
        
        counter+=1
        #print "iteration",counter
        #print "old c",old_cent
        #print "new c",centroids
        #print "assignments-begin",assginments
        if np.array_equal(old_cent,centroids):
            return centroids, assignments,cost_log
        #else:
            #print "old!=new"
        old_cent=centroids[:]
        #print "copied old:",old_cent
        #assign data points to clusters
        assignments={}
        for ind,i in enumerate(data):
            #print "ass",assignments
            min_dist=float('inf')
            closest_clust=None
            #here the min_dist is the min_dist to centroid: which centroid is closest to this point?
            for c_ind,j in enumerate(centroids):                
                cur_dist=euclid_dist(i,j)
                if cur_dist<min_dist:
                    min_dist=cur_dist
                    closest_clust=c_ind
            if closest_clust in assignments:
                #print "closest cent:",closest_clust
                assignments[closest_clust].append(ind)
            else:
                #print "no in ass"
                assignments[closest_clust]=[]
                #print "not in:",ind
        # print "assignments", assignments       
        #print "old before new:",old_cent
        
        #print 'centroids',centroids
        cost=objectFunction(data,centroids,assignments)
        
        cost_log.append(cost)
        
        #recalculate centroids of clusters

        for key in assignments:
            clust_sum=0
            for k in assignments[key]:
                clust_sum=clust_sum+data[k]
                #print "clust sum:",clust_sum
            #print "----OLD-before",old_cent
            if not np.array_equal(clust_sum,0):
                #print 'clust sum=',clust_sum
                #centroids[key]=[m/len(assignments[key]) for m in clust_sum]
                centroids[key]=np.array(clust_sum)/len(assignments[key])
                #print "------clust sum !=0"
                #print "----OLD",old_cent
            else:
                centroids=random.sample(data,num_clust)
                #print "------clust sum = 0"
                break
        #print "computed new:",centroids
        #print "old at this point:",old_cent
        #print "============"
    return centroids, assignments, cost_log
    


#mindist distance kmeans
def k_means_clust_mindist(data,num_clust,num_iter,word,alpha):
    
    data_SAX=[]
    s=SAX(word,alpha,0.000001)
    for ts in data:
        #convert i, a time series, into SAX
        (tsString, tsIndices) = s.to_letter_rep(ts)
        data_SAX.append(tsString)
    #print "Data", data_SAX
    
    
    centroids=random.sample(data,num_clust)
    centroids_SAX=[]
    for ts in centroids:
        #convert i, a time series, into SAX
        (tsString, tsIndices) = s.to_letter_rep(ts)
        centroids_SAX.append(tsString)
    #print "cent",centroids_SAX
    
    counter=0
    old_cent=None
    cost_log=[]
    for n in range(num_iter):
        
        counter+=1
        print "iteration",counter

        if np.array_equal(old_cent,centroids):
            print "num of iteration:",n-1
            return centroids, assignments,cost_log
        #else:
            #print "old!=new"
        
        old_cent=centroids[:]
        #print 'old cent',old_cent
        #assign data points to clusters
        assignments={}
        for ind,i in enumerate(data_SAX):
            #print "ass",assignments
            min_dist=float('inf')
            closest_clust=None
            #here the min_dist is the min_dist to centroid: which centroid is closest to this point?
            for c_ind,j in enumerate(centroids_SAX):                
                cur_dist=s.compare_strings(i,j)
                if cur_dist<min_dist:
                    min_dist=cur_dist
                    closest_clust=c_ind
            if closest_clust in assignments:
                assignments[closest_clust].append(ind)
            else:
                assignments[closest_clust]=[]
        #if len(assignments)==num_clust:
         #   cost=objectFunction(data,centroids,assignments)
        #else:
         #   cost=float('inf')
        #cost_log.append(cost)
        #recalculate centroids of clusters
        for key in assignments:
            clust_sum=0
            for k in assignments[key]:
                print clust_sum
                print data[k]
                clust_sum=clust_sum+data[k]
            if not np.array_equal(clust_sum,0):
                centroids[key]=np.array(clust_sum)/len(assignments[key])
            else:
                centroids=random.sample(data,num_clust)
                break
        
        #centroids_SAX=[]
        #for ts in centroids:
            #convert i, a time series, into SAX
         #   (tsString, tsIndices) = s.to_letter_rep(ts)
          #  centroids_SAX.append(tsString)
        #print "cent",centroids_SAX
        #print "new cent",centroids
        #print "old cent end",old_cent
        #print "============"
    return centroids, assignments,cost_log
    
    
    
    

    

def computeAccuracy_cmn(assignments,labels):
    
    #tone_assign=[]
    total_correct=0
    record=[]
    for k in assignments:
        #print k
        #tonex=[]
        a,b,c,d=0,0,0,0
        #print 'k=',k
        #print 'assigned:',assignments[k]
        labs=[labels[i] for i in assignments[k]]
        #print 'labs:',labs

        for idx in assignments[k]:
            #print idx
            if labels[idx][0]==1:
                #print 'case 1'
                #tonex.append(1)
                a+=1
            elif labels[idx][0]==2:
                #print 'case 2'
                #tonex.append(2)
                b+=1
            elif labels[idx][0]==3:
                #print 'case 3'
                #tonex.append(3)
                c+=1
            elif labels[idx][0]==4:
                #print 'case 4'
                #tonex.append(4)
                d+=1
            #else:
                #print 'case 0'
                #tonex.append(0)
             #   e+=1
        #tone_assign.append(tonex)
        l=[a,b,c,d]
        #majority is the tone label with the majority class in this cluster
        majority=l.index(max(l))+1
        #print 'majority:',majority

        if not majority in record:
            record.append(majority)
            num_majority=max(l)
            total_correct=total_correct+num_majority
        else:
            print "duplicated majority class, accuracy too low!!! Exiting..."
            break
    if len(record)==4:
        accuracy=total_correct/len(labels)
        #print "total correct:",total_correct
        #print "accureacy:",accuracy
        return accuracy
    else:
        #print "no accuracy to be computed"
        return 0 
        



