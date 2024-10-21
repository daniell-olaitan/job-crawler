import os
from mongoengine import Document


# Function to delete a file when a document is deleted
def delete_file(document: Document, path: str, field: str) -> None:
    file = getattr(document, field)
    if file:
        file_path = os.path.join(path, file)
        if os.path.exists(file_path):
            os.remove(file_path)
