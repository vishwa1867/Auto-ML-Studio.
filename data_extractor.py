import os
import pandas as pd
import re
from typing import Dict, Any, List
import spacy

# Load spaCy model for entity recognition
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("Error: spaCy model 'en_core_web_sm' not found. Install it with:")
    print("python -m spacy download en_core_web_sm")
    nlp = None

def clean_text(text: str) -> str:
    """Clean up the text by removing extra spaces and newlines."""
    text = str(text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def extract_entities(text: str) -> Dict[str, List[str]]:
    """Extract entities like names, dates, and addresses from text."""
    entities = {"names": [], "dates": [], "addresses": []}
    text = clean_text(text)
    
    # Extract dates using regex
    date_patterns = [
        r'\b\d{1,2}/\d{1,2}/\d{4}\b',
        r'\b\d{1,2}-\d{1,2}-\d{4}\b',
        r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{1,2},?\s+\d{4}\b',
        r'\b\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{4}\b'
    ]
    for pattern in date_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        entities["dates"].extend(matches)
    
    entities["dates"] = list(set(entities["dates"]))  # Remove duplicates
    
    # Use spaCy for named entity recognition if available
    if nlp:
        try:
            doc = nlp(text)
            for ent in doc.ents:
                if ent.label_ == "PERSON":
                    entities["names"].append(ent.text)
                elif ent.label_ in ["GPE", "LOC", "FAC"]:
                    entities["addresses"].append(ent.text)
        except Exception as e:
            print(f"Error in spaCy processing: {e}")
    
    entities["names"] = list(set(entities["names"]))  # Remove duplicates
    entities["addresses"] = list(set(entities["addresses"]))
    
    return entities

def data_extraction(file_path: str) -> Dict[str, Any]:
    """Extract structured data and entities from a CSV file."""
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    if not file_path.lower().endswith(".csv"):
        raise ValueError("Only CSV files are supported")
    
    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        raise RuntimeError(f"Error reading CSV file: {e}")
    
    df = df.fillna("")  # Replace NaN with empty strings
    
    # Combine all text content for entity extraction
    all_text = " ".join(df.astype(str).apply(lambda x: " ".join(x), axis=1))
    entities = extract_entities(all_text)
    
    # Create structured data from the CSV
    structure = []
    for _, row in df.iterrows():
        structure.append({col: clean_text(row[col]) for col in df.columns})
    
    return {
        "entities": entities,
        "columns": list(df.columns),
        "rows": structure,
        "preview": structure[:5]  # First 5 rows for preview
    }

def main():
    """Example usage."""
    file_path = "your_csv_file.csv"  # Update this to the path of your CSV file
    
    try:
        result = data_extraction(file_path)
        
        print("=== CSV EXTRACTION RESULTS ===")
        print(f"Entities found: {len(result['entities']['names'])} names, "
              f"{len(result['entities']['dates'])} dates, "
              f"{len(result['entities']['addresses'])} addresses")
        
        print(f"\nColumns: {result['columns']}")
        print(f"First 5 rows preview:")
        from pprint import pprint
        pprint(result["preview"])
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
