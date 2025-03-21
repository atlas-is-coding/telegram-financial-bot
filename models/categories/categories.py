"""Работа с категориями расходов"""
from typing import Dict, List, NamedTuple

from database.sqlite import SQLite
from models.categories.model import Category


class Categories:
    def __init__(self, db: SQLite):
        self._categories = self._load_categories()
        self.db = db

    def _load_categories(self) -> List[Category]:
        categories = self.db.fetchall(
            "category", "codename name is_base_expense aliases".split()
        )

        categories = self._fill_aliases(categories)
        return categories

    @staticmethod
    def _fill_aliases(categories: List[Dict]) -> List[Category]:
        categories_result = []

        for index, category in enumerate(categories):
            aliases = category["aliases"].split(",")
            aliases = list(filter(None, map(str.strip, aliases)))
            aliases.append(category["codename"])
            aliases.append(category["name"])
            categories_result.append(Category(
                codename=category['codename'],
                name=category['name'],
                is_base_expense=category['is_base_expense'],
                aliases=aliases
            ))

        return categories_result

    def get_all_categories(self) -> List[Dict]:
        return self._categories

    def get_category(self, category_name: str) -> Category:
        finded = None
        other_category = None
        for category in self._categories:
            if category.codename == "other":
                other_category = category
            for alias in category.aliases:
                if category_name in alias:
                    finded = category
        if not finded:
            finded = other_category
        return finded
