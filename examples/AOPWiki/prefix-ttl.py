import pandas as pd

# Load the TSV file with prefixes
df = pd.read_csv("./AOP-Wiki-prefixes.tsv", sep="\t")

# Define the path to the existing prefixes.ttl file (one folder up)
ttl_filename = "../prefixes.ttl"

# Open the existing TTL file in append mode
with open(ttl_filename, "a") as ttl_file:
    # Check if the file is initially empty to add header information if needed
    if ttl_file.tell() == 0:  # If the file is empty, write header
        ttl_file.write('''
@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
_:aopwiki_sparql_examples_prefixes a owl:Ontology ;
  rdfs:comment """This is a collection of SPARQL prefixes that are needed for the examples for use on different websites.""" ;
  owl:imports sh: .
''')

    # Append individual prefix declarations to the TTL file
    for _, row in df.iterrows():
        prefix, uri = row['Prefix'], row['URI']
        
        # Write the SHACL prefix declaration for each entry
        ttl_file.write(f"_:sparql_examples_prefixes sh:declare _:prefix_{prefix} .\n")
        ttl_file.write(f"_:prefix_{prefix} sh:prefix \"{prefix}\" ;\n")
        ttl_file.write(f"  sh:namespace \"{uri}\"^^xsd:anyURI .\n\n")

print(f"Prefixes successfully appended to '{ttl_filename}'.")
