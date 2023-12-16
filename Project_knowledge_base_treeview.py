import os
import tkinter as tk
from tkinter import ttk
import rdflib

root = tk.Tk()
root.title("Treeview Structure") #root.geometry("1200x680+50+20")

KB_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Project_knowledge_base_v2.n3")

knowledge_base = rdflib.Graph()
knowledge_base.parse(file=open(KB_path, "r"), format="text/n3")

treeview = ttk.Treeview(root)

treeview.config(column = ('Details'))
treeview.config(height = 10)
treeview.column('#0', width = 300)
treeview.column('Details', width = 300)

treeview.heading('#0', text = 'Process Names')
treeview.heading('Details', text = 'Details')


qres = knowledge_base.query(
    """SELECT DISTINCT ?label ?class
       WHERE {
          ?class rdf:type classes:Process .
          ?class rdfs:label ?label .
       }""")

for row in qres:
    label_name = str(row.asdict()['label'].toPython())
    class_name = str(row.asdict()['class'].toPython())
    print(label_name)
    print('=======process ind======')
    print(class_name)
    parent = treeview.insert('', 'end' ,label_name, text = label_name, open = True )

qres2 = knowledge_base.query(
    """SELECT DISTINCT ?label ?class
       WHERE {
          ?class prop:SubProcess ind:process0 .
          ?class rdfs:label ?label .
       }""")

for row in qres2:
    sub_label_name = str(row.asdict()['label'].toPython())
    sub_class_name = str(row.asdict()['class'].toPython())
    #print("%s is %s" % row)
    print(sub_label_name)
    print('=====process ind of sub process of proc0=====')
    print(sub_class_name)
    child1 = treeview.insert(parent,'end',sub_label_name, text = sub_label_name, open = True)

proclabel=[label_name,sub_label_name]

treeview.pack(fill='x')
root.mainloop()