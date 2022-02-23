#!/usr/bin/env python
# coding: utf-8

# # Data Review

# The databases are the 2020-2022 The World Covid19 Analysis (Missing some Countries )

# In[42]:


pip install -U pandasql


# In[43]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import math
plt.style.use('fivethirtyeight')
from functools import reduce
from pandasql import sqldf


get_ipython().run_line_magic('matplotlib', 'inline')


# In[44]:


CovidDeaths = pd.read_excel('C:/Users/tuzil/Desktop/All Projects/Project_Covid_19/CovidDeaths.xlsx')


# In[45]:


CovidDeaths.head(5)


# In[46]:


CovidVaccinations = pd.read_excel('C:/Users/tuzil/Desktop/All Projects/Project_Covid_19/CovidVaccinations.xlsx')


# In[47]:


CovidVaccinations.head(5)


# In[48]:


CovidDeaths.info()
CovidDeaths.describe()


# In[49]:


CovidVaccinations.info()
CovidVaccinations.describe()


# In[50]:


CovidVaccinations.isnull().sum().sort_values(ascending = False)


# In[51]:


CovidDeaths.isnull().sum().sort_values(ascending = False)


# In[ ]:





# # Data Cleaning

# In[52]:


CovidDeaths_copy = CovidDeaths.copy()
CovidVaccinations_copy = CovidVaccinations.copy()


# In[ ]:





# In[53]:


CovidDeaths_copy.info()


# In[54]:


CovidDeaths_copy.isnull().sum().sort_values(ascending = False)


# In[55]:


plt.figure(figsize=(12,10))
sns.barplot(data=CovidDeaths_copy.isnull().sum().sort_values(ascending = False).reset_index(), y='index',x=0)
plt.ylabel('Attributes')
plt.title('CovidDeaths_Missing_Values')
plt.xlabel('CovidDeaths_Missing_Value_Count')
plt.show()


# In[56]:


CovidDeaths_copy.drop(['excess_mortality_cumulative_per_million','excess_mortality','excess_mortality_cumulative','excess_mortality_cumulative_absolute','weekly_icu_admissions','weekly_icu_admissions_per_million','weekly_hosp_admissions','weekly_hosp_admissions_per_million'], axis = 1)


# In[ ]:





# In[57]:


# Show the CovidVaccinations' null value
CovidVaccinations_copy.isnull().sum().sort_values(ascending = False)


# In[ ]:





# In[225]:


# Plot the null value

plt.figure(figsize=(12,10))
sns.barplot(data=CovidVaccinations_copy.isnull().sum().sort_values(ascending = False).reset_index(), y='index',x=0)
plt.ylabel('Attributes')
plt.title('CovidVaccinations_Missing_Values')
plt.xlabel('CovidVaccinations_Missing_Value_Count')
plt.show()


# In[59]:


CovidVaccinations_copy.info()


# In[60]:


CovidVaccinations_copy.drop(['diabetes_prevalence','population_density','life_expectancy'], axis = 1)


# In[ ]:





# In[61]:


CovidVaccinations_copy.head()


# In[62]:


CovidVaccinations_copy.drop(['excess_mortality_cumulative_per_million','excess_mortality','excess_mortality_cumulative','excess_mortality_cumulative_absolute'], axis = 1)


# In[ ]:





# # SQL Part

# This part is according to the SQL syntax to solve some business questions.

# ## Question 1: What are the Top 10 countries with the highest total cases

# In[ ]:


Anwser: Brazil, France, Germany, Argentina, Colombia, Belgium, Czechia, Canada, Australia, Chile


# In[224]:


# Question 1 Code:

pysqldf = lambda sql : sqldf(sql_1,globals())
sql_1 = '''Select Location, total_cases,total_deaths, MAX(total_cases) as total_cases
   From CovidDeaths_copy 
   Where continent is not null
   GROUP BY location
   ORDER BY total_cases DESC
   LIMIT 10
'''
location_count = pysqldf(sql_1)
location_count.head(15)


# In[ ]:





# ## Question 2: What are the Top 5 countries with the highest InfectedRate

# Answer: Faeroe,Islands, Andorra, Gibraltar, Denmark, Georgia

# In[144]:


# Question 2 Code:

pysqldf = lambda sql : sqldf(sql_2,globals())
sql_2 = '''SELECT location, date, Population, MAX(total_cases) as MaxInfectionCount,  Max((total_cases/population))*100 as MaxInfectedRate
FROM CovidDeaths_copy
GROUP BY location, Population
ORDER BY MaxInfectedRate DESC
LIMIT 5
'''
Top5_InfectedRate = pysqldf(sql_2)
Top5_InfectedRate


# In[ ]:





# ## Question 3: What are the Top 5 countries with the highest MaxDeathRate?

# Answer: Bulgaria,Herzegovina, Georgia, Croatia, Czechia

# In[145]:


# Question 3 Code:

pysqldf = lambda sql : sqldf(sql_3,globals())
sql_3 = '''SELECT location, date, Population, MAX(total_deaths) as MaxDeathCount,  Max((total_deaths/population))*100 as MaxDeathRate
FROM CovidDeaths_copy
GROUP BY location, Population
ORDER BY MaxDeathRate DESC
LIMIT 10
'''
Top10_DeathRate = pysqldf(sql_3)
Top10_DeathRate


