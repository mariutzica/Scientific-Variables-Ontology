# -*- coding: utf-8 -*-
"""
Created on Fri Aug 12 10:53:39 2016

Last checked on Thurs Jan 19 2017

@author: Maria Stoica
@description: Script for cleaning up the current list of names (for consistency)

Take list of CSN from website and updated v0.85. Pull out the names that are
not in the intersection of the two and figure out if any or all of these names
should be dropped.
"""

################################
#    IMPORT NEEDED PACKAGES    #
################################

#Pandas for data frames and data manipulation
import pandas as pd
# Numpy for unique
import numpy as np

################################
#   INITIAL DATA LOAD          #
################################

# Load CSN list, split up by '__' to yield object and quantity parts.

# List from the website, has 2653 items.
# List from Google Drive folder has 3015 items.
csn = pd.DataFrame(np.unique(pd.read_csv('CSN_VarNames_v0.85b.txt',header=None)))
csn_web = pd.read_csv('CSN_list_website_31052016.txt',header=None)
csn_created = pd.read_csv('CSN_manually_created_01262019.txt',header=None)
csn_created2 = pd.read_csv('CSN_manually_created_03182019.txt',header=None)

# combine to get 3066 unique entries; write to new file to be semantically processed
new_CSN_list = pd.Series(list(set(csn[0]) | set(csn_web[0]) | set(csn_created[0]) | set(csn_created2[0])))
new_CSN_list.to_csv('CSN_VarNames_v0.85m0.csv',index=False)
