import random
from datetime import date
import string
import names
from tools.utils import generate_password, generate_email, random_date



class Profile:

    def __init__(self) -> None:
        self.firstName = names.get_first_name(random.randint(0, 2))
        self.lastName = names.get_last_name()

        self.email = generate_email(self.firstName)

        self.ebay_password = generate_password()
        self.ebay_phone = None

    def get_email(self):
        return self.email
    

