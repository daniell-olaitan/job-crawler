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
        self.mock_obj = MagicMock()
        self.mock_collection.return_value = self.mock_obj

    def test_insert(self):
        obj = self.db.insert(self.mock_collection, **self.mock_kwargs)

        self.assertEqual(obj, self.mock_obj)
        self.mock_obj.save.assert_called_once()

    def test_find(self):
        mock_objects = self.mock_collection.objects.return_value
        mock_objects.first.return_value = self.mock_obj

        obj = self.db.find(self.mock_collection, **self.mock_kwargs)

        self.assertEqual(obj, self.mock_obj)
        mock_objects.first.assert_called_once()
        self.mock_collection.objects.assert_called_once_with(**self.mock_kwargs)

    def test_find_all(self):
        self.mock_collection.objects.return_value = [self.mock_obj]

        objs = self.db.find_all(self.mock_collection)

        self.assertEqual(objs, [self.mock_obj])
        self.mock_collection.objects.assert_called_once()

    def test_filter(self):
        self.mock_collection.objects.return_value = [self.mock_obj]

        objs = self.db.filter(self.mock_collection, **self.mock_kwargs)

        self.assertEqual(objs, [self.mock_obj])
        self.mock_collection.objects.assert_called_once_with(**self.mock_kwargs)

    # @patch('models.engines.mongodb_storage.MongoDBStorage.find')
    # def test_update(self, mock_find: MagicMock):
    #     mock_find.return_value =
