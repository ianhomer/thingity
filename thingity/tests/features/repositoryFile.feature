Feature: Repository File
    Get repository file from file

    Scenario: File in git root
        Given I am in directory /tmp/foo
        And git root is bar
        When I have the file bar/file.txt
        Then the file path is file.txt
        And the file root is /tmp/foo/bar

    Scenario: Root File is not in git root
        Given I am in directory thingity/tests/data/things
        When I have the file foo/thing.md
        Then the file path is thing.md
        And the file root is thingity/tests/data/things/foo

  Scenario: File is not in git root
        Given I am in directory thingity/tests/data/things
        When I have the file foo/bar/thing.md
        Then the file path is bar/thing.md
        And the file root is thingity/tests/data/things/foo

    Scenario: File has leading ./
        Given I am in directory thingity/tests/data/things
        When I have the file ./foo/bar/thing.md
        Then the file path is bar/thing.md
        And the file root is thingity/tests/data/things/foo
