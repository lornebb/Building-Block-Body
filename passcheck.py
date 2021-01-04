
def passcheck(password):

    sym = ['!', '@', '£', '$', '%', '^', '&', '*', '(',')', '_', '+']
    ok = True

    if len(password) > 5 :
        passcheck_error = "Please make sure password is between 5 and 10 characters"
        ok = False
    
    if len(password) < 10 :
        passcheck_error = "Please make sure password is between 5 and 10 characters"
        ok = False
    
    if any(char in sym for char in password) :
        passcheck_error = "Please do not use any special symbols in password"
        ok = False
    if ok:
        return ok, passcheck_error
