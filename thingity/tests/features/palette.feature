Feature: Palette
    Colors in palette

    Scenario: Empty palette
        When I have an empty palette
        Then the color for undefined_colour is empty

    Scenario: Todo palette
        When I have the todo palette
        Then the color for context is PURPLE
