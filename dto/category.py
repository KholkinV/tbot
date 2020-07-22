class Category:
  id: int
  name: str
  info: str
  parentId: int

  def __init__(self, id, name, info, parentId):
    self.id = id
    self.name = name
    self.info = info
    self.parentId = parentId

