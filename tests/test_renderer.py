"""Tests for prompt_expander.renderer."""

import unittest

from prompt_expander.renderer import render, find_variables, unresolved


class RenderTests(unittest.TestCase):
    def test_simple_replacement(self):
        self.assertEqual(
            render("Hello {{name}}!", {"name": "Dylan"}), "Hello Dylan!"
        )

    def test_multiple_occurrences(self):
        self.assertEqual(
            render("{{word}} {{word}} {{word}}", {"word": "AI"}), "AI AI AI"
        )

    def test_whitespace_inside_braces(self):
        self.assertEqual(
            render("Hi {{  name  }}", {"name": "Sam"}), "Hi Sam"
        )

    def test_missing_variable_left_unchanged(self):
        self.assertEqual(
            render("Hi {{name}}, meet {{buddy}}", {"name": "Dylan"}),
            "Hi Dylan, meet {{buddy}}",
        )

    def test_no_variables(self):
        self.assertEqual(render("Just text."), "Just text.")

    def test_empty_template(self):
        self.assertEqual(render("", {"a": "1"}), "")

    def test_find_variables(self):
        self.assertEqual(
            find_variables("{{a}} and {{b}} and {{a}}"), ["a", "b", "a"]
        )

    def test_find_variables_no_match(self):
        self.assertEqual(find_variables("no braces here"), [])

    def test_unresolved(self):
        self.assertEqual(
            unresolved("{{a}} {{b}}", {"a": "1"}), ["b"]
        )

    def test_unresolved_unique_and_ordered(self):
        self.assertEqual(
            unresolved("{{z}} {{a}} {{z}}", {}), ["z", "a"]
        )

    def test_render_numeric_value(self):
        self.assertEqual(render("Count: {{n}}", {"n": 42}), "Count: 42")


if __name__ == "__main__":
    unittest.main()
