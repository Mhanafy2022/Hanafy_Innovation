#!/usr/bin/env python
# coding: utf-8

# # Project: Investigate a Dataset - [No-Show Appointments]
# 
# ## Table of Contents
# <ul>
# <li><a href="#intro">Introduction</a></li>
# <li><a href="#wrangling">Data Wrangling</a></li>
# <li><a href="#eda">Exploratory Data Analysis</a></li>
# <li><a href="#conclusions">Conclusions</a></li>
# </ul>

# <a id='intro'></a>
# ## Introduction
# 
# ### Dataset Description 
# 
# This dataset collects information from 100k medical appointments in Brazil and is focused on the question of whether or not patients show up for their appointment. A number of characteristics about the patient are included in each row.
# 
# •	‘ScheduledDay’ tells us on what day the patient set up their appointment.
# 
# •	‘Neighborhood’ indicates the location of the hospital.
# 
# •	‘Scholarship’ indicates whether or not the patient is enrolled in Brasilian welfare program Bolsa Família.
# 
# •	Be careful about the encoding of the last column: it says ‘No’ if the patient showed up to their appointment, and ‘Yes’     if they did not show up.
# 
# 
# 
# ### Question(s) for Analysis
# 
# What factors are important for us to know in order to predict if a patient will show up for their scheduled appointment?

# In[1]:


# Use this cell to set up import statements for all of the packages that you
#   plan to use.
# Remember to include a 'magic word' so that your visualizations are plotted
#   inline with the notebook. See this page for more:
#   http://ipython.readthedocs.io/en/stable/interactive/magics.html
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as snb
get_ipython().run_line_magic('matplotlib', 'inline')


# In[5]:


# Upgrade pandas to use dataframe.explode() function. 
get_ipython().system('pip install --upgrade pandas==0.25.0')


# <a id='wrangling'></a>
# ## Data Wrangling
# 
# To have a quick view on Dataset and prepare it for Cleaning and Analysis
# 
# 
# ### General Properties
# 

# In[2]:


# Load your data and print out a few lines. Perform operations to inspect data
#   types and look for instances of missing or possibly errant data.
Data_Set = pd.read_csv("./Database_No_show_appointments/noshowappointments-2016.csv")
Data_Set.head()


# Checked the main and important Data Factors within which extracted answers and got best results.

# In[3]:


# To Clarify the shape of Data (Columns&Rows)
Data_Set.shape


# Data contains 110527 rows and 14 columns.

# In[4]:


# To Check the total number for duplicated values
sum(Data_Set.duplicated())


# There are no duplicated values.

# In[5]:


# To Identify the unique values
Data_Set["PatientId"].unique()


# Return the array for Patient ID unique values.

# In[6]:


# To Check the number of unique values
Data_Set["PatientId"].nunique()


# Data consists of 62299 unique ID for patients.

# In[7]:


# To Check the total number for duplicated values of "PatientId"
Data_Set["PatientId"].duplicated().sum()


# Data consists of 48228 duplicated IDs for patients.

# In[8]:


# To Check the total number for duplicated values of "PatientId" in relation with "No-Show"
Data_Set.duplicated(["PatientId","No-show"]).sum()


# Data consists of 38710 duplicated IDs for patients who were attended or were absent.

# In[9]:


# To Identify if there is any missing values in the Dataset
Data_Set.info()


# There are no missing values for Dataset.

# In[10]:


# To obtain the essentail Statistics required
Data_Set.describe()


# *Descriptive Statistics Analysis*
# 
# Average age is 37 years old.
# 
# Maximum age is 115 years old.
# 
# Minimum age is -1 which doesn't make any sense that human age starts from -1 and its clear mistake.
# 
# 50% of ages are between 18 and 55 years old.
# 
# 50% of patients received SMS.
# 
# Majority of patients are not diabetics, alcoholic, handicapped or with hypertension.
# 
# Majority of patients have no scholarship (Medical insurance).

# 
# ### Data Cleaning
# 
# To Remove unnecessary data which has no effect on **Analysis** and adjust the **required and significant information.**

# In[11]:


# To Rename & Correct some Columns names to ensure the Best Analysis
Data_Set.rename(columns={'No-show' : 'No_Show'},inplace=True)
Data_Set.rename(columns={'Handcap' : 'Handicap'},inplace=True)
Data_Set.rename(columns={'Hipertension' : 'Hypertension'},inplace=True)
Data_Set.head()


# In[12]:


# To Remove duplicated values for "PatientID" & "No_Show"
Data_Set.drop_duplicates(["PatientId","No_Show"],inplace=True)
Data_Set.shape


# Dataset now after removing duplicates consists of 71817 rows and 14 columns.

# In[13]:


