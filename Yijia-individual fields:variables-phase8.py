# import modules 
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import cm
get_ipython().run_line_magic('matplotlib', 'inline')

#Convert two Excel files into CSV files, uploading to notebook and loading the files.
CCDate_2021_Data = pd.read_csv("CCDate2018-2021-3-8.csv")
CMC_2021_Data = pd.read_csv("CustomerMedicalConditions04Nov21.csv")

# Delete data other than 'user' in 'Role'
Role_notUser_list=[]
for x in range(len(CCDate_2021_Data.index)):
    if CCDate_2021_Data.iloc[x,2] !='User':
#         print(CCDate_2021_Data.iloc[x,2])
        Role_notUser_list.append(x)
# print(Role_notUser_list)
CCDate_2021_Data_ClRole=CCDate_2021_Data.drop(Role_notUser_list)
print('done')
CCDate_2021_Data_ClRole

#Delete 'NULL' in 'ExternalID'
CCDate_2021_Data_ClRole_ClEx = CCDate_2021_Data_ClRole.dropna(axis = 0, subset = ['ExternalID'])
print('done')
CCDate_2021_Data_ClRole_ClEx

# I find that some 'External ID' have several rows
ID_counts = CMC_2021_Data['ExternalID'].value_counts()
print(ID_counts)

# Delete duplicate data in 'External ID'
CMC_2021_Data_OnlyID = CMC_2021_Data.drop_duplicates(['ExternalID'])
CMC_2021_Data_OnlyID

# inner merge CCDate_2021_Data_ClRole_ClEx and CMC_2021_Data_OnlyID
CCDate_CMC_2021_inner = pd.merge(CCDate_2021_Data_ClRole_ClEx, CMC_2021_Data_OnlyID, on='ExternalID', how='inner')
print('done')
CCDate_CMC_2021_inner

# Age distribution
pic = plt.figure(figsize=(10,5),dpi=80) 
fig1 = pic.add_subplot(1,2,1)
age_displot = sns.distplot(CMC_2021_Data_OnlyID['Age'])
age_displot.set_title('Age distribution plot')
fig2 = pic.add_subplot(1,2,2)
age_boxplot = sns.boxplot(CMC_2021_Data_OnlyID['Age'])
age_boxplot.set_title('Age box plot')
plt.show()

# Method of showing both values and percentages in a pie chart
def make_autopct(values):
    def my_autopct(pct):
        total = sum(values)
        val = int(round(pct*total/100.0))
        return '{p:.2f}%  ({v:d})'.format(p=pct,v=val)
    return my_autopct


# Gender distribution
pic = plt.figure(figsize=(7,7),dpi=80)
gender_counts = CMC_2021_Data_OnlyID['Gender'].value_counts()
plt.pie(gender_counts, labels = gender_counts.index, startangle = 90, counterclock = False, autopct=make_autopct(gender_counts));
plt.show()

# CareSysCondition distributon
pic = plt.figure(figsize=(7,7),dpi=80)
CSC_counts = CMC_2021_Data_OnlyID['CareSysCondition'].value_counts()
plt.pie(CSC_counts, labels = CSC_counts.index, startangle = 90, counterclock = False, autopct=make_autopct(CSC_counts));
plt.show()

# StaffPlanConditions distributon
pic = plt.figure(figsize=(7,7),dpi=80)
SPC_counts = CMC_2021_Data['StaffPlanConditions'].value_counts()
SPC_counts_clean=SPC_counts[SPC_counts>3] #Too small data filtered out, too small data not clearly displayed in the pie chart
plt.pie(SPC_counts_clean, labels = SPC_counts_clean.index, startangle = 90, counterclock = False, autopct=make_autopct(SPC_counts_clean));
plt.show()
# print(SPC_counts)

# Usage of each ExternalID 
pic = plt.figure(figsize=(7,7),dpi=80)
ExternalID_counts = CCDate_2021_Data_ClRole_ClEx['ExternalID'].value_counts()
plt.pie(ExternalID_counts, labels = ExternalID_counts.index, startangle = 90, counterclock = False, autopct=make_autopct(ExternalID_counts));
plt.show()

# LinkType Distribution
pic = plt.figure(figsize=(5,5),dpi=80)
LinkType_counts = CCDate_2021_Data_ClRole_ClEx['LinkType'].value_counts()
plt.pie(LinkType_counts, labels = LinkType_counts.index, startangle = 90, counterclock = False, autopct=make_autopct(LinkType_counts));
plt.show()
print(LinkType_counts)

# LinkTitle Distribution
pic = plt.figure(figsize=(7,7),dpi=80) 
LinkTitle_counts = CCDate_2021_Data_ClRole_ClEx['LinkTitle'].value_counts()
a=LinkTitle_counts[LinkTitle_counts>1000] # Cleaning out too small data
plt.pie(a, labels = a.index, startangle = 90, counterclock = False, autopct=make_autopct(a))
plt.show()

# Location Distribution
pic = plt.figure(figsize=(7,7),dpi=80) 
Location_counts = CCDate_2021_Data_ClRole_ClEx['Location'].value_counts()
plt.pie(Location_counts, labels = Location_counts.index, startangle = 90, counterclock = False, autopct=make_autopct(Location_counts));
plt.show()

# Relationships between Variables Analysed

# 1. Usage amount per month**    
# Usage amount per month
pic = plt.figure(figsize=(10,6),dpi=80) 

Usage_amount_data_list = []
Usage_amount_month_list = []

# Identify the month and generate the dataset by identifying the beginning of the Time list string
for x in range(3, 12): 
    Usage_amount_data_list.append(len(CCDate_2021_Data_ClRole_ClEx[CCDate_2021_Data_ClRole_ClEx['Time'].str.startswith(str(x))]))
    Usage_amount_month_list.append(x)

plt.bar(range(len(Usage_amount_data_list)), Usage_amount_data_list, tick_label = Usage_amount_month_list)

plt.xlabel("Month (2021)")  # Set X-axis Y-axis name  
plt.ylabel("Usage amount") 

for a,b in zip(range(len(Usage_amount_data_list)),Usage_amount_data_list):  # Use text to display values 
    plt.text(a, b+0.05, '%.0f' % b, ha='center', va='bottom',fontsize=10) 

plt.show()
