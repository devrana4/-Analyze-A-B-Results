#!/usr/bin/env python
# coding: utf-8

# # Analyze A/B Test Results 
# 
# This project will assure you have mastered the subjects covered in the statistics lessons. We have organized the current notebook into the following sections: 
# 
# - [Introduction](#intro)
# - [Part I - Probability](#probability)
# - [Part II - A/B Test](#ab_test)
# - [Part III - Regression](#regression)
# - [Final Check](#finalcheck)
# - [Submission](#submission)
# 
# Specific programming tasks are marked with a **ToDo** tag. 
# 
# <a id='intro'></a>
# ## Introduction
# 
# A/B tests are very commonly performed by data analysts and data scientists. For this project, you will be working to understand the results of an A/B test run by an e-commerce website.  Your goal is to work through this notebook to help the company understand if they should:
# - Implement the new webpage, 
# - Keep the old webpage, or 
# - Perhaps run the experiment longer to make their decision.
# 
# Each **ToDo** task below has an associated quiz present in the classroom.  Though the classroom quizzes are **not necessary** to complete the project, they help ensure you are on the right track as you work through the project, and you can feel more confident in your final submission meeting the [rubric](https://review.udacity.com/#!/rubrics/1214/view) specification. 
# 
# >**Tip**: Though it's not a mandate, students can attempt the classroom quizzes to ensure statistical numeric values are calculated correctly in many cases.
# 
# <a id='probability'></a>
# ## Part I - Probability
# 
# To get started, let's import our libraries.

# In[48]:


import pandas as pd
import numpy as np
import random
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
#We are setting the seed to assure you get the same answers on quizzes as we set up
random.seed(42)


# ### ToDo 1.1
# Now, read in the `ab_data.csv` data. Store it in `df`. Below is the description of the data, there are a total of 5 columns:
# 
# <center>
# 
# |Data columns|Purpose|Valid values|
# | ------------- |:-------------| -----:|
# |user_id|Unique ID|Int64 values|
# |timestamp|Time stamp when the user visited the webpage|-|
# |group|In the current A/B experiment, the users are categorized into two broad groups. <br>The `control` group users are expected to be served with `old_page`; and `treatment` group users are matched with the `new_page`. <br>However, **some inaccurate rows** are present in the initial data, such as a `control` group user is matched with a `new_page`. |`['control', 'treatment']`|
# |landing_page|It denotes whether the user visited the old or new webpage.|`['old_page', 'new_page']`|
# |converted|It denotes whether the user decided to pay for the company's product. Here, `1` means yes, the user bought the product.|`[0, 1]`|
# </center>
# Use your dataframe to answer the questions in Quiz 1 of the classroom.
# 
# 
# >**Tip**: Please save your work regularly.
# 
# **a.** Read in the dataset from the `ab_data.csv` file and take a look at the top few rows here:

# In[2]:


df = pd.read_csv('ab_data.csv')
df.head()


# **b.** Use the cell below to find the number of rows in the dataset.

# In[3]:


df.shape[0]


# **c.** The number of unique users in the dataset.

# In[4]:


df.nunique()


# **d.** The proportion of users converted.

# In[5]:


(df['converted']).mean()


# **e.** The number of times when the "group" is `treatment` but "landing_page" is not a `new_page`.

# In[6]:


(df.query('group== "treatment" and landing_page != "new_page"').shape[0])+ (df.query('group!= "treatment" and landing_page == "new_page"').shape[0])


# **f.** Do any of the rows have missing values?

# In[7]:


df.isnull().sum()