# To Clear unused Columns to ensure Best Analysis
Data_Set.drop(["PatientId", "AppointmentID", "ScheduledDay", "AppointmentDay"],axis=1,inplace=True)
Data_Set.head()


# ## Data Preprocessing Summary:
# 
# •	Checked the main and important Data Factors within which extracted answers and got best results.
# 
# •	Data contains 110527 rows and 14 columns.
# 
# •	There are no duplicated values.
# 
# •	Data consists of 62299 unique ID for patients.
# 
# •	Data consists of 48228 duplicated IDs for patients.
# 
# •	Data consists of 38710 duplicated IDs for patients who were attended or were absent.
# 
# •	There are no missing values for Dataset.
# 
# •	Removed unnecessary data which has no effect on Analysis and adjust the required and significant information.
# 
# •	Average patients age is 37 years old.
# 
# •	Maximum age is 115 years old.
# 
# •	Minimum age is -1 which doesn't make any sense that human age starts from -1 and its clear mistake.
# 
# •	50% of ages are between 18 and 55 years old.
# 
# •	50% of patients received SMS.
# 
# •	Majority of patients are not diabetics, alcoholic, handicapped or with hypertension.
# 
# •	Majority of patients have no scholarship (Medical insurance).
# 

# # <a id='eda'></a>
# ## Exploratory Data Analysis
# 
# Now after Data cleaning phase, it's time for **exploration**, focusing on **Data Visualization** and **Descriptive Statistics** to ensure **best Analysis Conclusion.**
# 
# 
# ### Data Overview

# In[14]:


# To Explore Dataset within Data Visualization
Data_Set.hist(figsize=(14,11));


# In[15]:


# To Classify "Show" & "No_Show" Patients
Show_Patients = Data_Set.No_Show == "No"
Noshow_Patients = Data_Set.No_Show == "Yes"
Data_Set[Show_Patients].count(), Data_Set[Noshow_Patients].count()


# The total number of Show patients is 54154 and No_Show patients is 17663

# # Measuring Impact of different factors on Patients Attendance

# In[16]:


# To Investigate if the Patients age affect on their attendance
plt.figure(figsize=[14,6])
Data_Set.Age[Show_Patients].hist(alpha=.7,bins=12,color='green',label='Show_Patients')
Data_Set.Age[Noshow_Patients].hist(alpha=.7,bins=12,color='blue',label='Noshow_Patients')
plt.legend();
plt.title('Measuring The Impact of Patients Age')
plt.xlabel('Patients Age')
plt.ylabel('Patients Number');


# Ages from 0 to 10 is the top attendance rate, from 45 to 55 is the middle rate and starting from 65 years old is the lowest rate which means that people attendance rate decrease as long as they are aging.

# In[17]:


# To Investigate if Hypertension Disease affect their Attendance
plt.figure(figsize=[10,6])
Data_Set.Hypertension[Show_Patients].hist(alpha=.7,bins=12,color='blue',label='Show_Patients')
Data_Set.Hypertension[Noshow_Patients].hist(alpha=.7,bins=12,color='yellow',label='Noshow_Patients')
plt.legend();
plt.title('Measuring The Impact of Hypertension Disease')
plt.xlabel('Hypertension Disease')
plt.ylabel('Patients Number');


# Hypertension Disease has no effect on patients attendance.

# In[18]:


# To Investigate if Diabetes Disease affect their Attendance
plt.figure(figsize=[10,6])
Data_Set.Diabetes[Show_Patients].hist(alpha=.7,bins=12,color='blue',label='Show_Patients')
Data_Set.Diabetes[Noshow_Patients].hist(alpha=.7,bins=12,color='yellow',label='Noshow_Patients')
plt.legend();
plt.title('Measuring The Impact of Diabetes Disease')
plt.xlabel('Diabetes Disease')
plt.ylabel('Patients Number');


# Diabetes Disease has no effect on patients attendance.

# In[19]:


# To Investigate if the Alcoholism affects the Patients Attendance
plt.figure(figsize=[10,6])
Data_Set.Alcoholism[Show_Patients].hist(alpha=.7,bins=12,color='blue',label='Show_Patients')
Data_Set.Alcoholism[Noshow_Patients].hist(alpha=.7,bins=12,color='red',label='Noshow_Patients')
plt.legend();
plt.title('Measuring The Impact of Alcoholism')
plt.xlabel('Alcoholic Patients')
plt.ylabel('Patients Number');


# Alcoholism Disease has no effect on patients attendance.

# In[20]:


