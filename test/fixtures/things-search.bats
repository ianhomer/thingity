#!/usr/bin/env bats

load test_helper

@test "things-serach : should find things" {
  run things-search --dry "test thing 2"
  assert_output --partial 'Test Thing 2'
}

@test "things-serach : should find things for test mode" {
  run things-search -n test --dry "test thing 2"
  assert_output --partial 'Test Thing 2'
}

