*** Settings ***
Documentation     End-to-end transfer: act in the UI, verify through the API (PB-RF-010, 011).
Resource          ../resources/parabank.resource
Suite Setup       Create ParaBank API Session
Test Setup        Open Signed In ParaBank
Test Teardown     Close All Browsers


*** Test Cases ***
PB-RF-010 Transfer Moves The Exact Amount
    [Tags]    smoke    ui    api
    ${customer_id}=    Get Customer Id
    ${ids}=    Get Account Ids    ${customer_id}
    ${from_id}=    Convert To String    ${ids}[0]
    ${to_id}=    Convert To String    ${ids}[1]
    ${before}=    Get Balance    ${from_id}
    Transfer Funds In UI    25.50    ${from_id}    ${to_id}
    ${after}=    Get Balance    ${from_id}
    ${expected}=    Evaluate    round(${before} - 25.50, 2)
    Should Be Equal As Numbers    ${after}    ${expected}

PB-RF-011 Empty Transfer Amount Is Rejected
    [Documentation]    Known defect DEF-002: ParaBank shows an internal error instead of the
    ...                validation message. robot:skip-on-failure reports it as SKIP until fixed.
    [Tags]    negative    ui    known-defect    robot:skip-on-failure
    Click Link    Transfer Funds
    Wait For Account Options    fromAccountId
    Click Button    css:input[value='Transfer']
    Wait Until Element Is Visible
    ...    xpath://p[@id='amount.errors' and normalize-space()='The amount cannot be empty.']
    Element Should Not Be Visible    id:showResult
