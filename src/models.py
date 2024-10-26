import json
import os
from typing import Any, Dict, List, Optional


class JSONModel:
    def __init__(self, json_file: str):
        """
        Initialize the JSONModel with the file path to store the JSON data.
        """
        self.json_file = json_file
        self._data: List[Dict[str, Any]] = []
        self._load()

    def _load(self) -> None:
        """
        Load data from the JSON file if it exists; otherwise, initialize with an empty list.
        """
        if os.path.exists(self.json_file):
            with open(self.json_file, "r") as file:
                try:
                    self._data = json.load(file)
                except json.JSONDecodeError:
                    self._data = []
        else:
            self._data = []

    def _save(self) -> None:
        """
        Save the current data to the JSON file.
        """
        with open(self.json_file, "a") as file:
            json.dump(self._data, file, indent=2)

    def create(self, item: Dict[str, Any]) -> None:
        """
        Add a new item to the data and persist to JSON.
        """
        self._data.append(item)
        self._save()

    def read_all(self) -> List[Dict[str, Any]]:
        """
        Return all items in the data.
        """
        return self._data

    def read_by_id(self, item_id: Any) -> Optional[Dict[str, Any]]:
        """
        Find an item by its unique 'id' field.
        """
        return next((item for item in self._data if item.get("id") == item_id), None)

    def update(self, item_id: Any, updates: Dict[str, Any]) -> bool:
        """
        Update an existing item by 'id' with the provided updates.
        """
        for item in self._data:
            if item.get("id") == item_id:
                item.update(updates)
                self._save()
                return True
        return False

    def delete(self, item_id: Any) -> bool:
        """
        Delete an item by its 'id'.
        """
        for i, item in enumerate(self._data):
            if item.get("id") == item_id:
                del self._data[i]
                self._save()
                return True
        return False
