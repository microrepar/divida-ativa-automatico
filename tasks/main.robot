*** Settings ***
Documentation    Documentação da Suite de Tasks Robot Framework

Library     rpapy.core.activities
Resource    ../resources/keywords.robot
  
*** Variables ***
${VAR}=      Everybody


*** Tasks ***
Tarefa principal
    Keyword principal


*** Keywords ***
Keyword principal
    Primeira Keyword        ${VAR}