Feature: Things
  Normalise a thing

  Scenario: Thing
    When I have the thing my-collection/path/thing.md
    Then the thing base is thing

  Scenario: Date stream this year thing
    Given today is 20210609
    When I have the thing my-collection/stream/0425.md
    Then the thing base is 0425
    And the thing path is stream
    And the thing isn't normal
    And the thing normalFilename is my-collection/stream/archive/2021/20210425.md

  Scenario: Recent date stream thing
    Given today is 20210609
    When I have the thing my-collection/stream/0607.md
    Then the thing base is 0607
    And the thing path is stream
    And the thing normalFilename is my-collection/stream/0607.md
    And the thing is normal

  Scenario: Date with dashes stream thing like obsidian default
    Given today is 20210609
    When I have the thing my-collection/stream/2021-06-07.md
    Then the thing base is 2021-06-07
    And the thing path is stream
    And the thing normalFilename is my-collection/stream/0607.md
    And the thing isn't normal

  Scenario: Date stream with year from archive path
    Given today is 20210709
    When I have the thing my-collection/stream/archive/2019/0425.md
    Then the thing base is 0425
    And the thing isn't normal
    And the thing normalFilename is my-collection/stream/archive/2019/20190425.md

  Scenario: Date stream last year thing
    Given today is 20210301
    When I have the thing my-collection/stream/0425.md
    Then the thing base is 0425
    And the thing path is stream
    And the thing isn't normal
    And the thing normalFilename is my-collection/stream/archive/2020/20200425.md

  Scenario: No path date thing
    Given today is 20210812
    When I have the thing my-collection/2021-01-25.md
    Then the thing base is 2021-01-25
    And the thing isn't normal
    And the thing path isn't set
    And the thing normalFilename is my-collection/stream/archive/2021/20210125.md

  Scenario: No path thing
    When I have the thing my-collection/thing.md
    Then the thing base is thing
    And the thing is normal
    And the thing path isn't set

  Scenario: No normal thing
    When I have the thing "my-collection/Ab_c d.123.md"
    Then the thing isn't normal
    And the thing normalFilename is my-collection/Ab-c-d-123.md