# ### ToDo 1.2  
# In a particular row, the **group** and **landing_page** columns should have either of the following acceptable values:
# 
# |user_id| timestamp|group|landing_page|converted|
# |---|---|---|---|---|
# |XXXX|XXXX|`control`| `old_page`|X |
# |XXXX|XXXX|`treatment`|`new_page`|X |
# 
# 
# It means, the `control` group users should match with `old_page`; and `treatment` group users should matched with the `new_page`. 
# 
# However, for the rows where `treatment` does not match with `new_page` or `control` does not match with `old_page`, we cannot be sure if such rows truly received the new or old wepage.  
# 
# 
# Use **Quiz 2** in the classroom to figure out how should we handle the rows where the group and landing_page columns don't match?
# 
# **a.** Now use the answer to the quiz to create a new dataset that meets the specifications from the quiz.  Store your new dataframe in **df2**.

# In[8]:


# Remove the inaccurate rows, and store the result in a new dataframe df2
df1=df.drop(df[(df['group'] == 'treatment') & (df['landing_page'] != 'new_page')].index)
print(df1)
df2=df1.drop(df1[(df1['group'] == 'control') & (df1['landing_page'] == 'new_page')].index)


# In[9]:


# Double Check all of the incorrect rows were removed from df2 - 
# Output of the statement below should be 0
df2[((df2['group'] == 'treatment') == (df2['landing_page'] == 'new_page')) == False].shape[0]


# ### ToDo 1.3  
# Use **df2** and the cells below to answer questions for **Quiz 3** in the classroom.

# **a.** How many unique **user_id**s are in **df2**?

# In[10]:


df2.nunique()


# In[11]:


df2.shape


# In[ ]:





# In[ ]:





# **b.** There is one **user_id** repeated in **df2**.  What is it?

# In[15]:


df2.duplicated('user_id').sum()


# **c.** Display the rows for the duplicate **user_id**? 

# In[16]:


df2[df2.duplicated('user_id', keep= False)]


# **d.** Remove **one** of the rows with a duplicate **user_id**, from the **df2** dataframe.

# In[19]:


# Remove one of the rows with a duplicate user_id..
# Hint: The dataframe.drop_duplicates() may not work in this case because the rows with duplicate user_id are not entirely identical. 
df2.drop(2893, inplace= True)


# In[20]:


# Check again if the row with a duplicate user_id is deleted or not
df2.duplicated('user_id').sum()


# ### ToDo 1.4  
# Use **df2** in the cells below to answer the quiz questions related to **Quiz 4** in the classroom.
# 
# **a.** What is the probability of an individual converting regardless of the page they receive?<br><br>
# 
# >**Tip**: The probability  you'll compute represents the overall "converted" success rate in the population and you may call it $p_{population}$.
# 
# 

# In[21]:


p_pop = (df2['converted']==1).mean()
print(p_pop)


# **b.** Given that an individual was in the `control` group, what is the probability they converted?

# In[22]:


p_converted_control = (df2.query('group == "control"')['converted']).mean()
print(p_converted_control)


# **c.** Given that an individual was in the `treatment` group, what is the probability they converted?

# In[23]:


p_treat_converted = (df2.query('group == "treatment"')['converted']).mean()
print(p_treat_converted)


# >**Tip**: The probabilities you've computed in the points (b). and (c). above can also be treated as conversion rate. 
# Calculate the actual difference  (`obs_diff`) between the conversion rates for the two groups. You will need that later.  

# In[24]:


# Calculate the actual difference (obs_diff) between the conversion rates for the two groups.
obs_diff =p_converted_control-p_treat_converted
print(obs_diff)


# **d.** What is the probability that an individual received the new page?

# In[25]:


p_newPage = (df2['landing_page']=='new_page').mean()
print(p_newPage)


# **e.** Consider your results from parts (a) through (d) above, and explain below whether the new `treatment` group users lead to more conversions.
# 

# #the prob of the individual received old page == prob of the old page with respect to all user who received new and old page
# prob_oldpage = 1- prob_newpage
# prob_oldpage

