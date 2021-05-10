import matplotlib.pyplot as plt
import pandas as pd
from tkinter import filedialog

# Get CSV file
filename1 = filedialog.askopenfilename(initialdir = 'C:/Users/BrunaK/Desktop', filetypes = [('CSV files', '*.csv')])
file1 = pd.read_csv(filename1)
data = pd.DataFrame(file1)

#Get layout file
filename2 = filedialog.askopenfilename(initialdir = 'C:/Users/BrunaK/Desktop', filetypes = [('CSV files', '*.csv')])
file2 = pd.read_csv(filename2)
layout = pd.DataFrame(file2)
layout = layout.drop(layout.columns[0], axis=1)

#Subtract baseline
baseline = data.min()
data = data - baseline

#Delete unused columns from CSV file
data = data.drop(data.columns[0], axis=1)
data = data.drop(data.columns[0], axis=1)

#Rename columns according to layout
legend = []
i = 0
while i < 8:
    legend.append(list(layout.iloc[i]))
    i = i+1

legend = [x for y in legend for x in y]
data.columns = legend

#Keep only used columns according to layout
data = data.loc[:, data.columns.notnull()]

# Standard plot for QC
plt.plot(data['ref-900'], color='#DA54A3', ls='--')
plt.plot(data['ref-450'], color='#00CC99', ls='--')
plt.plot(data['ref-225'], color='#0071BC', ls='--')
plt.plot(data['new-900'], color='#DA54A3')
plt.plot(data['new-450'], color='#00CC99')
plt.plot(data['new-225'], color='#0071BC')
plt.plot(data['ntc'], color='#C8CCD0')
plt.plot(data['netc'], color='#C8CCD0')

#Plot definitions
plt.xlabel('Cycle')
plt.ylabel('RFU')
plt.axis([0, 120, 0, 50000])
plt.grid(color='#C8CCD0', linewidth=0.5)