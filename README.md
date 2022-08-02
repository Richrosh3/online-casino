# Online Casino
This was a group project that was completed in one of my classes. The team consisted of University of Maryland students: Thomas, Jordan, Johnny, Andrew, and Roshen. 

## Installation and Testing
To play Online Casino, please visit our website [here](http://cmsc435onlinecasino.herokuapp.com). If you want to play around with the website, you can create an account or login using `user` and `pass` for the username and password respectively.  

If you would like to run the project locally then clone the repository, install the requirements, run `python manage.py runserver` in the base directory and head to `http://127.0.0.1:8000` in your browser.

To run the project tests, clone the repository, install the requirements and run `python manage.py test` in the base 
directory

## Purpose
Online Casino is a website where you can use your real money to gamble online. Whether it's blackjack, craps, roulette, 
or other casino games, you can play the games right from the comfort of your own room. A variety of single and 
multiplayer games are available.

## Instructions

### Creating an Account/Logging In
To begin, refer to our Installation section above on how to visit our website. Begin by creating an account with us by 
clicking on the `Sign Up` button. Enter your email and create a username and password for your login.  If you've visited
us before and already have an account with us, you can log in to your account with your username and password. If you 
have forgotten your username or password, head to the login page and follow the steps after clicking `Reset Password` to
regain access to your account.

### Account Management
Once we've authenticated your password, you can view your current account balance and total earnings from games, and add
funds into your account via a cryptocurrency wallet and/or a bank account. If you would like to cash out, you have the 
option to withdraw your money from your account with us back to your bank account.

### Playing Games
Under the `Games` menu at the top, you'll find the option of choosing between any of our 5 games. Poker, Blackjack, 
Craps, Roulette, and Slots are the available games. Tutorials for how to play will be available in a later version.

When you've selected a game, you will be greeted with a list of ongoing sessions, if there are any. Each session will 
list the number of players currently playing the game. Clicking on a session will allow you to join it. You can also 
create a new session using the `Create a new session` button. Once you enter or create a session, you will be able to 
play the game!

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
├── docs/  ⁃  ⁃  ⁃  ⁃  ⁃  ⁃   Developer documentation
├── games/  ⁃  ⁃  ⁃  ⁃  ⁃  ⁃  Files for each of the games 
│   ├── blackjack/            Files for Blackjack
│   │   ├── game/               Python files that control game logic
│   │   ├── templates/          HTML templates for Blackjack 
│   │   │   ├── ...
│   │   └── web/                Files facilitating communication between frontend and backend
│   │       ├── consumers.py      Contains updater and consumer classes
│   │       └── tests.py
│   ├── craps/                Files for Craps (all games have same structure as above)
│   │   ├── ...
│   ├── poker/                Files for Poker
│   │   ├── ...
│   ├── roulette/             Files for Roulette
│   │   ├── ...
│   └── slots/                Files for Slots
│       ├── ...
├── menus/  ⁃  ⁃  ⁃  ⁃  ⁃  ⁃  Files for the website menus
│   ├── templates/            HTML templates for menus
│   │   ├── ...
│   ├── tests.py
│   ├── urls.py               URL Routing for menu pages
│   └── views.py              Handling of web requests
├── OnlineCasino/ ⁃  ⁃  ⁃  ⁃  Website configuration files
│   ├── settings.py           Website settings
│   └── urls.py               URL Routing for entire website
├── staticfiles/ ⁃  ⁃  ⁃  ⁃   Static files (i.e. JavaScript, image files)
│   ├── ...
├── db.sqlite3                Database
├── manage.py                 Website runner
└── requirements.txt          Project library requirements
```