# To Investigate if the Handicap affects the Patients Attendance
plt.figure(figsize=[10,6])
Data_Set.Handicap[Show_Patients].hist(alpha=.7,bins=12,color='green',label='Show_Patients')
Data_Set.Handicap[Noshow_Patients].hist(alpha=.7,bins=12,color='red',label='Noshow_Patients')
plt.legend();
plt.title('Measuring The Impact of Handicap')
plt.xlabel('Handicapped Patients')
plt.ylabel('Patients Number');


# Handicap has no effect on patients attendance.

# In[21]:


# To Identify the Attendance Percentage of Gender
plt.figure(figsize=[14,5])
Data_Set.Gender[Show_Patients].hist(alpha=.7,bins=12,color='green',label='Show_Patients')
Data_Set.Gender[Noshow_Patients].hist(alpha=.7,bins=12,color='red',label='Noshow_Patients')
plt.legend();
plt.title('Male VS Female Attendance')
plt.xlabel('Patients Gender')
plt.ylabel('Patients Number');


# Gender has no explicit effect on patients attendance.

# In[22]:


# To Investigate if the Patients Age & Gender affect their Attendance
plt.figure(figsize=[10,6])
Data_Set[Show_Patients].groupby('Gender').Age.mean().plot(kind='bar',color='yellow',label='Show_Patients')
Data_Set[Noshow_Patients].groupby('Gender').Age.mean().plot(kind='bar',color='green',label='Noshow_Patients')
plt.legend();
plt.title('Measuring The Impact of Patients Age & Gender')
plt.xlabel('Patients Gender')
plt.ylabel('Average Age');


# There is no clear correlation between age and gender affect patients attendance

# In[23]:


# To Investigate if the Patients Age & Gender affect their Attendance within a Numeric Analysis
print(Data_Set[Show_Patients].groupby('Gender').Age.mean(),Data_Set[Noshow_Patients].groupby('Gender').Age.mean())


# In[24]:


# To Investigate if SMS affect the Patient Attendance
plt.figure(figsize=[14,5])
Data_Set.SMS_received[Show_Patients].hist(alpha=.7,bins=12,color='brown',label='Show_Patients')
Data_Set.SMS_received[Noshow_Patients].hist(alpha=.7,bins=12,color='blue',label='Noshow_Patients')
plt.legend();
plt.title('Measuring The Impact of SMS')
plt.xlabel('SMS')
plt.ylabel('Patients Number');


# The total number of show patients without receiving SMS is greater than show patients who already have received SMS.

# In[25]:


# To Investigate if the Patients Neighbourhood affect their Attendance
plt.figure(figsize=[15,7])
Data_Set.Neighbourhood[Show_Patients].value_counts().plot(kind='bar',color='blue',label='Show_Patients')
Data_Set.Neighbourhood[Noshow_Patients].value_counts().plot(kind='bar',color='orange',label='Noshow_Patients')
plt.legend();
plt.title('Measuring The Impact of Neighbourhood')
plt.xlabel('Patients Neighbourhood')
plt.ylabel('Patients Number');


# Neighbourhood has a strong and direct effect on patients attendance, the top attendance rate neighbourhood is JARDIM CAMBURI and the lowest one is ILHA DO FRADE.

# In[25]:


# To Investigate if the Patients Scholarship affect their Attendance
plt.figure(figsize=[14,6])
Data_Set.Scholarship[Show_Patients].hist(alpha=.7,bins=12,color='green',label='Show_Patients')
Data_Set.Scholarship[Noshow_Patients].hist(alpha=.7,bins=12,color='brown',label='Noshow_Patients')
plt.legend();
plt.title('Measuring The Impact of Scholarship')
plt.xlabel('Patients Scholarship')
plt.ylabel('Patients Number');


# Scholarship has no effect on patient attendance rate.

# <a id='conclusions'></a>
# ## Conclusions
# 
# •	Neighbourhood is highly correlated with patients’ attendance rate as there is obvious difference among attendance rate in many neighbourhoods.
# 
# •	We need to reconsider the SMS campaign to make sure that all patients received in correct way with a good and creative content, that’s because the total number of show patients without receiving SMS is greater than show patients who already have received SMS.
# 
# •	Ages from 0 to 10 is the top attendance rate, from 45 to 55 is the middle rate and starting from 65 years old is the lowest rate which means that people attendance rate decrease as long as they are aging.
# 
# •	Both age and gender have no clear correlation with patients’ attendance.
# 
# 
# ## Limitations
# 
# Apparently, couldn’t find any clear correlation among patients’ attendance and different factors suchlike Hypertension, Diabetes, gender, alcoholism, disabilities or medical insurance enrollment.
# 
# 
# 
# ## Submitting your Project 
# 
# 

# In[26]:


from subprocess import call
call(['python', '-m', 'nbconvert', 'Investigate_a_Dataset.ipynb'])

