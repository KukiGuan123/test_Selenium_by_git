Feature: Login3
  Background:
    Given open the login page
    And maximize browser window

  Scenario: Successful login
    When input user "testAccount"
    And click login button
    Then login with "successful" account


  Scenario: Failed login with lock account
    When input user "lockAccount"
    And click login button
    Then login with "lock" account


  Scenario: Failed login with wrong password
    When input user "wrongAccount"
    And click login button
    Then login with "not match" account
