Feature: Human Dates
  Parse human dates

  Scenario: Next Monday
    Given today is 20210609
    And natural mode
    And I have the task MON something
    Then the task is MEM 20210614 something

  Scenario: Next Tuesday
    Given today is 20210609
    And natural mode
    And I have the task TUE something
    Then the task is MEM 20210615 something

  Scenario: Next Wednesday
    Given today is 20210609
    And natural mode
    And I have the task WED something
    Then the task is MEM 20210616 something

  Scenario: Next Thursday
    Given today is 20210609
    And natural mode
    And I have the task THU something
    Then the task is MEM 20210610 something

  Scenario: Next Friday
    Given today is 20210609
    And natural mode
    And I have the task FRI something
    Then the task is MEM 20210611 something

  Scenario: Next Saturday
    Given today is 20210609
    And natural mode
    And I have the task SAT something
    Then the task is MEM 20210612 something

  Scenario: Next Sunday
    Given today is 20210609
    And natural mode
    And I have the task SUN something
    Then the task is MEM 20210613 something
