from flask import redirect, session
from functools import wraps

def login_required(f):
    """
       Decorate routes to require login.

       http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
       """
    @wraps(f)
    def decorated_function(*args, **kwargs):

        #using dict.get() to see if user has logged in
        if not session.get('logged_in'):
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function