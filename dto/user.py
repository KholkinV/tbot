class User:
  chat_id: int
  first_name: str
  last_name: str
  is_admin: bool

  def __init__(self, id, first_name, last_name, is_admin):
    self.chat_id = id
    self.first_name = first_name
    self.last_name = last_name
    self.is_admin = is_admin