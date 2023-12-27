*** Settings ***
Documentation    Documentacao das Keywords da Suite de Tasks
Library     rpapy.core.activities
  

*** Variables ***
${VAR}=      variables


*** Keywords ***
Primeira Keyword
    [Arguments]         ${arg}
    Log To Console      Hello ${arg}!