import spacy

# Load the NLP engine once at the global level
nlp = spacy.load("en_core_web_sm")

def clean_and_analyze(input_path, output_path):
    """
    Reads a file, performs NLP tasks, and writes a structured report.
    """
    # 1. Read the raw file
    with open(input_path, "r", encoding="utf-8") as f:
        raw_text = f.read()

    # 2. Process the text with spaCy
    doc = nlp(raw_text)

    # 3. Prepare the output content
    output_lines = []
    output_lines.append(f"{'TOKEN':<15} | {'LEMMA':<15} | {'POS':<8} | {'ENTITY'}")
    output_lines.append("-" * 55)

    for token in doc:
        # Get the NER label if the token is part of an entity, otherwise 'O'
        entity_label = token.ent_type_ if token.ent_type_ else "O"
        
        line = f"{token.text:<15} | {token.lemma_:<15} | {token.pos_:<8} | {entity_label}"
        output_lines.append(line)

    # 4. Write the results to the output file
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(output_lines))
    
    print(f"Success! Analysis written to {output_path}")

# --- Execution ---
input_file = "raw.txt"
output_file = "output.txt"

clean_and_analyze(input_file, output_file)