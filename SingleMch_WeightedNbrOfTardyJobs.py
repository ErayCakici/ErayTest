#!/usr/bin/env python
# coding: utf-8

# This notebook adresseses a basic single machine scheduling problem. The objective studied is minimizing total weighted number of tardy jobs. 
# 
# Each job is associated with:
# - proccesing time 
# - due date
# - weight
# 
# A job is tardy if the completion time of job *j* is later than the due date. All jobs need to be processed on the single machine and preemption is not allowed. 
# 
# The scheduling problem can be represented by 1| | $\sum_{i=1}^n w_jU_j$. This problem is known to be NP-hard, even when the jobs all have common due date. IBM ILOG CPLEX Optimization Studio includes solvers for both Mathematical and Constraint Programming. Constraint Programming is particularly efficient and useful to tackle such detailed scheduling problems. By using docplex.cp python package, you can easily formulate and solve scheduling problems in python notebooks. Below is an example formulation with randomly generated sample data to provide a better understanding of the problem and the code. 
# 
# 

# In[1]:


from project_lib import Project
project = Project(project_id='3b7d7e85-7967-4801-8634-0ff185f9bc87')


# In[2]:


nbrOfJobs = 10
jobs = [*range(0, nbrOfJobs)] 


# In[3]:


minProcessingTime=10
maxProcessingTime=40
import random
processingTimes = [random.randint(minProcessingTime, maxProcessingTime) for j in jobs]


# In[4]:


minDueDate=75
maxDueDate=200
dueDates = random.sample(range(minDueDate, maxDueDate), len(jobs))


# In[5]:


minWeight=1
maxWeight=5
weights = [random.randint(minWeight, maxWeight) for j in jobs]


# In[6]:


import pandas as pd
JobsTable = pd.DataFrame(columns=['job', 'processing_time', 'weight', 'due_date'])
for j in jobs:
    JobsTable=JobsTable.append({'job': j,'processing_time':processingTimes[j],'weight':weights[j],'due_date':dueDates[j]}, ignore_index=True)
print(JobsTable)


# In[7]:


from docplex.cp.model import *
mdl = CpoModel(name='singleMachineScheduling_WeightedNbrOfTardyJobs') 


# In[8]:


# define production processing interval of each job at each machine
processing_itv_vars = [mdl.interval_var(size=processingTimes[j], name="interval_job{}".format(j)) for j in jobs] 
for j in jobs:
    print(processing_itv_vars[j])


# In[9]:


#minimize number of tardy jobs
objective = mdl.sum((mdl.end_of(processing_itv_vars[j])>dueDates[j])*weights[j] for j in jobs)  
mdl.add(mdl.minimize(objective)) 


# In[10]:


#No overlap constraint
mdl.add(mdl.no_overlap([processing_itv_vars[j] for j in jobs])) 


# In[11]:


msol= mdl.solve(log_output=True)


# In[12]:


print("Solution: ")
msol.print_solution()


# In[13]:


for j in jobs:
    if((msol.get_var_solution(processing_itv_vars[j]).get_end()) > dueDates[j]):
       print("job {} with weight {} is tardy".format(j,weights[j]))
    


# In[14]:


import docplex.cp.utils_visu as visu
import matplotlib.pyplot as plt
#Change the plot size
from pylab import rcParams
rcParams['figure.figsize'] = 25, 5
if msol and visu.is_visu_enabled():
    visu.timeline("Solution Schedule", 0, 100)
    for j in jobs:
        itv = msol.get_var_solution(processing_itv_vars[j])
        if itv.is_present():
            visu.interval(itv,'lightgreen','J' + str(j))
    visu.show()


# In[ ]:




