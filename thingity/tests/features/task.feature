Feature: Task
    Parse a task

    Scenario: Simple task
        Given I have the task ABC something
        Then the task context is ABC
        And the task garage is False
        And the task date is not set
        And the task mission is False
        And the task subject is something
        And the task rank is 4000

    Scenario: Task in file
        Given I am in the file things/foo/bar/my.md
        And I have the task - [ ] ABC something
        Then the task file is things/foo/bar/my.md
        And the task repository is foo
        And the task context is ABC
        And the task subject is something
        And the task row is 4000 ABC something ‣foo things/foo/bar/my.md

    Scenario: Next task
        Given I am in the file my.md
        And I have the task ABC ^ something next
        Then the task next is True
        And the task file is my.md
        And the task repository is not set
        And the task mission is False
        And the task subject is something next
        And the task rank is 2000
        And the task is ABC ^ something next

    Scenario: Garage task
        Given I have the task - something in garage
        Then the task garage is True
        And the task mission is False
        And the task subject is something in garage
        And the task is - something in garage
        And the task is garage

    Scenario: Mission task
        Given I have the task ~ something in mission
        Then the task garage is False
        And the task is mission
        And the task subject is something in mission
        And the task is ~ something in mission

    Scenario: Backlog task
        Given I have the task . something in backlog
        Then the task backlog is True
        And the task subject is something in backlog
        And the task is . something in backlog 

    Scenario: Backlog task
        Given I have the task a question?
        Then the task question is True
        And the task subject is a question?

    Scenario: Markdown task
        Given I have the task - [ ] something
        Then the task subject is something

    Scenario: Task for now
        Given I have the task 0 something
        Then the task subject is something
        And the task date is ***
        And the task is near

    Scenario: Task for the future
        Given I have the task 20500101 something
        Then the task subject is something
        And the task date is 01 JAN 2050
        And the task is future

    Scenario: Task with to date
        Given I have the task 20500101 to 20500120 something
        Then the task is as given
        And the task subject is something
        And the task date is 01 JAN 2050
        And the task end is 20 JAN 2050

    Scenario: Task with relative day
        Given today is 20210609
        And natural mode
        And I have the task ABC FRI something
        Then the task subject is something
        And the task context is ABC
        And the task date is FRI
        And the task is ABC 20210611 something
        And the task is near
        And the task is not upcoming

    Scenario: Task with absolute upcoming day
        Given today is 20210609
        And natural mode
        And I have the task ABC 20210704 something
        Then the task subject is something
        And the task is upcoming
        And the task is not diary

    Scenario: Task with relative date
        Given today is 20210609
        And natural mode
        And I have the task ABC JUL 8 something
        Then the task is ABC 20210708 something
        And the task is not near

    Scenario: Task with relative day without context
        Given today is 20210609
        And natural mode
        And I have the task SUN something
        Then the task is MEM 20210613 something
        And the task is upcoming

    Scenario: Task with time without context
        Given today is 20210609
        And natural mode
        And I have the task 17:15 something
        Then the task is MEM 20210609 1715 something
        And the task is near

    Scenario: Task with relative day with time without context
        Given today is 20210612
        And natural mode
        And I have the task SUN 10:15 something
        Then the task is MEM 20210613 1015 something
        And the task rank is 1000202106131015

    Scenario: Task with relative day of todays day
        Given today is 20210613
        And natural mode
        And I have the task SUN something
        Then the task is MEM 20210620 something
        And the task display is SUN+ something

    Scenario: Task for today
        Given today is 20210613
        And natural mode
        And I have the task TOD today thing
        Then the task is MEM 20210613 today thing

    Scenario: Task for tomorrow
        Given today is 20210613
        And natural mode
        And I have the task TOM tomorrow thing
        Then the task is MEM 20210614 tomorrow thing

    Scenario: Task for next year
        Given today is 20210613
        And natural mode
        And I have the task 20220401 next year thing
        Then the task display is 01 APR 2022 next year thing

    Scenario: Task with date and time
        Given I have the task 20500101 1415 something
        Then the task subject is something
        And the task date is 01 JAN 2050
        And the task time is 14:15
        And the task rank is 6000205001011415

    Scenario: Task with month
        Given today is 20210613
        And I have the task 202107 something
        Then the task subject is something
        And the task date is JUL

    Scenario: Task with no context
        Given I have the task something
        Then the task subject is something
        And the task context is not set
        And the task is not awaits

    Scenario: Task inbox
        Given I have the task ABC something
        Then the task subject is something
        And the task is inbox

    Scenario: Task with no context and default context
        Given default context is XYZ
        And I have the task something
        Then the task subject is something
        And the task context is XYZ

    Scenario: Task with lower case context
        Given I have the task abc something
        Then the task context is ABC

    Scenario: Task with await
        Given I have the task ABC {BOB} something
        Then the task context is ABC
        And the task display is BOB something
        And the task is awaits
        And the task is not inbox

    Scenario: Task with date in past
        Given today is 20210615
        And I am in the file my.md
        And I have the task MEM 20210617 1930 Something
        Then the task display is THU 19:30 Something
        Then the task row is 1000202106171930 MEM THU 19:30 Something ‣None my.md

