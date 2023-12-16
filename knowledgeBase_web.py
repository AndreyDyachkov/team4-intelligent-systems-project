from rdflib import Graph

def perform_sparql_query(query):
    knowledge_base = Graph()
    knowledge_base.parse(file=open("Project_knowledge_base_v2.n3", "r"), format="text/n3")
    # Perform SPARQL query on the knowledge base
    result = knowledge_base.query(query)
    dict ={}
    for row in result:
        label = str(row.asdict()['label'].toPython())
        threshold = str(row.asdict()['threshold'].toPython())
        dict[label] = threshold
    return dict




