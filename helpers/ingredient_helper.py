class IngredientHelper:

    @staticmethod
    def select_ingredients_for_order(ingredients_list):
        """
        Сложная логика выбора ингредиентов для заказа.
        """
        categorized = {
            "bun": [],
            "sauce": [],
            "main": []
        }

        for ingredient in ingredients_list:
            ing_type = ingredient.get("type")
            ing_id = ingredient.get("_id")

            if ing_type in categorized and ing_id:
                categorized[ing_type].append(ing_id)

        selected = []

        # Добавляем булку, если есть
        if categorized["bun"]:
            selected.append(categorized["bun"][0])
        if categorized["sauce"]:
            selected.append(categorized["sauce"][0])
        if categorized["main"]:
            selected.append(categorized["main"][0])

        return selected

    @staticmethod
    def get_fallback_ingredients():
        """
        Возвращает fallback ингредиенты для тестов.
        Используется, когда API недоступно.
        """
        return [
            "61c0c5a71d1f82001bdaaa6d",  # bun (Флюоресцентная булка R2-D3)
            "61c0c5a71d1f82001bdaaa70",  # sauce (Соус Spicy-X)
            "61c0c5a71d1f82001bdaaa6f"  # main (Мясо бессмертных моллюсков Protostomia)
        ]