# <a id='ab_test'></a>
# ## Part II - A/B Test
# 
# Since a timestamp is associated with each event, you could run a hypothesis test continuously as long as you observe the events. 
# 
# However, then the hard questions would be: 
# - Do you stop as soon as one page is considered significantly better than another or does it need to happen consistently for a certain amount of time?  
# - How long do you run to render a decision that neither page is better than another?  
# 
# These questions are the difficult parts associated with A/B tests in general.  
# 
# 
# ### ToDo 2.1
# For now, consider you need to make the decision just based on all the data provided.  
# 
# > Recall that you just calculated that the "converted" probability (or rate) for the old page is *slightly* higher than that of the new page (ToDo 1.4.c). 
# 
# If you want to assume that the old page is better unless the new page proves to be definitely better at a Type I error rate of 5%, what should be your null and alternative hypotheses (**$H_0$** and **$H_1$**)?  
# 
# You can state your hypothesis in terms of words or in terms of **$p_{old}$** and **$p_{new}$**, which are the "converted" probability (or rate) for the old and new pages respectively.

# >**Put your answer here.**

# ### ToDo 2.2 - Null Hypothesis $H_0$ Testing
# Under the null hypothesis $H_0$, assume that $p_{new}$ and $p_{old}$ are equal. Furthermore, assume that $p_{new}$ and $p_{old}$ both are equal to the **converted** success rate in the `df2` data regardless of the page. So, our assumption is: <br><br>
# <center>
# $p_{new}$ = $p_{old}$ = $p_{population}$
# </center>
# 
# In this section, you will: 
# 
# - Simulate (bootstrap) sample data set for both groups, and compute the  "converted" probability $p$ for those samples. 
# 
# 
# - Use a sample size for each group equal to the ones in the `df2` data.
# 
# 
# - Compute the difference in the "converted" probability for the two samples above. 
# 
# 
# - Perform the sampling distribution for the "difference in the converted probability" between the two simulated-samples over 10,000 iterations; and calculate an estimate. 
# 
# 
# 
# Use the cells below to provide the necessary parts of this simulation.  You can use **Quiz 5** in the classroom to make sure you are on the right track.

# **a.** What is the **conversion rate** for $p_{new}$ under the null hypothesis? 

# In[26]:


p_new = df.converted.mean()
p_new


# **b.** What is the **conversion rate** for $p_{old}$ under the null hypothesis? 

# In[27]:


p_old = df.converted.mean()
p_old


# **c.** What is $n_{new}$, the number of individuals in the treatment group? <br><br>
# *Hint*: The treatment group users are shown the new page.

# In[28]:


n_new = df2.query('landing_page=="new_page"').shape[0]
n_new


# **d.** What is $n_{old}$, the number of individuals in the control group?

# In[29]:


n_old = df2.query('landing_page=="old_page"').shape[0]
n_old


# **e. Simulate Sample for the `treatment` Group**<br> 
# Simulate $n_{new}$ transactions with a conversion rate of $p_{new}$ under the null hypothesis.  <br><br>
# *Hint*: Use `numpy.random.choice()` method to randomly generate $n_{new}$ number of values. <br>
# Store these $n_{new}$ 1's and 0's in the `new_page_converted` numpy array.
# 

# In[33]:


new_page_converted = np.random.binomial(1,p_new,n_new)
new_page_converted


# In[34]:


#Mean for the new page converted with n_new elements of 0,1
new_page_converted_mean=new_page_converted.mean()
new_page_converted_mean


# In[35]:


(new_page_converted.sum(), len(new_page_converted) - new_page_converted.sum())


# In[36]:


new_page_converted2 = np.random.choice([1, 0], size=n_new, p=[p_new, (1-p_new)])
new_page_converted2


# In[37]:


#Mean for the new page converted with n_new elements of 0,1 with random.choice
new_page_converted2_mean=new_page_converted2.mean()
new_page_converted2_mean


# **f. Simulate Sample for the `control` Group** <br>
# Simulate $n_{old}$ transactions with a conversion rate of $p_{old}$ under the null hypothesis. <br> Store these $n_{old}$ 1's and 0's in the `old_page_converted` numpy array.

# In[30]:


old_page_converted = np.random.binomial(1,p_old,n_old)
old_page_converted


# In[39]:


