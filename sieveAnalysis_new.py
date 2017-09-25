import xml.etree.ElementTree as ET
from bokeh.plotting import figure, output_file, show
from bokeh.models import HoverTool
from bokeh.palettes import Paired12
from bokeh.models.widgets import Div
from bokeh.layouts import layout
from bokeh.io import curdoc
import itertools


xml_file = 'Geosyntec.xml'

# Read the XML file
tree = ET.parse(xml_file)
root = tree.getroot()


# Extract DIGGSML version
# TO-DO: test with other versions and improve with regex
version = root.tag[-11:-6]


# Address for test names
name_address = '{http://diggsml.org/schemas/' + version +'}'

# Address for geotechnical data
geo_address = '{http://diggsml.org/schemas/' + version +'/geotechnical}'



# Start dictionary that will hold the results
sieve_results = {}

for test in root.iter(name_address + 'Test'):

    # Extract the test names
    test_name = test.get(test.keys()[0])[16:-1]

    # Extract sieve opening and percent passing for each test
    psize_list = []
    ppassing_list = []

    for grading in test.iter(geo_address + 'Grading'):

        for particle_size, percent_passing in zip(
                grading.findall(geo_address + 'particleSize'),
                grading.findall(geo_address + 'percentPassing')):
            psize_list.append(float(particle_size.text))
            ppassing_list.append(float(percent_passing.text))

    # Add test results to the main dictionary
    sieve_results[test_name] = {'particle_size' : psize_list,
                                'percent_passing' : ppassing_list}



##############################################################################
###                             BOKEH PLOTTING                             ###
##############################################################################

hover = HoverTool(tooltips=[
    ("Sieve Size (mm)", "($x)"),
    ("Passing (%)", "($y)")])


p = figure(plot_width = 900,
           plot_height = 550,
           x_axis_type = "log",
           title = 'Sieve Analysis',
           tools='pan,save,reset,hover')

p.xaxis.axis_label = 'Sieve size (mm)'
p.yaxis.axis_label = 'Percent Passing'

p.background_fill_color = "gray"
p.background_fill_alpha = 0.1


for i, c in zip(sieve_results.keys(), itertools.cycle(Paired12)):
    p.line(x = sieve_results[i]['particle_size'],
           y = sieve_results[i]['percent_passing'],
           line_width = 2.5,
           legend = i,
           color = c)
    p.circle(x = sieve_results[i]['particle_size'],
           y = sieve_results[i]['percent_passing'],
           fill_color="white", size=7,
           color = c)

p.legend.location = "top_left"


##############################################################################
###                          SET UP HEADER/FOOTER                          ###
##############################################################################

# Page header and footer
page_header = Div(text = """
            <style>
            h1 {
                margin: 1em 0 0 0;
                color: #2e484c;
                font-family: 'Julius Sans One', sans-serif;
                font-size: 1.8em;
                text-transform: uppercase;
            }
            a:link {
                font-weight: bold;
                text-decoration: none;
                color: #0d8ba1;
            }
            a:visited {
                font-weight: bold;
                text-decoration: none;
                color: #1a5952;
            }
            a:hover, a:focus, a:active {
                text-decoration: underline;
                color: #9685BA;
            }
            p {
                text-align: justify;
                text-justify: inter-word;
                /*font: "Libre Baskerville", sans-serif;
                width: 90%;
                max-width: 940;*/
            }
            small {
                color: #424242;
            }

            p.big {
                margin-bottom: 0.8cm;
            }

            </style>
            <h1>DIGGS Sieve Analysis Graph (Demo)</h1>
            <p>
            This online tool retrieves and plots the results of the sieve analyses of multiple tests stored in a DIGGSML file. Click <a href="https://github.com/DIGGSml/diggs-graph-demo/blob/master/Geosyntec.xml" target="_blank">here</a><br /> to view the file and its contents.
            </p>
            <br />
            <hr />
            <br />
            """
,width = 940)

page_footer = Div(text = """
            <br>
            <hr>
            <br>
            <div>
                <div align="left">
                  <a href="http://diggsml.org/" target="_blank">
                    <img src="media/DIGGSML_logo.png" style="float:left" onerror="this.src='http://diggsml.org/sites/default/files/joint-logos.png'" width="20%">
                  </a>
                </div>
                <div align="right" style="color:gray">
                    Developed by:<br>
                    <a href="https://github.com/gyrosphere" target="_blank">Tom Cadden</a><br />
                    <a href="https://github.com/nickmachairas" target="_blank">Nick Machairas</a>
                </div>
            </div>
            """
,width = 940)




##############################################################################
###                             SET UP LAYOUT                              ###
##############################################################################

# Set up initial page layout
page_layout = layout([[page_header],
                      [p],
                      [page_footer]],
                      width = 940)


# Add the page layout to the current document
curdoc().add_root(page_layout)
curdoc().title = "DIGGS Sieve Analysis"



# run with:
# bokeh serve --show sieveAnalysis_new.py
