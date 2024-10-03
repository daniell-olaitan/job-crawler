#!/usr/bin/env python3
"""
Module to test the MongoDBStorage
"""
import unittest
from models.engines.mongodb_storage import MongoDBStorage
from unittest.mock import (
    patch,
    MagicMock
)


class TestMongoDBStorage(unittest.TestCase):
    def setUp(self):
        self.db = MongoDBStorage()
        self.mock_collection = MagicMock()
        self.mock_kwargs = {'name': 'test', 'value': 'mock_test'}
        self.mock_doc = MagicMock()
        self.mock_collection.return_value = self.mock_doc

    def test_insert(self):
        doc = self.db.insert(self.mock_collection, **self.mock_kwargs)

        self.assertEqual(doc, self.mock_doc)
        self.mock_doc.save.assert_called_once()

    def test_find(self):
        mock_objects = self.mock_collection.objects.return_value
        mock_objects.first.return_value = self.mock_doc

        doc = self.db.find(self.mock_collection, **self.mock_kwargs)

        self.assertEqual(doc, self.mock_doc)
        mock_objects.first.assert_called_once()
        self.mock_collection.objects.assert_called_once_with(**self.mock_kwargs)

    def test_find_all(self):
        self.mock_collection.objects.return_value = [self.mock_doc]

        docs = self.db.find_all(self.mock_collection)

        self.assertEqual(docs, [self.mock_doc])
        self.mock_collection.objects.assert_called_once()

    def test_filter(self):
        self.mock_collection.objects.return_value = [self.mock_doc]

        docs = self.db.filter(self.mock_collection, **self.mock_kwargs)

        self.assertEqual(docs, [self.mock_doc])
        self.mock_collection.objects.assert_called_once_with(**self.mock_kwargs)

    @patch('models.engines.mongodb_storage.MongoDBStorage.find')
    def test_update(self, mock_find: MagicMock):
        mock_doc = MagicMock(name='testname', value='testvalue')
        mock_find.return_value = mock_doc
        mock_id = 'uuid'

        doc = self.db.update(self.mock_collection, mock_id, **self.mock_kwargs)

        mock_find.assert_called_with(self.mock_collection, id=mock_id)
        self.assertEqual(doc.name, 'test')
        self.assertEqual(doc.value, 'mock_test')
        mock_doc.save.assert_called_once()

    @patch('models.engines.mongodb_storage.MongoDBStorage.find')
    def test_delete(self, mock_find: MagicMock) -> None:
        mock_find.return_value = self.mock_doc
        mock_id = 'uuid'

        self.db.delete(self.mock_collection, mock_id)

        mock_find.assert_called_with(self.mock_collection, id=mock_id)
        self.mock_doc.delete.assert_called_once()
