Feature: Login2
  Scenario Outline: Login with <status> account
    Given open the login page
    When input user "<username>"
    And click login button
    Then <result>

    Examples:
      | status                          | username           | result                              |
      | Successful login                | testAccount        | login with "successful" account     |
      | Failed login with lock account  | lockAccount        | login with "lock" account           |
      | Failed login with wrong password| wrongAccount       | login with "not match" account      |