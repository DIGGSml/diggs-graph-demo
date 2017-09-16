from bokeh.layouts import column
from bokeh.models import Button
from bokeh.palettes import RdYlBu3
from bokeh.plotting import figure, curdoc
from bokeh.plotting import figure, output_file, show
from bokeh.models import HoverTool
import xml.etree.ElementTree as ET
import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()

version = input("Enter the Diggs schema version (eg '2.0.b'):")
print (version)
address = '{http://diggsml.org/schemas/' + version +'}'
address2= '{http://diggsml.org/schemas/' + version +'/geotechnical}'

file_path = filedialog.askopenfilename()
tree = ET.parse(file_path)
root = tree.getroot()


names=[]
for test in root.iter(address+'Test'):
    temp=str(test.attrib)

    names.append(temp[56:-2])
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

lineColors = ["red","yellow","black","blue","orange","green","purple","brown","coral","cyan","darkgoldenrod","pink","gray","darkmagenta","gold","idigo","olive","salmon","sienna","springgreen","yellow","tan","teal"]
output_file("lines.html")


hover = HoverTool(tooltips=[
    ("(x,y)", "($x, $y)")
])
Tools='hover,xwheel_zoom,box_zoom,reset'
p = figure(tools=Tools,
           title="Diggs Sieve Analysis",
           height=600,width=1000,
           x_axis_type="log", x_range=[0.001,100],
           x_axis_label='Sieve Size',
           y_axis_label='Percent Passing')

i = 0
c = 0

for x in range(0,len(names)-1):
    p.line(sizesArrays[i], passingArrays[i], legend=names[i], line_width=2, line_color=lineColors[c])
    i+=1
    if(c<22):
        c+=1
    else:
        c=0
show(p)

p = figure(x_range=(0, 100), y_range=(0, 100), toolbar_location=None)
p.border_fill_color = 'black'
p.background_fill_color = 'black'
p.outline_line_color = None
p.grid.grid_line_color = None


r = p.text(x=[], y=[], text=[], text_color=[], text_font_size="20pt",
           text_baseline="middle", text_align="center")

i = 0

ds = r.data_source
