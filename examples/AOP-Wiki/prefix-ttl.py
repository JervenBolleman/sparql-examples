import pandas as pd

# Load the TSV file
df = pd.read_csv("./AOP-Wiki-prefixes.tsv", sep="\t")

# Create the TTL file
ttl_filename = "prefixes.ttl"
with open(ttl_filename, "w") as ttl_file:
    # Write TTL header and ontology information
    ttl_file.write("""
@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
_:aopwiki_sparql_examples_prefixes a owl:Ontology ;
  rdfs:comment ""This is a collection of AOP-Wiki SPARQL prefixes that are needed for the examples for use on different websites."" ;
  owl:imports sh: .
""")

    # Iterate over the dataframe to create individual prefix declarations
    for _, row in df.iterrows():
        prefix, uri = row['Prefix'], row['URI']
        
        # Write the SHACL prefix declaration for each entry
        ttl_file.write(f"_:aopwiki_sparql_examples_prefixes sh:declare _:prefix_{prefix} .\n")
        ttl_file.write(f"_:prefix_{prefix} sh:prefix \"{prefix}\" ;\n")
        ttl_file.write(f"  sh:namespace \"{uri}\"^^xsd:anyURI .\n\n")

print(f"Turtle file '{ttl_filename}' created successfully.")
