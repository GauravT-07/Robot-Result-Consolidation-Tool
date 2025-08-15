*** Settings ***
Library    SeleniumLibrary

*** Test Cases ***
Open Example In Chrome
    #[Tags]   gaurav  akshay  shanky
    Open Browser    https://www.hackerrank.com/profile/GauravTotla_CS    chrome
    Sleep    10s
    Close Browser