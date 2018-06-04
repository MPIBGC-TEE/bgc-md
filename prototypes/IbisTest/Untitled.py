
# coding: utf-8

# In[60]:
from bgc_md.Model import Model
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


# In[236]:


m=Model.from_file("data/FlagstaffTemplates/Ibis.yaml")


# In[237]:


mr=m.model_runs[0]


# In[238]:


cm=mr.model


# In[239]:


rm=m.reservoir_model


# In[240]:


rm.input_fluxes


# In[241]:


rm.external_inputs


# In[242]:


sol=mr.solve()


# In[243]:


C_il_f=sol[:,0]
C_il_g=sol[:,3]


print(C_il_f)
s=C_il_g+C_il_f
print(s)
lamda=C_il_f/s
print(lamda)
i=0
total_f=sol[:,i]+sol[:,i+1]+sol[:,i+2]
i=3
total_g=sol[:,i]+sol[:,i+1]+sol[:,i+2]

plt.plot(mr.times,C_il_f)
#plt.plot(mr.times,c_f)

fig = plt.figure(figsize=(7,7))

ax = fig.add_subplot(4,1,1)
ax.plot(mr.times,C_il_f,"r")
ax.plot(mr.times,C_il_g,"g")

ax = fig.add_subplot(4,1,2)
ax.plot(mr.times,sol[:,1],"r")
ax.plot(mr.times,sol[:,4],"g")


ax = fig.add_subplot(4,1,3)
ax.plot(mr.times,total_f,"r")
ax.plot(mr.times,total_g,"g")
ax = fig.add_subplot(4,1,4)
ax.plot(mr.times,lamda,"y")

fig.savefig('forest_and_shrubs_biomass.pdf')
plt.close(fig)

# In[252]:



