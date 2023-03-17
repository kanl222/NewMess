def Ok_Authorization(id: int, username: str, email: str, icon: str) -> dict:
    return {
        'command': 'OK_AUTHORIZATION',
        'id': id,
        'username': username,
        'email': email,
        'icon': icon
    }
    
user = [1,'sdfsdf','sdfsdfs','sdfsf']
print(Ok_Authorization(id = user[0],username= user[1],email= user[2],icon= user[-1]))