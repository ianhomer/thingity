#!/usr/bin/env bats

load test_helper

@test "things-serach : should find things" {
  run things-search --noconfig "test thing 2"
  assert_output '0:things/my-notes/test-thing-2.md:1:# Test Thing 2'
}

@test "things-serach : should find things for test mode" {
  run things-search --noconfig -n test "test thing 2"
  assert_output 'things/my-notes/test-thing-2.md:1:# Test Thing 2'
}

