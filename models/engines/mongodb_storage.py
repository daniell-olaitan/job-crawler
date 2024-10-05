#!/usr/bin/env python3
"""
Module that abstracts mongodb storage
"""
import typing as t
from mongoengine import (
    connect,
    disconnect,
    get_db
)
from os import getenv
from datetime import datetime
from mongoengine import Document


class MongoDBStorage:
    """
    Class that abstracts mongodb storage
    """
    def __init__(self):
        self.db_name = getenv('DB_NAME', 'job_crawler_db')
        self.db_host = getenv('DB_HOST', 'localhost')
        self.db_port = int(getenv('DB_PORT', 27017))

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

            doc.updated_at = datetime.now()
            doc.save()

        return self.find(collection, id=id)

    def delete(self, collection: t.Type[Document], id: str) -> None:
        """
        Delete a document from the collection
        """
        doc = self.find(collection, id=id)
        doc.delete()

    def drop_database(self):
        connect(self.db_name, host=self.db_host, port=self.db_port)
        db = get_db()
        db.client.drop_database(db.name)
        disconnect()
