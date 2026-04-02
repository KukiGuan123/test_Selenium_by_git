Feature: Login1

  Scenario: Successful login
    Given open the login page
    When input user "testAccount"
    And click login button
    Then login with "successful" account

  Scenario Outline: sort and add <goods> in cart
    Given sort all item
    When click "<goods>" and check details
    And add in cart
    Then check if "<goods>" is in cart
    Then back to all items page

    Examples:
      | goods                            |
      | Sauce Labs Backpack              |
      | Sauce Labs Bike Light            |
      | Sauce Labs Bolt T-Shirt          |
      | Sauce Labs Fleece Jacket         |
      | Sauce Labs Onesie                |
      | Test.allTheThings() T-Shirt (Red)|

  Scenario Outline: sort and add <goods> in cart
    Given enter the cart
    When remove "<goods>"
    Then check if "<goods>" is removed
    Then back to all items page

    Examples:
      | goods                            |
      | Sauce Labs Backpack              |
      | Sauce Labs Bike Light            |
      | Sauce Labs Bolt T-Shirt          |
      | Sauce Labs Fleece Jacket         |
      | Sauce Labs Onesie                |
      | Test.allTheThings() T-Shirt (Red)|

  Scenario Outline: checkout <user>
    Given enter the cart
    When enter checkout page
    Then inpput "<user>" and finish

    Examples:
      | user |
      | user1|
      | user2|
      | user3|
      | user4|
      | user5|
      | user6|