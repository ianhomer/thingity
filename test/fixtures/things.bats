#!/usr/bin/env bats

load test_helper

@test "things : should find things" {
  run things --test "test thing 2"
  assert_output --partial 'Test Thing 2'
}


