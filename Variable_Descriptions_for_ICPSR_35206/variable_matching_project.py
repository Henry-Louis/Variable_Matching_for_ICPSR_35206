import os
import re
import PyPDF2
import pandas as pd
import heapq
import json
from typing import Dict, List
from dask import compute, delayed, bag as db


class PdfReader:
    def __init__(self, directory_path: str):
        self.directory_path = directory_path

    def load_pdfs_from_directory(self, recursive: bool = True):
        pdf_texts = {}
        if recursive:
            for root, dirs, files in os.walk(self.directory_path):
                for file_name in files:
                    if file_name.endswith('.pdf'):
                        with open(os.path.join(root, file_name), 'rb') as file:
                            reader = PyPDF2.PdfReader(file)
                            num_pages = len(reader.pages)
                            text = ""
                            for page in range(num_pages):
                                text += reader.pages[page].extract_text()
                            pdf_texts[os.path.join(root, file_name)] = text
        else:
            files = os.listdir(self.directory_path)
            for file_name in files:
                if file_name.endswith('.pdf'):
                    with open(os.path.join(self.directory_path, file_name), 'rb') as file:
                        reader = PyPDF2.PdfReader(file)
                        num_pages = len(reader.pages)
                        text = ""
                        for page in range(num_pages):
                            text += reader.pages[page].extract_text()
                        pdf_texts[os.path.join(self.directory_path, file_name)] = text
        return pdf_texts

    def find_var_descriptions_in_text(self, text: str):
        pattern = re.compile(r'([A-Z]+[0-9]*): (.*)')
        lines = text.split('\n')
        bag = db.from_sequence(lines)
        bag = bag.map(self.find_var_descriptions_in_line, pattern=pattern)
        results = bag.compute()
        matches = {k: v for result in results for k, v in result.items()}
        return matches

    def find_var_descriptions_in_line(self, line: str, pattern: re.Pattern):
        match_dict = {}
        match = pattern.search(line)
        if match:
            match_dict[match.group(1)] = match.group(2)
        return match_dict


class VariableMatcher:
    def __init__(self, list_of_variable_description_dict, list_interested_variable_descriptions):
        self.list_of_variable_description_dict = list_of_variable_description_dict
        self.list_interested_variable_descriptions = list_interested_variable_descriptions

    def preprocess_string(self, input_string):
        input_string = input_string.lower()
        input_string = re.sub(r'[^\w\s$]', '', input_string)
        words_to_remove = {'to', 'for', 'of', 'in', 'a', 'an', 'the'}
        words = input_string.split()
        filtered_words = [word for word in words if word not in words_to_remove]
        return ' '.join(filtered_words)

    def jaccard_similarity(self, desc1, desc2):
        set1 = set(desc1.lower().split())
        set2 = set(desc2.lower().split())
        intersection = set1.intersection(set2)
        union = set1.union(set2)
        return 0.0 if not union else len(intersection) / len(union)

    def jaccard_matching(self, desc, desc_dict):
        desc = self.preprocess_string(desc)
        similarities = [(var, self.jaccard_similarity(self.preprocess_string(desc_dict[var]), desc)) for var in desc_dict]
        top_vars = heapq.nlargest(5, similarities, key=lambda x: x[1])
        return [var for var, _ in top_vars]

    def create_matched_dict(self):
        matched_dict = {}
        for desc in self.list_interested_variable_descriptions:
            matched_dict[desc] = [self.jaccard_matching(desc, desc_dict) for desc_dict in self.list_of_variable_description_dict]
        return matched_dict


def save_to_json(data, file_path):
    with open(file_path, 'w') as outfile:
        json.dump(data, outfile)


def load_from_json(file_path):
    with open(file_path, 'r') as infile:
        return json.load(infile)


if __name__ == "__main__":
    # Replace "path_to_pdfs" with the path to your directory with PDFs
    reader = PdfReader('path_to_pdfs')

    # Load all PDFs from the directory
    pdf_texts = reader.load_pdfs_from_directory(recursive=True)

    # Extract variable descriptions from the PDF texts
    variable_descriptions = [reader.find_var_descriptions_in_text(text) for text in pdf_texts.values()]

    # Replace with your list of interested variable descriptions
    interested_variable_descriptions = ["desc1", "desc2", "desc3"]

    # Create the variable matcher
    matcher = VariableMatcher(variable_descriptions, interested_variable_descriptions)

    # Find the best matches for each interested variable description
    matched_dict = matcher.create_matched_dict()

    # Save the matched variables to a JSON file
    save_to_json(matched_dict, "matched_variables.json")
