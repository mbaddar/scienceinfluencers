class User():
  def __init__(self, email):
    self.email = email

  def is_active(self):
    return True

  def get_id(self):
    return self.email

  def is_authenticated(self):
    return True

  @staticmethod
  def find_or_create_by_email(email):
    return User(email)

  @staticmethod
  def find_by_id(id):
    return User(id)

# this is what it might look like if we were a real application
# user=User.query.filter_by(email=email).first()
# if not user:
#     # Create the user. Try and use their name returned by Google,
#     # but if it is not set, split the email address at the @.
#     nickname = username
#     if nickname is None or nickname == "":
#         nickname = email.split('@')[0]

#     # We can do more work here to ensure a unique nickname, if you 
#     # require that.
#     user=User(nickname=nickname, email=email)
#     db.session.add(user)
#     db.session.commit()