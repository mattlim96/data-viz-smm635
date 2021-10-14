#%%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# %%
np.random.seed(000)
y = np.random.randint(1,11,10)
x = np.arange(1,11)

# %%
fig = plt.figure(figsize=(5, 5))
ax = fig.add_subplot(111)
ax.bar(x, y, color='grey')
ax.grid(ls='--',axis='y')
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
plt.show()

# %%
# plt.xticks(x)
# plt.ylabel('Usage')
# plt.xlabel('Patient')
# plt.title('Barchart')

# %%
ax.grid?
# %%
