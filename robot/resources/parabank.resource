*** Settings ***
Documentation     Shared variables and keywords for the ParaBank Robot Framework suites.
Library           SeleniumLibrary    timeout=15s
Library           RequestsLibrary
Library           Collections
Library           String


*** Variables ***
${BASE_URL}       http://localhost:8080/parabank
${API_URL}        ${BASE_URL}/services/bank
${BROWSER}        chrome
${USERNAME}       john
${PASSWORD}       demo
&{JSON}           Accept=application/json


*** Keywords ***
# ------------------------------------------------------------------ browser
Open ParaBank
    [Documentation]    Opens the home page in a fresh browser.
    Open Browser    ${BASE_URL}/index.htm    ${BROWSER}
    Set Window Size    1366    900

Log In As
    [Arguments]    ${user}    ${pass}
    Input Text        name:username    ${user}
    Input Password    name:password    ${pass}
    Click Button      css:input[value='Log In']

Accounts Overview Should Be Shown
    Wait Until Page Contains Element    css:#accountTable tbody tr td a
    Title Should Be    ParaBank | Accounts Overview

Login Should Fail With
    [Arguments]    ${message}
    Wait Until Element Is Visible    css:#rightPanel p.error
    Element Text Should Be    css:#rightPanel p.error    ${message}
    Page Should Not Contain Link    Log Out

Open Signed In ParaBank
    Open ParaBank
    Log In As    ${USERNAME}    ${PASSWORD}
    Accounts Overview Should Be Shown

Wait For Account Options
    [Arguments]    ${select_id}
    Wait Until Page Contains Element    css:#${select_id} option

Transfer Funds In UI
    [Arguments]    ${amount}    ${from_id}    ${to_id}
    Click Link    Transfer Funds
    Wait For Account Options    fromAccountId
    Input Text    id:amount    ${amount}
    Select From List By Value    id:fromAccountId    ${from_id}
    Select From List By Value    id:toAccountId    ${to_id}
    Click Button    css:input[value='Transfer']
    Wait Until Element Is Visible    id:showResult
    Element Text Should Be    id:fromAccountIdResult    ${from_id}
    Element Text Should Be    id:toAccountIdResult    ${to_id}

# ------------------------------------------------------------------ API
Create ParaBank API Session
    Create Session    parabank    ${API_URL}    headers=${JSON}    verify=True

Get Customer Id
    ${response}=    GET On Session    parabank    /login/${USERNAME}/${PASSWORD}
    RETURN    ${response.json()}[id]

Get Account Ids
    [Arguments]    ${customer_id}
    ${response}=    GET On Session    parabank    /customers/${customer_id}/accounts
    ${ids}=    Create List
    FOR    ${account}    IN    @{response.json()}
        Append To List    ${ids}    ${account}[id]
    END
    RETURN    ${ids}

Get Balance
    [Arguments]    ${account_id}
    ${response}=    GET On Session    parabank    /accounts/${account_id}
    ${balance}=    Evaluate    round(${response.json()}[balance], 2)
    RETURN    ${balance}
