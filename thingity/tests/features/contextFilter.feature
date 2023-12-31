Feature: Context Filter
  Parser context filter

  Scenario: Excludes
    When I have the filter -A,-B
    Then the filter has excludes A,B

  Scenario: Children
    When I have the filter :A>B,C
    Then the filter for A has children B,C
    And the filter for A has family A,B,C
    And the filter for A has pattern (A|B|C)
    And the filter for B has no children

  Scenario: Excludes family
    When I have the filter -A,-D:A>B,C:E>F
    Then the filter has excludes A,B,C,D
    And the filter for E has children F

  Scenario: Single context with repository
    When I have the filter :A>>a-notes
    Then the filter for A has repository a-notes

  Scenario: Context with children with repository
    When I have the filter :A>B,C>a-notes
    Then the filter for A has repository a-notes
    And the filter for A has children B,C
    And the filter for B has repository a-notes
