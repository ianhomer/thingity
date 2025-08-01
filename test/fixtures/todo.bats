#!/usr/bin/env bats

load test_helper

@test "todo : should find todo" {
  run todo --noconfig --test bananas
  assert_output --partial 'test-todo.md'
}
