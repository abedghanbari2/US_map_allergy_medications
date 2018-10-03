#!/usr/bin/env python

"""
"""
import os
import xlrd
from bs4 import BeautifulSoup
from IPython.display import SVG, display
import cairosvg
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 
import imageio

# Set your working directory
dirname = "/Users/abedghanbari/project_map"
os.chdir(dirname)


drug_allergy = xlrd.open_workbook("wide_2016.xls")

drug_data = drug_allergy.sheet_by_index(0)

# Hash to store median income
drug_use_mg = {}
drug_column = []

# Create income group categories for the colors
p1 = .1
p2 = .5
p3 = 1
p4 = 5
p5 = 10

# Load map of US counties from Wikipedia
us_map = open('USA_Counties_with_FIPS_and_names.svg', 'r' ).read()

# Load US map SVG into Beautiful Soup
soup = BeautifulSoup(us_map, 'lxml')
 
# Find counties
paths = soup.findAll('path')

# County style
path_style = 'font-size:12px;fill-rule:nonzero;stroke:#000000;stroke-opacity:1;stroke-width:0.1;stroke-miterlimit:4;stroke-dasharray:none;stroke-linecap:butt;marker-start:none;stroke-linejoin:bevel;fill:'

# Map colors from Color Brewer 2
colors = ["#FFFFCC", "#D9F0A3", "#ADDD8E", "#78C679", "#31A354", "#006837"] 

filenames=[]
for j in range(1,13):
    # Create FIPS and median income hash function
    for rownum in range(3, drug_data.nrows):
    	
    	try:	
    		complete_fips = int(drug_data.cell(rownum, 0).value)
    		
    		mg_percap1 = float(drug_data.cell(rownum, j).value)
    		drug_use_mg[complete_fips] = mg_percap1
    		drug_column.append(mg_percap1)
    	except:
    		continue
    
    # Color the states based on median income
    for p in paths:
        if p['id'] not in ["State_Lines", "separator"]:
            
            try:
                inc_value = drug_use_mg[int(p['id'][5:])]
            except:
                continue
            try:
                if inc_value > p5:
                    color_class = 5
                elif inc_value > p4:
                    color_class = 4
                elif inc_value > p3:
                    	color_class = 3
                elif inc_value > p2:
                    	color_class = 2
                elif inc_value > p1:
                    	color_class = 1
                else:
                    	color_class = 0
            except:
                continue
            color = colors[color_class]
            p['style'] = path_style + color
    

    # Save SVG
    f = open('drug_mg'+str(j)+'.svg', 'w')
    f.write(soup.prettify())
    f.close()
#    display(SVG('drug_mg'+str(j)+'.svg'))
    cairosvg.svg2png(url='drug_mg'+str(j)+'.svg',parent_width=600, parent_height=350, scale=3, dpi=900,  write_to='drug_mg'+str(j)+'.png')
    filenames.append('drug_mg'+str(j)+'.png')
#%% add month name to each image
months = ['January','February','March','April','May','June','July','August','September','October','November','December']
fill_color = (255,255,255)
for j in range(1,13):
    img = Image.open(filenames[j-1])
    if img.mode in ('RGBA', 'LA'):
        background = Image.new(img.mode[:-1], img.size, fill_color)
        background.paste(img, img.split()[-1])
        img = background

    
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("MODERNE SANS.ttf", 70)
    draw.text((1050, 50),months[j-1],(147,197,114),font=font)
    img = img.convert("RGB")
    img.save(filenames[j-1][:-4]+'.jpg')

#%%
images = []
for filename in filenames:
    images.append(imageio.imread(filename[:-4]+'.jpg'))
imageio.mimsave('drug_use.gif', images, duration=.5)
#%% remove all images PNG and SVG
for i in filenames:
    try:
        os.remove(i[:-4]+'.jpg')
        os.remove(i[:-4]+'.svg')
        os.remove(i)
    except:
        continue
