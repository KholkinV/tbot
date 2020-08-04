import datetime

class Visit:
  id: int
  category_id: int
  chat_id: int
  visit_date: datetime

  def __init__(self, id, category_id, chat_id, visit_date):
    self.id = id
    self.category_id = category_id
    self.chat_id = chat_id
    self.visit_date = visit_date
