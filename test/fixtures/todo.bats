#!/usr/bin/env bats

load test_helper

@test "todo : should find todo" {
  run todo --test Bananas
  assert_output --partial 'test-todo.md'
}

