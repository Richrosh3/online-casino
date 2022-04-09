# Online Casino

## Installation and Testing
To play Online Casino, please visit our website [here](http://cmsc435group7.pythonanywhere.com).  
To run the project tests, clone the repository, install the requirements and run `python manage.py test` in the home directory
## Purpose
Online Casino is a website where you can use your real money to gamble online. Whether it's blackjack, craps, roulette, or other casino games, you can play the game right from the comfort of your own room. 

## Instructions
To begin, refer to our Installation section above on how to visit our website. Begin by creating an account with us by clicking on `Sign Up` button to sign up an account using your email and creating a username and password for your login. If you've visited us before and already have an account with us, you can login to your account with your username and password. If you have forgotten your username or password, head to the login page and follow the steps after clicking `Reset Password` to regain access to your account. 

Once we've authenticated your password, you can view your current account balance, total earnings from games, and options to add funds into your account with crypto currency and/or bank account. If you would like to cash out, you have the option to withdraw your money from your account with us back to your bank account.

## File Structure
```
OnlineCasino
├── accounts/  ⁃  ⁃  ⁃  ⁃  ⁃  Files for users and accounts
│   ├── forms.py              Django forms to create HTML forms
│   ├── models.py             Models (database definitions)
│   ├── templates/            HTML templates for accounts
│   │   ├── ...
│   ├── tests.py
│   ├── tests_features.py
│   ├── urls.py               URL Routing for accounts pages
│   └── views.py              Handling of web requests
├── menus/  ⁃  ⁃  ⁃  ⁃  ⁃  ⁃  Files for the website menus
│   ├── templates/            HTML templates for menus
│   │   └── ...
│   ├── tests.py
│   ├── urls.py               URL Routing for menu pages
│   └── views.py              Handling of web requests
├── OnlineCasino/ ⁃  ⁃  ⁃  ⁃  Website configuration files
│   ├── settings.py           Website settings
│   ├── urls.py               URL Routing for entire website
├── db.sqlite3                Database
├── manage.py                 Website runner
└── requirements.txt          Project library requirements
```

## Sprint 1
- ##### Thomas (30%)
    - Django setup
    - Account creation
    - Password reset
    - Tests & CI/CD
- ##### Jordan (17.5%)
    - Add funds by crypto wallet
    - Add funds by bank
    - Internal documentation
- ##### Johnny (17.5%)
    - Display user's account balance
    - Withdraw funds
    - User documentation
- ##### Andrew (17.5%)
    - Display user's total earnings
    - Games menu with links to each casino game
- ##### Roshen (17.5%)
    - Login
    - Logout
    - Profile Features