# In[ ]:





# ## Join Two Tables

# In[260]:


pysqldf = lambda sql : sqldf(sql_4,globals())
sql_4 = '''SELECT D.continent, D.location, D.date, D.population, D.total_cases, D.total_deaths, V.total_vaccinations, 
V.total_boosters, V.gdp_per_capita, V.life_expectancy
FROM CovidDeaths_copy D
LEFT JOIN CovidVaccinations_copy V
ON D.location = V.location AND D.date = V.date
WHERE D.continent is not null

'''
Jointables = pysqldf(sql_4)
Jointables.head()


# In[ ]:





# ## Question 4: What are the Top 5 countries with the highest Vaccinations?

# Anwser: China, Brazil, Germany, Bangladesh, France

# In[268]:


pysqldf = lambda sql : sqldf(sql_5,globals())
sql_5 = '''
SELECT continent, location, date, population, total_cases, total_deaths, MAX(total_vaccinations) as Max_Vaccinations, 
MAX(total_vaccinations)/population AS VaccinationsRate, gdp_per_capita, life_expectancy
FROM Jointables 
GROUP BY location
ORDER BY Max_vaccinations DESC

'''
# Formate the date type 
JoinTableFilter = pysqldf(sql_5)
JoinTableFilter['date'] = pd.to_datetime(JoinTableFilter['date'])
JoinTableFilter['Year'] = JoinTableFilter['date'].dt.year
JoinTableFilter['Month'] = JoinTableFilter['date'].dt.month
JoinTableFilter


# In[ ]:





# In[ ]:





# # Visualization Part

# ## Question 5: What are the Top 5 countries in GDP?

# Anwswer: Brunei, Bermuda, Cayman Islands, Denmark, Austria

# ### Plot of Ranking the Country's GDP

# In[269]:


#Ranking the Countries with highest GDP per capita
fig, ax = plt.subplots(figsize=(16,6))
sns.barplot(x='location',y='gdp_per_capita',data=JoinTableFilter.sort_values('gdp_per_capita',ascending=False).head(30), palette='Set3')
plt.xticks(rotation=90)
plt.show()


# In[ ]:





# ### Question 6: What is the average life expectancy? What is the mode age of life expectancy?

# Anwser: mean = 73, mode are 61.58 and 77.29

# In[270]:


life_med = JoinTableFilter['life_expectancy'].mean()
life_mode = JoinTableFilter['life_expectancy'].mode()
print(life_mode)

plt.hist(data = JoinTableFilter, x = 'life_expectancy', color = "lightgreen", bins=15)
plt.axvline(x=life_med, color='deeppink', ls='--', ymax=0.95, lw=2, label="Mean: {:.0f}".format(life_med))
plt.text(life_med,10,'Mean',rotation=0)
plt.xlabel("life_expectancy")
plt.ylabel("Count")
plt.xlim(50,90)
plt.grid()
plt.title("Life_Expectancy_Count")
plt.legend(bbox_to_anchor=(1.0, 1), loc='upper left');


# In[ ]:





# ### Question 7: What is the correlationship between 'gdp_per_capita' and 'VaccinationsRate'?

# Anwser: The below scatterplot investigates the 'gdp_per_capita' is more, and the 'VaccinationsRate' is more, so the 'gdp_per_capita' positively correlates with 'VaccinationsRate'.

# In[271]:


# gdp_per_capita VS VaccinationsRate
plt.figure(figsize=(12,10))
sns.scatterplot(data=JoinTableFilter,x='gdp_per_capita',y='VaccinationsRate',hue='location')


# In[ ]:





# ### Plot for Date VS total_cases/Max_Vaccinations/total_deaths

# The content of this data is incomplete, so we only analyze the existing content. If we are going to get a more accurate conclusion. We should get more sufficient datasets.
# As we can see from the chart below, the total number of confirmed cases in South America remains low. Asia is far ahead of other continents in terms of vaccines. The total death rate in South America is higher than in other continents.

# In[335]:


f, ax = plt.subplots(3,1,figsize=(15,15))
sns.lineplot(x = 'date', y="total_cases", hue="continent", data=JoinTableFilter,  ci="sd", ax=ax[0])
sns.lineplot(x = 'date', y="Max_Vaccinations", hue="continent", data=JoinTableFilter,  ci="sd", ax=ax[1])
sns.lineplot(x = 'date', y="total_deaths", hue="continent", data=JoinTableFilter,  ci="sd", ax=ax[2])
 
ax[0].set(title="World _Covid19_Total_cases")
ax[0].set(xlabel="Date", ylabel="Total_cases")
ax[0].set(ylim = (0,1100000))

ax[1].set(title="World _Covid19_Vaccinations")
ax[1].set(xlabel="Date", ylabel="Max_Vaccinations")
ax[1].set(ylim = (0,800000000))

ax[2].set(title="World _Covid19_Total_deaths")
ax[2].set(xlabel="Date", ylabel="Total_deaths")
ax[2].set(ylim = (0,350000))
    
plt.show()


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




