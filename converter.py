# This is a helper function to convert Choo-Choo Charles location.py file to use with location_mapping.lua and the location jsons
# Not called in the poptracker but is useful for others want to tinker with their own poptracker the way i did it
import tkinter as tk
import pyperclip
from tkinter.filedialog import askopenfilename
from tkinter.simpledialog import askstring
tk.Tk().withdraw()

fn = askopenfilename()
filt_location = askstring("What location","here")

check = "hello"
is_scrap = False
location = ""
location_cap= ""
base_id = 66600000
prnt = ""
with open(fn) as f:
  for line in f.readlines():
    if "loc_" in line:
      location = line[4:-5]
      location_cap = location.replace("_"," ")
      location_cap = location_cap.title()
      continue
    if location_cap not in filt_location: # Skip if not id
      continue
    if "base_id " not in line: # Skip if not id
      continue
    is_scrap = "Scraps" in line
    check = line.split('"')[1]
    if "-" in line:
      if is_scrap:
        check = check.split(' - ')[1]
    else:
      if location_cap in check:
        check = check[len(location):]
    if "Chest" in line and is_scrap:
      is_scrap = False
      check = "Chest"
    id_pos = line.index("base_id")+10
    if line[id_pos:][:4].isdigit():
      id = base_id + int(line[id_pos:][:4])
    else:
      id = -1

    # Use this for location_mapping
    #l = '    [{0}] = {{{{"@Aranerarum/{1}/{2}"}},{{"@{1}/{3}/{4}"}}}},'.format(id,location_cap,(check, "Scraps")[is_scrap],check,("", "Scraps")[is_scrap])
    
    # Use this for location .json files
    l = '      {{\n        "name": "{3}",\n        "sections": [{{\n          "name": "{2}",\n          "chest_unopened_img": "images/chests/scraps.png",\n          "chest_opened_img": "images/chests/scraps_true.png"\n        }}],\n        "map_locations": [\n          {{\n            "map": "{1}",\n            "x": 0,\n            "y": 0\n          }}\n        ]\n      }},'.format(id,location,(check, "Scraps")[is_scrap],check,("", "Scraps")[is_scrap])
    print(l)
    prnt += l + "\n"
    
  pyperclip.copy(prnt)