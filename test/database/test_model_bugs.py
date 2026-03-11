"""
Тесты, выявляющие баги в моделях.
"""

import pytest
from .helpers import gen_id
from shoersshopapi.core.database.models.favorite import Favorite


class TestFavoriteMixinBug:
    """
    BUG: В Favorite дважды присваивается один и тот же атрибут:

        _user_back_populates = "favorites"
        _user_back_populates = "joined"      ← перезаписал!
        _product_back_populates = "favorites"
        _product_back_populates = "joined"   ← перезаписал!

    Итог: оба = "joined", а должны быть "favorites".
    Скорее всего хотели:
        _user_load_strategy = "joined"
        _product_load_strategy = "joined"
    """

    def test_user_back_populates_overwritten(self):
        actual = Favorite._user_back_populates
        assert actual == "favorites", (
            f"BUG: Favorite._user_back_populates = '{actual}'. "
            f"Ожидается 'favorites'. Строка '_user_back_populates = \"joined\"' "
            f"перезаписала предыдущую. "
            f"Вероятно нужно: _user_load_strategy = 'joined'"
        )

    def test_product_back_populates_overwritten(self):
        actual = Favorite._product_back_populates
        assert actual == "favorites", (
            f"BUG: Favorite._product_back_populates = '{actual}'. "
            f"Ожидается 'favorites'. Строка '_product_back_populates = \"joined\"' "
            f"перезаписала предыдущую. "
            f"Вероятно нужно: _product_load_strategy = 'joined'"
        )

    @pytest.mark.asyncio
    async def test_favorite_creates_despite_bug(
        self, session, sample_user, sample_product
    ):
        """FK работают, но relationship User.favorites будет сломан."""
        fav = Favorite(
            id=gen_id(),
            user_id=sample_user.id,
            product_id=sample_product.id,
        )
        session.add(fav)
        await session.flush()
        assert fav.id is not None