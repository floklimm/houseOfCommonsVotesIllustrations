#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""


@author: Florian Klimm
"""

import pandas as pd
import numpy as np
import json # for writing the json


outputJSONFileName='./../html/voteFileApril1.json'

# 0) Functions we need later
def readVoteFile( filename ):
    voteData = pd.read_csv(filename, header=6)  # load the raw data file 
    voteData =  voteData.drop(['Proxy Member'],axis='columns') # remove the unneeded column
    listOfAye = voteData.loc[voteData['Vote'] == 'Aye' ] # get everybody voting Aye
    return listOfAye

# 1) get the data for all eight votes
vote1 = readVoteFile("./../rawData/Division655.csv")
vote2 = readVoteFile("./../rawData/Division656.csv")
vote3 = readVoteFile("./../rawData/Division657.csv")
vote4 = readVoteFile("./../rawData/Division658.csv")
#vote5 = readVoteFile("./../rawData/Division659.csv")
#vote6 = readVoteFile("./../rawData/Division660.csv")
#vote7 = readVoteFile("./../rawData/Division661.csv")
#vote8 = readVoteFile("./../rawData/Division662.csv")


# 2) construct a bipartite network from this data
# a) First, all members as an index
allMembers= pd.concat([vote1, vote2, vote3, vote4,vote5,vote6,vote7,vote8]).drop_duplicates(subset=['Member']).drop(['Vote'],axis='columns')

uniqueParties = allMembers['Party'].unique().tolist()

node_list = [] # an emtpty node list
# iterate over all members
for index, row in allMembers.iterrows():
    node_dict = {} # create an empty dictionary for this node
    node_dict["id"] = "M" + str(index) # index for this member
    node_dict["party"] = row["Party"] # party membership 
    node_dict["group"] = uniqueParties.index(row["Party"]) # party membership as an itneger
    node_dict["name"] = row["Member"]
    node_dict["constituency"] = row["Constituency"]
    
    node_list.append(node_dict) # add it to the dictionary



# add nodes for the votes and construct links to all aye voters
link_list = [] # empty link list

for i in range(1,9):
    # first, construct the node for this vote
    node_dict = {} # create an empty dictionary for this node
    node_dict["id"] = "V" + str(i) # index for this vote
    
    # an ugly if section to define the names of the votes
    if i==1:
        node_dict["name"] = "Motion C"
        node_dict["constituency"] = 'Customs Union'
    elif i==2:
        node_dict["name"] = "Motion D"
        node_dict["constituency"] = 'Common market 2.0'
    elif i==3:
        node_dict["name"] = "Motion E"
        node_dict["constituency"] = 'Confirmatory Public Vote'
    elif i==4:
        node_dict["name"] = "Motion G"
        node_dict["constituency"] = 'Parliamentary Supremacy'
#    elif i==5:
#        node_dict["name"] = "Motion K"
#        node_dict["constituency"] = 'Labour&#39;s alternative plan'
#    elif i==6:
#        node_dict["name"] = "Motion L"
#        node_dict["constituency"] = 'Revocation to avoid no deal'    
#    elif i==7:
#        node_dict["name"] = "Motion M"
#        node_dict["constituency"] = 'Confirmatory public vote'  
#    elif i==8:
#        node_dict["name"] = "Motion O"
#        node_dict["constituency"] = 'Contingent preferential arrangements'  
    else:
       node_dict["name"] = "Vote" + str(i)
       
       node_dict["constituency"] = ''
    
    node_dict["group"] = 9  # the votes get group nine
    node_dict["party"] = "VOTE" # no party memebrship
    
    node_list.append(node_dict) # add it to the dictionary
    
  
    voteFileInterested = globals()["vote" + str(i)] 
    
    
    # second, construct the edges
    for index, row in voteFileInterested.iterrows(): 
        link_dict = {} # empty dictionary for this edge
        link_dict["source"] = "M" + str(index) # attached to this member voting Aye
        link_dict["target"] = "V" + str(i) # index for this vote
        link_list.append(link_dict)    # save it into the list


# allMembers.index[allMembers['Member'] == 'Sammy Wilson'].tolist()[0]

# write into dictionary
graph_dict = {"nodes" : node_list, "links" : link_list}
with open(outputJSONFileName, 'w') as f:
       json.dump(graph_dict, f)