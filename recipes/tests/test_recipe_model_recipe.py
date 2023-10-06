from .test_recipe_base import Recipe, RecipeTestBase
from django.core.exceptions import ValidationError
from parameterized import parameterized


class RecipeModelTest(RecipeTestBase):
    def setUp(self) -> None:
        self.recipe = self.make_recipe()
        return super().setUp()

    def make_recipe_no_defaults(self):
        recipe = Recipe(
            category=self.make_category(name='test_default_category'),
            author=self.make_author(username='test_default_author'),
            title='Recipe Title',
            description='Recipe Description',
            slug='recipe-slug',
            preparation_time=10,
            preparation_time_unit='minutes',
            servings=4,
            servings_unit='people',
            preparation_steps='Recipe Preparation Steps',
        )

        recipe.full_clean()
        recipe.save()
        return recipe

    @parameterized.expand([
            ('title', 65),
            ('description', 165),
            ('preparation_time', 65),
            ('servings_unit', 65),
        ])
    def test_recipe_fields_max_lenght(self, field, max_lenght):
        setattr(self.recipe, field, 'A' * (max_lenght + 1))
        with self.assertRaises(ValidationError):
            self.recipe.full_clean()

    def test_recipe_preparation_steps_is_html_is_false_by_default(self):
        recipe = self.make_recipe_no_defaults()

        self.assertFalse(
            recipe.preparation_steps_is_html,
            msg='Recipe preparation_steps_is_html should be False by default.'
            )

    def test_recipe_is_published_is_false_by_default(self):
        recipe = self.make_recipe_no_defaults()

        self.assertFalse(
            recipe.is_published,
            msg='Recipe preparation_steps_is_html should be False by default.'
            )

    def test_recipe_string_representation(self):
        needed = 'testing_representation'
        self.recipe.title = 'testing_representation'
        self.recipe.full_clean()
        self.recipe.save()
        self.assertEqual(
            str(self.recipe), needed,
            msg=f'Recipe string representation must be'
            f' "{needed}" but "{str(self.recipe)}" was received.'
            )