old_page_converted_mean=old_page_converted.mean()
old_page_converted_mean


# In[40]:


(old_page_converted.sum(), len(old_page_converted) - old_page_converted.sum())


# In[41]:


old_page_converted2 = np.random.choice([1, 0], size=n_old, p=[p_old, (1-p_old)])
old_page_converted2


# In[43]:


old_page_converted2_mean=old_page_converted2.mean()
old_page_converted2_mean


# **g.** Find the difference in the "converted" probability $(p{'}_{new}$ - $p{'}_{old})$ for your simulated samples from the parts (e) and (f) above. 

# In[50]:


# Get the diff between new page converted mean and old page converted mean
diff = new_page_converted_mean - old_page_converted_mean
diff


# 
# **h. Sampling distribution** <br>
# Re-create `new_page_converted` and `old_page_converted` and find the $(p{'}_{new}$ - $p{'}_{old})$ value 10,000 times using the same simulation process you used in parts (a) through (g) above. 
# 
# <br>
# Store all  $(p{'}_{new}$ - $p{'}_{old})$  values in a NumPy array called `p_diffs`.

# In[52]:


#Identify values for the iterations
p_diffs=[]
size=10000

#Stimulate 10000 values of p_new - p_old
for _ in range(size):
    new_page_converted_mean = np.random.binomial(1,p_new,n_new).mean()
    old_page_converted_mean = np.random.binomial(1,p_old,n_old).mean()
    p_diff = new_page_converted_mean - old_page_converted_mean
    p_diffs.append(p_diff)
    
#Convert to numpy array
p_diffs = np.array(p_diffs)


# **i. Histogram**<br> 
# Plot a histogram of the **p_diffs**.  Does this plot look like what you expected?  Use the matching problem in the classroom to assure you fully understand what was computed here.<br><br>
# 
# Also, use `plt.axvline()` method to mark the actual difference observed  in the `df2` data (recall `obs_diff`), in the chart.  
# 
# >**Tip**: Display title, x-label, and y-label in the chart.

# In[53]:


# Get observed differnce value to display in histogram with the p_diffs array
obs_diff = prob_treatment_converted - prob_control_converted
obs_diff


# In[ ]:


plt.hist(p_diffs, label="Prob Diff")
plt.axvline(x=obs_diff , color='red', label="Obs Diff")
plt.legend()
plt.xlabel('Probability Differences' , color="#881111", size="14")
plt.ylabel('Simulation Frequency ' , color="#881111", size="14")
plt.title('Simulated Differences (P_new - P_old) under the Null hypothesis', color="blue", size="16");


# **j.** What proportion of the **p_diffs** are greater than the actual difference observed in the `df2` data?

# In[58]:


(p_diffs > obs_diff).mean()


# **k.** Please explain in words what you have just computed in part **j** above.  
#  - What is this value called in scientific studies?  
#  - What does this value signify in terms of whether or not there is a difference between the new and old pages? *Hint*: Compare the value above with the "Type I error rate (0.05)". 

# >**Put your answer here.**

# 
# 
# **l. Using Built-in Methods for Hypothesis Testing**<br>
# We could also use a built-in to achieve similar results.  Though using the built-in might be easier to code, the above portions are a walkthrough of the ideas that are critical to correctly thinking about statistical significance. 
# 
# Fill in the statements below to calculate the:
# - `convert_old`: number of conversions with the old_page
# - `convert_new`: number of conversions with the new_page
# - `n_old`: number of individuals who were shown the old_page
# - `n_new`: number of individuals who were shown the new_page
# 

# In[56]:


import statsmodels.api as sm
convert_old = df2.query('landing_page == "old_page"').converted.sum()
convert_new = df2.query('landing_page == "new_page"').converted.sum()
n_old = n_old
n_new = n_new


# In[57]:


z_score, p_value = sm.stats.proportions_ztest([convert_old, convert_new], [n_old, n_new], alternative='smaller')
(z_score, p_value)

