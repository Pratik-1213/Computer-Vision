class InvalidPasswordException(Exception):
    def __init__ (self, message="Password is incorrect"):
        self.message = message
        super().__init__ (self.message)

def check_password(input_password):
    correct_password = "SecurePassword123" 
    if input_password != correct_password:
        raise InvalidPasswordException("The password you entered is incorrect.")
    else:
        print("Password is correct. Access granted.")

try:
    user_password = input("Enter your password: ")
    check_password(user_password)
except InvalidPasswordException as e:
    print(e)