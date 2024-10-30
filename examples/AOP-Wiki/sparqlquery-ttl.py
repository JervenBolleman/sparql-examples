import os

# Define the directory to search for .rq files and the output TTL file name
input_directory = "AOPWikiSNORQL"  # Cloned directory within the GitHub Actions workspace
ttl_output_file = "AOP-Wiki-SPARQL-examples.ttl"  # Output TTL file

# Define schema target and contributor name
schema_target = "https://aopwiki.rdf.bigcat-bioinformatics.org/sparql/"
contributor = "Marvin Martens"

# Write the header to the output TTL file
with open(ttl_output_file, "w") as ttl_file:
    ttl_file.write("""
@prefix ex: <https://bigcat-um.github.io/sparql-examples/AOP-Wiki/> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix schema: <https://schema.org/> .
@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix dc: <http://purl.org/dc/elements/1.1/> .

""")

# Counter for unique identifiers in the Turtle file
ex_counter = 0

# Walk through all files in the input directory and subdirectories
for root, dirs, files in os.walk(input_directory):
    for file in files:
        if file.endswith(".rq"):
            # Construct full file path
            sparql_query_file = os.path.join(root, file)
            
            # Read the SPARQL query from the .rq file
            with open(sparql_query_file, "r") as query_file:
                sparql_query = "".join(
                    line for line in query_file if not line.strip().startswith("PREFIX")
                )

            # Append each query as a new SPARQLExecutable block to the TTL file
            with open(ttl_output_file, "a") as ttl_file:
                ttl_file.write(f"""
ex:{ex_counter} a sh:SPARQLExecutable,
       sh:SPARQLSelectExecutable ;
    rdfs:comment "[fill out comment here]"@en ;
    sh:prefixes _:sparql_examples_prefixes ;
""")
                
                # Insert the SPARQL query content
                ttl_file.write(f'    sh:select """{sparql_query.strip()}""" ;\n')
                
                # Add schema target and contributor information
                ttl_file.write(f'    schema:target <{schema_target}> ;\n')
                ttl_file.write(f'    dc:contributor "{contributor}" .\n\n')
            
            print(f"Added query from '{sparql_query_file}' to '{ttl_output_file}'")
            ex_counter += 1  # Increment identifier for the next entry

print(f"Number of queries added: {ex_counter}")
