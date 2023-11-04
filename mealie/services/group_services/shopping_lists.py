from typing import cast

from pydantic import UUID4

from mealie.core.exceptions import UnexpectedNone
from mealie.repos.repository_factory import AllRepositories
from mealie.schema.group import ShoppingListItemCreate, ShoppingListOut
from mealie.schema.group.group_shopping_list import (
    ShoppingListCreate,
    ShoppingListItemBase,
    ShoppingListItemOut,
    ShoppingListItemRecipeRefCreate,
    ShoppingListItemRecipeRefOut,
    ShoppingListItemsCollectionOut,
    ShoppingListItemUpdate,
    ShoppingListItemUpdateBulk,
    ShoppingListMultiPurposeLabelCreate,
    ShoppingListSave,
)
from mealie.schema.recipe.recipe_ingredient import IngredientFood, IngredientUnit, RecipeIngredient
from mealie.schema.response.pagination import OrderDirection, PaginationQuery
from mealie.schema.user.user import GroupInDB


class ShoppingListService:
    def __init__(self, repos: AllRepositories, group: GroupInDB):
        self.repos = repos
        self.group = group
        self.shopping_lists = repos.group_shopping_lists
        self.list_items = repos.group_shopping_list_item
        self.list_item_refs = repos.group_shopping_list_item_references
        self.list_refs = repos.group_shopping_list_recipe_refs

    @staticmethod
    def can_merge(item1: ShoppingListItemBase, item2: ShoppingListItemBase) -> bool:
        """Check to see if this item can be merged with another item"""

        # Extract the ingredient name from the note
        def get_ingredient_name(note):
            if note:
                words = note.split()
                if words[0].lower() not in ['salt', 'pepper', 'oil']:
                    return words[0]
            return None

        note1 = get_ingredient_name(item1.note)
        note2 = get_ingredient_name(item2.note)

        if any(
            [
                item1.checked,
                item2.checked,
                item1.food_id != item2.food_id,
                item1.unit_id != item2.unit_id,
                note1 != note2,
            ]
        ):
            return False

        # if foods match, we can merge, otherwise compare the notes
        return bool(item1.food_id) or note1 == note2

    ...(rest of the code remains the same)...
