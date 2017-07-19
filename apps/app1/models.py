from django.db import models
import re 

class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def login_errors(self):
        errors = []
        find_user = User.objects.filter(email=self.email)
        if len(find_user) == 0:
            errors.append('No user found with this email address.')
        elif self.password != find_user[0].password: # TODO: encryption
            errors.append('Incorrect password supplied for this user.')
        
        return errors

    # @ property
    def registration_errors(self):
        errors = []

        # check no duplicate email
        find_user = User.objects.filter(email=self.email)
        if len(find_user) > 0:
            errors.append('Account with this email already exists.')

        # check email address is valid
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
        if not EMAIL_REGEX.match(self.email):
            errors.append('Invalid email format.')

        # check names are 2 or more characters long
        if len(self.first_name) <= 1 or len(self.last_name) <= 1:
            errors.append('First and last name must have at least 2 characters.')

        return errors


class Message(models.Model):
    user_id = models.ForeignKey(User)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    user_id = models.ForeignKey(User)
    message_id = models.ForeignKey(Message)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    