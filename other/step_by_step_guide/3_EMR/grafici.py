from cProfile import label
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

x = [0.923, 0.921, 0.870, 0.712]
# data
m5xlarge = pd.DataFrame({
    'y_axis': [0.487, 0.420, 0.403, 0.269],
    'x_axis': [0.923, 0.921, 0.870, 0.712]
})

c4xlarge = pd.DataFrame({
    'y_axis': [0.325, 0.292, 0.227, 0.184],
    'x_axis': [0.923, 0.921, 0.870, 0.712]
})

m4large = pd.DataFrame({
    'y_axis': [0.565, 0.477, 0.371, 0.283],
    'x_axis': [0.923, 0.921, 0.870, 0.712]
})

plt.rcParams["figure.figsize"] = (13, 5)

# plot
plt.plot('x_axis', 'y_axis', data=m5xlarge,
         linestyle='--', marker='o', label='m5.xlarge')
plt.plot('x_axis', 'y_axis', data=c4xlarge,
         linestyle='--', marker='o', label="c4.xlarge")
plt.plot('x_axis', 'y_axis', data=m4large,
         linestyle='--', marker='o', label="m4.large")
plt.xlabel('accuracy')
plt.ylabel('cost of the execution in $')
plt.legend()
plt.xticks(np.arange(min(x), max(x), 0.015))
plt.savefig("Desktop/tradeoff-emr.svg", dpi=1200,
            bbox_inches='tight', pad_inches=0)
