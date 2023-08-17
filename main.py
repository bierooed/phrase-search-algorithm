from typing import List, Dict
import os
def read_text_fragments(file_path: str) -> List[str]:
    with open(file_path, 'r') as f:
        fragments = f.readlines()
        return [fragment.strip() for fragment in fragments if fragment.strip()]


def extract_and_combine_text_fragments(folder_path: str) -> Dict[str, List[str]]:
    texts_fragments_dict = {}

    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):
            fragments = read_text_fragments(file_path)
            texts_fragments_dict[file_name] = fragments
    return texts_fragments_dict


class InvertedIndex:
    def __init__(self):
        self.index = {}

    def add_document(self, doc_id, fragment):
        translation_table = str.maketrans("", "", ".,()")  # Таблица для удаления символов
        cleaned_fragment = fragment.translate(translation_table)
        tokens = cleaned_fragment.lower().split()
        for token in tokens:
            if token not in self.index:
                self.index[token] = []
            self.index[token].append(doc_id)

    def search(self, query):
        query_tokens = query.lower().split()
        doc_matches = {}
        for token in query_tokens:
            if token in self.index:
                for doc_id in self.index[token]:
                    if doc_id not in doc_matches:
                        doc_matches[doc_id] = set()
                    doc_matches[doc_id].add(token)

        result = []
        for doc_id, matched_tokens in doc_matches.items():
            if len(matched_tokens) == len(query_tokens):
                result.append(doc_id)

        return result

    def get_fragment(self, doc_id, fragment_idx):
        if doc_id in documents and 0 <= fragment_idx < len(documents[doc_id]):
            return documents[doc_id][fragment_idx]
        return None


documents = extract_and_combine_text_fragments('./text_files')

inverted_index = InvertedIndex()

for doc_id, fragments in documents.items():
    for fragment in fragments:
        inverted_index.add_document(doc_id, fragment)

query = "Berisha is elected chairman of the Democratic Party"
search_results = inverted_index.search(query)
for doc_id in search_results:
    matching_fragments = [fragment for fragment in documents[doc_id] if sum(1 for token in query.lower().split() if token in fragment.lower()) >= len(query.split())]
    for fragment in matching_fragments:
        print(f"Found in document: {doc_id}, fragment: {fragment}")
