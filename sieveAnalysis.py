import plotly
import plotly.plotly as py
import plotly.graph_objs as go
plotly.tools.set_credentials_file(username='TomCadden', api_key='O3t8TE5Xl17vsVPTwgSJ')
import xml.etree.ElementTree as ET
import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()

file_path = filedialog.askopenfilename()
tree = ET.parse(file_path)
root = tree.getroot()


names=[]
for test in root.iter('{http://diggsml.org/schemas/2.1.a}Test'):
    temp=str(test.attrib)

    names.append(temp[56:-2])
    print(names)


sizesArrays = []
sizes=[]
i=0
j=0
for size in root.iter('{http://diggsml.org/schemas/2.1.a/geotechnical}particleSize'):

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
for passing in root.iter('{http://diggsml.org/schemas/2.1.a/geotechnical}percentPassing'):
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
py.iplot(fig, filename = 'styled-line')

