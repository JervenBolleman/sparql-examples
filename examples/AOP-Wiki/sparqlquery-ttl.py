import os
import pandas as pd

# Define the directory to search for .rq files and the output TTL file name
input_directory = "AOPWikiSNORQL"  # Directory within the GitHub Actions workspace
ttl_output_file = "AOP-Wiki-SPARQL-examples.ttl"  # Output TTL file

# Define schema target and contributor name
schema_target = "https://aopwiki.rdf.bigcat-bioinformatics.org/sparql/"
contributor = "Marvin Martens"

# Load prefixes from the TSV file into a dictionary
prefixes_df = pd.read_csv("./AOP-Wiki-prefixes.tsv", sep="\t")
prefixes = {row['Prefix']: row['URI'] for _, row in prefixes_df.iterrows()}

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
            
            # Read the SPARQL query from the .rq file and filter out any existing "PREFIX" lines
            with open(sparql_query_file, "r") as query_file:
                query_lines = [line for line in query_file]
                sparql_query = "".join(query_lines)

            # Identify required prefixes based on keywords in the query
            required_prefixes = []
            for prefix, uri in prefixes.items():
                if any(f"{prefix}:" in line for line in query_lines):
                    required_prefixes.append(f"PREFIX {prefix}: <{uri}>\n")

            # Combine required PREFIX statements with the query
            sparql_query_with_prefixes = "".join(required_prefixes) + sparql_query

            # Append each query as a new SPARQLExecutable block to the TTL file
            with open(ttl_output_file, "a") as ttl_file:
                ttl_file.write(f"""
ex:{ex_counter} a sh:SPARQLExecutable,
       sh:SPARQLSelectExecutable ;
    rdfs:comment "[fill out comment here]"@en ;
    sh:prefixes _:sparql_examples_prefixes ;
""")
                
                # Insert the SPARQL query content with prefixes
                ttl_file.write(f'    sh:select """{sparql_query_with_prefixes.strip()}""" ;\n')
                
                # Add schema target and contributor information
                ttl_file.write(f'    schema:target <{schema_target}> ;\n')
                ttl_file.write(f'    dc:contributor "{contributor}" .\n\n')
            
            print(f"Added query from '{sparql_query_file}' to '{ttl_output_file}' with prefixes")
            ex_counter += 1  # Increment identifier for the next entry

print(f"Number of queries added: {ex_counter}")
