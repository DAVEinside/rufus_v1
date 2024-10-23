# rufus/output.py

import json

class OutputAgent:
    def prepare_output(self, scored_data):
        # Instead of limiting to top_n, return all data above evaluation threshold
        structured_documents = []
        for data, score in scored_data:
            structured_doc = {
                'url': data['url'],
                'score': score,
                'content': data['content']
            }
            structured_documents.append(structured_doc)
        # Return the list of structured documents
        return structured_documents
