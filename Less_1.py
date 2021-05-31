from pathlib import Path
import json
import time
import requests

class CategoriesParser(Parse5ka):
    headers = {"User-Agent": "StepanovVV"}
    def __init__(self, categories_url, *args, **kwargs):
        self.categories_url = categories_url
        super().__init__(*args, **kwargs)

    def _get_categories(self):
        response = self._get_response(self.categories_url)
        data = response.json()
        return data

    def run(self):
        for category in self._get_categories():
            category["products"] = []
            params = f"?categories={category['parent_group_code']}"
            url = f"{self.start_url}{params}"

            category["products"].extend(list(self._parse(url)))
            file_name = f"{category['parent_group_code']}.json"
            cat_path = self.save_dir.joinpath(file_name)
            self._save(category, cat_path)


def get_dir_path(dir_name: str) -> Path:
    dir_path = Path(__file__).parent.joinpath(dir_name)
    if not dir_path.exists():


if __name__ == "__main__":
    url = "https://5ka.ru/api/v2/special_offers/"
    save_dir = get_dir_path("products")
    parser = Parse5ka(url, save_dir)
    parser.run()
    category_url = "https://5ka.ru/api/v2/categories/"
    product_path = get_dir_path("products")
    parser = Parse5ka(url, product_path)
    category_parser = CategoriesParser(category_url, url, get_dir_path("category_products"))
    category_parser.run()