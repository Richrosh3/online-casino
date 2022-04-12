# Web Socket Documentation
## Game Manager
The first thing is the Game Manager. This is where you would implement your game in. For everything to work properly, you need to create a {Game} class that inherits from `Game`. If you want to change how players are added and removed (i.e. do other stuff when players are added or removed) or change how the number of players in the session are defined, just overwrite these functions:
```python
def add_player(self, player: CustomUser):
    self.players.add(player)

def remove_player(self, player: CustomUser):
    self.players.remove(player)

# How many players there are in the current session
def __len__(self):
    return len(self.players)
```
Then you can create a session manager for that game with 
```python
{GAME}_MANAGER = SessionManager(GameClass)
```
This is what goes in all the {GAME}_MANAGER variables that you see below

## `consumers.py`
The `{Game}Updater` class gets called when you send a message to the server from the client javascript. Each function in this class should be static, take one parameter (the data being sent to the server) and could return a dictionary that would be sent to all users in the session (just don't return anything if you dont want to send everyone a message).  

The request being passed in should always be in the format `{'type': type, 'data': data}` for this to work. You then access the data send with `function_parameter['data']`   

The return data doesn't need to be in any format other than that it needs to be a dict

For example:
```python
@staticmethod
def place_bet(request_data):
    bet = request_data['data']['bet']
    
    ...

    return {'type': 'update',
            'data': {data}
            }
```

At the bottom of that class, you need to define the function mapper that will map the incoming message to the right function. It should look something like this:
```python
FUNCTION_MAP = {"type string passed in request_data['type']": function_name_above.__func__, ...}
```


The `{Game}Consumer` class handles the connection to the web socket. It needs 3 functions  

The __init__ fuction that give it reference to the Session Manager and the Game Updater
```python
def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.game_manager = {GAME}_MANAGER
    self.updater = {Game}Updater
```

The connect function gets called when the user initiates the web socket. Make sure to call the super first before doing anything else
```python
def connect(self):
    super({Game}Consumer, self).connect()

    ...
```

And the disconnect function gets called when the websocket connection terminates. Again, make sure to call the super
```python
def disconnect(self, code):
    super({Game}Consumer, self).disconnect(code)
    
    ...
```
If you want to send a message to all users in the Session, you can do it with this code:
```python
async_to_sync(self.channel_layer.group_send)(
    self.session_id,
    {
        'type': 'send_message', # Dont change this. This calls a send_message function that sends it
        'data': {'Data to be sent to all users'}
    }
)
```
To send it to just the current person, use:
```python
# message here would be a dict
self.send(text_data=json.dumps(message))
```


## `routing.py`
This is the file to define the web socket addresses. It could look like this to route the url `ws/blackjack/<session_id> to the Blackjack consumer`
```python
websocket_urlpatterns = [
    re_path(r'ws/blackjack/(?P<session_id>[0-9a-f-]+)/$', consumers.{Game}Consumer.as_asgi())
]
```

## `views.py`
This is the view for the actual game interface. To deal with the web socket, we need a class based view that inherits some functionality. So it could look like this:
```python
class BlackjackSession(GameSessionView):
    template_name = 'path_to_template'
    game_manager = {GAME}_MANAGER
    redirect_to = 'name_of_url_to_redirect_to'
```
If you want to add more functionality to the get request, you could have to call the super get last:
```python
class BlackjackSession(GameSessionView):
    template_name = 'blackjack/blackjack.html'
    game_manager = {GAME}_MANAGER
    redirect_to = 'blackjack_sessions'
    
    def get(self, request: WSGIRequest, *args, **kwargs) -> HttpResponse:
        
        # More stuff
        
        super(BlackjackSession, self).get(request, args, kwargs)
```

## Inside Javascript
To initiate the connection to the web socket in the web page, we need javascript. Here's how to do it:
```javascript
const socket = new WebSocket(`ws://${window.location.host}/{url_you_specified_in_routing_file}`)
```

Then you can use the onmessage to update the page when the web socket recieves a message from the server
```javascript
socket.onmessage = function (e) {
    const message = JSON.parse(e.data)
    // Do stuff with the message
}
```
Hope this helps

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