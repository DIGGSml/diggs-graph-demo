import plotly
import plotly.plotly as py
import plotly.graph_objs as go

import xml.etree.ElementTree as ET
import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()

version = input("Enter the Diggs schema version (eg '2.0.b'):")
print (version)
address = '{http://diggsml.org/schemas/' + version +'}'
address2= '{http://diggsml.org/schemas/' + version +'/geotechnical}'
user = input("Enter your plotly Username:")
print (user)

API = input("Enter your plotly API:")
print (API)

graphName = input("Enter the name for your graoh")


plotly.tools.set_credentials_file(username=user, api_key=API)

file_path = filedialog.askopenfilename()
tree = ET.parse(file_path)
root = tree.getroot()


names=[]

for test in root.iter(address+'Test'):
    temp=str(test.attrib)

    names.append(temp)
    print(names)


sizesArrays = []
sizes=[]
i=0
j=0
for size in root.iter( address2 + 'particleSize'):

    print(i)
    if sizes != []:
        if float(size.text) > sizes[len(sizes)-1]:
            i += 1
            j = 0
            sizesArrays.append(sizes)
            sizes=[]

    sizes.append(float(size.text))
    print(sizes)

print(sizesArrays)


passingArrays = []
i=0
j=0
percentPassing=[]
for passing in root.iter(address2 +'percentPassing'):
    print(i)
    if percentPassing != []:
        if float(passing.text) > percentPassing[len(percentPassing) - 1]:
            i += 1
            j = 0
            passingArrays.append(percentPassing)
            percentPassing = []

    percentPassing.append(float(passing.text))
    print(percentPassing)

print(passingArrays)



i=0
data=[]
for x in range(0,len(names)-1):
    trace=go.Scatter(
        x = sizesArrays[i],
        y = passingArrays[i],
        name = names[i],
        line = dict(
            color = ('rgb(i*10,i*10,i*10)'),
            width = 4
        )
    )
    i+=1
    data.append(trace)
layout = dict(title = 'Seive Analysis',
              xaxis = dict(title = 'Sieve Size(mm)',
                          type = 'log'),

              yaxis = dict(title = 'Percent Passing(%)'),
              )
fig = dict(data=data,layout=layout)
py.iplot(fig, filename = graphName)

