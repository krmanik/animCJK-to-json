import os
import json
import re
import html

from xml.dom import minidom

for filename in os.listdir('svgsKana'):
  if filename.endswith('.svg'):
    with open(os.path.join('svgsKana', filename)) as f:
      #print(f)
      name = filename.replace(".svg", "")
      name = html.unescape('&#' + name)
      print(name)
      svg = minidom.parse(f)
      paths = svg.getElementsByTagName('path')

      stroke_path = {}
      median_path = {}
      stroke = ""
      l = ""
      k = ""

      i=0
      j=0
      for node in paths:
        if node.getAttributeNode('id'):
          path_id = str(node.getAttributeNode('id').nodeValue)
          path = str(node.getAttributeNode('d').nodeValue)
          stroke_path[i] = path
          i += 1
        if node.getAttributeNode('clip-path'):
          median_path[j] = "[" + str(node.getAttributeNode('d').nodeValue) + "]"
          j += 1

      i=0
      for i in range(len(stroke_path)):
        stroke = str(stroke_path[i])
        stroke = re.sub(r"(\w)([A-Z])", r"\1 \2 ", stroke)
        stroke = stroke.replace('M', "M ")
        stroke = stroke.rstrip(' ')
        stroke = '"'+ stroke +'",'
        if i == len(stroke_path) - 1:
          stroke = stroke.rstrip(',')
        l += stroke 
        #print(stroke)

      l = '{"strokes" : ['+ l + "],"
      print(l)

      j=0
      for j in range(len(median_path)):
        med = str(median_path[j])
        m = med.replace(" ", "],[")
        m = m.replace("[M],", "")
        m = ",[" + m + "]"
        if j == 0:
          m = m.lstrip(',')
        if j == len(median_path) - 1:
          m = m.rstrip(',')
        k += m 
        #print(m)

      k = '"medians" : ['+ k + "]}"
      print(k)

      f = open(name+".json", "w", encoding="utf-8")
      f.write(l+k)
      f.close()
