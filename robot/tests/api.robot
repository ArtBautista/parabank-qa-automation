*** Settings ***
Documentation     REST API checks with RequestsLibrary (PB-RF-020 to 023).
Resource          ../resources/parabank.resource
Suite Setup       Create ParaBank API Session


*** Test Cases ***
PB-RF-020 Login Returns The Customer
    [Tags]    smoke    api
    ${response}=    GET On Session    parabank    /login/${USERNAME}/${PASSWORD}
    Status Should Be    200    ${response}
    Dictionary Should Contain Key    ${response.json()}    id
    Dictionary Should Contain Key    ${response.json()}    firstName

PB-RF-021 Every Account Belongs To The Customer
    [Tags]    api
    ${customer_id}=    Get Customer Id
    ${response}=    GET On Session    parabank    /customers/${customer_id}/accounts
    Status Should Be    200    ${response}
    FOR    ${account}    IN    @{response.json()}
        Should Be Equal As Integers    ${account}[customerId]    ${customer_id}
        Should Contain Any    ${account}[type]    CHECKING    SAVINGS    LOAN
    END

PB-RF-022 Unknown Customer Returns 400
    [Tags]    negative    api
    ${response}=    GET On Session    parabank    /customers/999999999    expected_status=400
    Should Contain    ${response.text}    Could not find customer #999999999

PB-RF-023 Create Savings Account
    [Tags]    api
    ${customer_id}=    Get Customer Id
    ${ids}=    Get Account Ids    ${customer_id}
    &{params}=    Create Dictionary
    ...    customerId=${customer_id}    newAccountType=1    fromAccountId=${ids}[0]
    ${response}=    POST On Session    parabank    /createAccount    params=${params}
    Status Should Be    200    ${response}
    Should Be Equal    ${response.json()}[type]    SAVINGS
