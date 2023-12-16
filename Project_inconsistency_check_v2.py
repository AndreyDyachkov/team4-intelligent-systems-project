from rdflib import Graph
import os

# Parse the knowledge base
KB_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Project_knowledge_base_v2.n3")
knowledge_base = Graph()
knowledge_base.parse(file=open(KB_path, "r"), format="text/n3")
print('The lenght of the knowledge base: ',len(knowledge_base))

# Parse the rule base
RB_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Rules_v2.n3")
rule_base = Graph()
rule_base.parse(file=open(RB_path, "r"), format="text/n3")
print('The lenght of the rule base: ',len(rule_base))

# Check for inconsistency

# 1. owl:oneOf
#Any individual that belongs to the class KPI must be either 'kpi0', 'kpi1', 'kpi2', 'kpi3', and no other individual can belong to the class KPI.
#Any individual that belongs to the class resources must be either 'resource0', 'resource1', 'resource2', and no other individual can belong to the class 'resources'.

print('\n-----1.owl:oneOf-----')

# Query to the rule base
rule_base_query_1 = rule_base.query(
            """SELECT DISTINCT ?t4class ?t4values
               WHERE {
                  ?t4class owl:oneof ?t4values.
               }""")
my_dict_1 = {'KPI':[],
           'resources':[]}
for row in rule_base_query_1:
  t4class = str(row.asdict()['t4class'].toPython().split(":")[2])
  t4values = str(row.asdict()['t4values'].toPython().split(":")[2])
  if t4class not in my_dict_1:
    my_dict_1[t4class] = t4values
  else:
    my_dict_1[t4class].append(t4values)

# Query to the knowledge base
knowledge_base_query_1 = knowledge_base.query(
"""
SELECT ?subject ?predicate ?object
WHERE {
  ?subject ?predicate ?object.
  FILTER (
    ?predicate = prop:hasKPI || ?predicate = prop:hasResource
  )
}
""")
my_dict_2 = {'hasKPI':[],
             'hasResource':[]}

for row in knowledge_base_query_1:
    predicate = str(row.asdict()['predicate'].toPython().split(":")[2])
    t4_object = str(row.asdict()['object'].toPython().split(":")[2])
    if predicate not in my_dict_2:
      my_dict_2[predicate] = t4_object
    else:
      my_dict_2[predicate].append(t4_object)

# Check for inconsistency
for key, value in my_dict_2.items():
  if key =='hasKPI':
    for item in value:
      if item in my_dict_1['KPI']:
        print(item+' --  in list')
      else:
        print("Inconsistency Found in item  "+item)
  if key =='hasResource':
    for item in value:
      if item in my_dict_1['resources']:
        print(item+' --  in list')
      else:
        print("Inconsistency Found in item  "+item)

# 2.owl:disjointWith
# Any individual that belongs to the class KPI cannot belong to the class resources and vice versa.
print('\n-----2.owl:disjointWith-----')

# Query to the rule base
rule_base_query_2 = rule_base.query(
            """SELECT DISTINCT ?t4class ?t4values
               WHERE {
                  ?t4class owl:disjointWith ?t4values.
               }""")
my_dict_3 = {}
for row in rule_base_query_2:
  t4class = str(row.asdict()['t4class'].toPython().split(":")[2])
  t4values = str(row.asdict()['t4values'].toPython().split(":")[2])
  my_dict_3[t4class] = t4values

# Query to the knowledge base
knowledge_base_query_2 = knowledge_base.query(
"""
SELECT ?subject ?predicate ?object
WHERE {
  ?subject rdf:type ?object.
  FILTER (
    ?object = classes:KPI || ?object = classes:resources
  )
}
""")
my_dict_4 = {'classKPI':[],
              'classresources':[]}
for row in knowledge_base_query_2:
  t4_subject = str(row.asdict()['subject'].toPython().split(":")[2])
  t4_object = str(row.asdict()['object'].toPython().split(":")[1])
  if t4_object not in my_dict_4:
      my_dict_4[t4_object] = t4_subject
  else:
      my_dict_4[t4_object].append(t4_subject)

# Check for inconsistency
for key, value in my_dict_4.items():
  if key =='classKPI':
    for item in value:
      if item in my_dict_4['classresources']:
        print("Inconsistency Found in item  "+item)
      else:
        print(item, "found only in class", key)
  if key =='classresources':
    for item in value:
      if item in my_dict_4['classKPI']:
        print("Inconsistency Found in item  "+item)
      else:
        print(item, "found only in class", key)


# 3.owl:IrreflexiveProperty
# Any individual that has the property hasKPI with another individual cannot have the same property with itself.
# Any statement using the property hasKPI cannot have the same resource as both the subject and the object
print('\n-----3.owl:IrreflexiveProperty-----')

# Query to the rule base
rule_base_query_3 = rule_base.query(
            """SELECT DISTINCT ?t4_subject
               WHERE {
                  ?t4_subject a owl:IrreflexiveProperty.
               }""")
my_list_1 = []
for row in rule_base_query_3:
  t4_subject = str(row.asdict()['t4_subject'].toPython().split(":")[2])
  my_list_1.append(t4_subject)

# Query to the knowledge base
knowledge_base_query_3 = knowledge_base.query(
"""
SELECT ?subject ?object
WHERE {
  ?subject prop:hasKPI ?object.
  }
""")
subject_list_1 =[]
object_list_1 = []
for row in knowledge_base_query_3:
  t4_subject = str(row.asdict()['subject'].toPython().split(":")[2])
  t4_object = str(row.asdict()['object'].toPython().split(":")[2])
  subject_list_1.append(t4_subject)
  object_list_1.append(t4_object)

# Check for inconsistency
for i in range(len(subject_list_1)):
  if subject_list_1[i] == object_list_1[i]:
    print("Inconsistency Found in pair  ",subject_list_1[i],object_list_1[i])
  else:
    print(subject_list_1[i],' and ', object_list_1[i] ,"are different")

# 4.owl:AsymmetricProperty
#If one individual has hasResource property with another individual, then the second individual cannot have the same hasResource property with the first individual.
print('\n-----4.owl:AsymmetricProperty-----')

# Query to the rule base
rule_base_query_4 = rule_base.query(
            """SELECT DISTINCT ?t4_subject
               WHERE {
                  ?t4_subject a owl:AsymmetricProperty.
               }""")
my_list_2 = []
for row in rule_base_query_4:
  t4_subject = str(row.asdict()['t4_subject'].toPython().split(":")[2])
  my_list_2.append(t4_subject)

# Query to the knowledge base
knowledge_base_query_4 = knowledge_base.query(
"""
SELECT ?subject ?object
WHERE {
  ?subject prop:hasResource ?object.
  }
""")
my_list_5 = []
for row in knowledge_base_query_4:
  t4_subject = str(row.asdict()['subject'].toPython().split(":")[2])
  t4_object = str(row.asdict()['object'].toPython().split(":")[2])
  my_list_5.append((t4_subject,t4_object))

# Check for inconsistency
for i in my_list_5:
  tutuple = (i[1],i[0])
  if tutuple in my_list_5:
    print("Inconsistency Found in pair  ", i)
  else:
    print(i, "follows the rule")