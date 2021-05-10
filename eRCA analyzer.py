import matplotlib.pyplot as plt
import pandas as pd
import tkinter
from tkinter import filedialog

### Get input files ###

#Read Biorad's output .csv file
root = tkinter.Tk()
root.withdraw()

filename1 = filedialog.askopenfilename(initialdir = 'C:/Users/BrunaK/Desktop', filetypes = [('CSV files', '*.csv')])
file1 = pd.read_csv(filename1)
data = pd.DataFrame(file1)

#Read layout file
filename2 = filedialog.askopenfilename(initialdir = 'C:/Users/BrunaK/Desktop', filetypes = [('CSV files', '*.csv')])
file2 = pd.read_csv(filename2)
layout = pd.DataFrame(file2)
layout = layout.drop(layout.columns[0], axis=1)

### Process data ###

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

### Plot Results ###

plt.rcParams['font.size'] = '16'

#Plot raw traces for standard QC experiments
plt.figure(1)
plt.plot(data['ref-900'], color='#DA54A3', ls='--')
plt.plot(data['ref-450'], color='#00CC99', ls='--')
plt.plot(data['ref-225'], color='#0071BC', ls='--')
plt.plot(data['new-900'], color='#DA54A3')
plt.plot(data['new-450'], color='#00CC99')
plt.plot(data['new-225'], color='#0071BC')
plt.plot(data['ntc'], color='#C8CCD0')
plt.plot(data['netc'], color='#C8CCD0')

plt.xlabel('Cycle')
plt.ylabel('RFU')
plt.axis([0, 120, 0, 50000])
plt.grid(color='#C8CCD0', linewidth=0.5)
plt.tight_layout()
plt.savefig('Raw traces.png')
plt.show()

# Plot value at cycle 20 #

#Get value at cycle 20
rfu20 = data.loc[19]

#Remove ntc and netc from cycle 20 calculation
rfu20 = rfu20.drop(labels=['ntc', 'netc'])

#Calculate average and standard deviation between replicates
avg20 = rfu20.groupby(level=0).mean()
stdev20 = rfu20.groupby(level=0).std()

#Add gap in avg20 and stdev20 series for plot formatting
avg20.at['new-gap']=0
avg20.sort_index(inplace=True)

stdev20.at['new-gap']=0
stdev20.sort_index(inplace=True)

#Plot RFU at cycle 20 with error bars
plt.figure(2)
x = list(range(7))
plt.bar(x, avg20, width=1.0, color=['#0071BC', '#00CC99', '#DA54A3', 'white', '#0071BC', '#00CC99', '#DA54A3'], yerr=stdev20, ecolor='grey', capsize=2)
plt.xticks(x, ['', 'New', '', '', '', 'Ref', ''])
plt.tick_params(axis='x', which = 'both', bottom = False, top=False)
plt.ylabel('RFU at Cycle 20')
plt.ylim(0, 50000)
plt.tight_layout()
plt.savefig('RFU at Cycle 20.png')
plt.show()
