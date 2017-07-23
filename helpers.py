def validate_user(username):
    if not username:
        return "That's not a valid username"
    else:
        if len(username)<3 or len(username)>20 or " " in username :
            return "That's not a valid username"
        return ""


def validate_password(password):

    if not password :
        return "That's not a valid password"
    else:
        if len(password)<3 or len(password)>20 or " " in password :
            return "That's not a valid password"

        else:
            return ""    

def verify_passwords(password,verify_pwd):
    if password != verify_pwd:
        return "The passwords dont match"
    else:
        return "" 

def validate_email(email):
    if not email:
        return ""
    else:
        if len(email)<3 or len(email)>20:
            return "That's not a valid email"
        else:
            pattern = r"^[a-zA-Z0-9+-_!.]+@[a-zA-Z0-9]+\.[a-z]+[.]*[a-z]*$"
            matchstring = re.match(pattern,email)
            if matchstring:
                return ""
            else:
                return "That's not a valid email"        
