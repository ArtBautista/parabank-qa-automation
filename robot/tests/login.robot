*** Settings ***
Documentation     Keyword-driven and data-driven login tests (PB-RF-001 to 004).
Resource          ../resources/parabank.resource
Test Setup        Open ParaBank
Test Teardown     Close All Browsers


*** Test Cases ***
PB-RF-001 Valid Login Opens Accounts Overview
    [Tags]    smoke    ui
    Log In As    ${USERNAME}    ${PASSWORD}
    Accounts Overview Should Be Shown
    Element Should Contain    css:#leftPanel .smallText    Welcome

PB-RF-002 Wrong Password Is Rejected
    [Tags]    negative    ui
    [Template]    Invalid Login Should Show
    ${USERNAME}    wrong-password-123    The username and password could not be verified.

PB-RF-003 Unknown User Is Rejected
    [Tags]    negative    ui
    [Template]    Invalid Login Should Show
    no_such_user_xyz    whatever    The username and password could not be verified.

PB-RF-004 Empty Credentials Are Rejected
    [Tags]    negative    ui
    [Template]    Invalid Login Should Show
    ${EMPTY}    ${EMPTY}    Please enter a username and password.


*** Keywords ***
Invalid Login Should Show
    [Arguments]    ${user}    ${pass}    ${message}
    Log In As    ${user}    ${pass}
    Login Should Fail With    ${message}
