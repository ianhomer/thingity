#!/usr/bin/env bats

load test_helper

@test "things : should use local directory" {
  run things --noconfig --info
  assert_output --partial 'thingity/test'
}

@test "things : should find things" {
  run things --noconfig --test "test thing 2"
  assert_output --partial 'Test Thing 2'
}


