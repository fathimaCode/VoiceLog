def login(email, pwd):
    default_email = "admin@gmail.com"
    default_password = "admin"
    res = email == default_email and pwd == default_password
    return res
