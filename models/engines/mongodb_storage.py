#!/usr/bin/env python3
"""
Module that abstracts mongodb storage
"""
import typing as t
from datetime import datetime
from mongoengine import Document


class MongoDBStorage:
    """
    Class that abstracts mongodb storage
    """

    def insert(self, collection: t.Type[Document], **kwargs: t.Mapping) -> Document:
        """
        Create and insert new document in the collection
        """
        doc = collection(**kwargs)
        doc.pre_save()
        doc.save()

        return doc

    def find(self, collection: t.Type[Document], **kwargs: t.Mapping) -> Document:
        """
        Fetch a document in the collection by attributes
        """
        return collection.objects(**kwargs).first()

    def find_all(self, collection: t.Type[Document]) -> t.List[Document]:
        """
        Fetch all the documents in a collection
        """
        return list(collection.objects())

    def filter(
        self,
        collection: t.Type[Document],
        **kwargs: t.Mapping
    ) -> t.List[Document]:
        """
        Filter documents based on attributes
        """
        return list(collection.objects(**kwargs))

    def update(
        self,
        collection: Document,
        id: str,
        **kwargs: t.Mapping
    ) -> Document:
        """
        Update a document in collection
        """
        doc = self.find(collection, id=id)
        if doc:
            for key, val in kwargs.items():
                setattr(doc, key, val)

            self.updated_at = datetime.now()
            doc.save()

        return self.find(collection, id=id)

    def delete(self, collection: t.Type[Document], id: str) -> None:
        """
        Delete a document from the collection
        """
        doc = self.find(collection, id=id)
        doc.delete()
