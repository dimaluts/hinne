from database import db
from time import time
def new_user(user_id):
    return (user_id, 2500, 0, 0, 100, 0, 5000, 0, 5000)

def if_user(user_id, message):
    user = db(user_id)
    if user.is_user():
        pass
    else:
        user.new_user('users', new_user(user_id))

    if user.select_chats('chats', message.chat.id):
        pass
    else:
        if message.chat.type == 'supergroup':
            user.new_user('chats', f'(\'{message.chat.id}\', {0})')
        
    

    data = user.select_data('users')
    give_time = int(data[7])
    give_max = data[8]
    
    current_time = time()
    
    if int(current_time) - give_time >= 43200:
        user.set_value('give_time', int(time()), 'users')
        user.set_value('give_limit', int(give_max), 'users')
    
    
    return True