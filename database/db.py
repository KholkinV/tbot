import psycopg2
from dto.category import Category

def connect():
  con = psycopg2.connect(
    host = 'localhost',
    database = 'tbot',
    user = 'tbotuser',
    password = 'qwe0151360'
  )
  return con

#region Category

# Добавить категорию
def add_category(con, name, info, parentId):
  cur = con.cursor()
  cur.execute(f"insert into categories.category (name, info, parent_id) values (%s, %s, %s)", (name, info, parentId))
  con.commit()
  cur.close()

# Получить все категории с parentId = null
def select_categories(con):
  categories = []
  cur = con.cursor()
  cur.execute('select * from categories.category where parent_id isnull')
  rows = cur.fetchall()
  for row in rows:
    categories.append(Category(row[0], row[1], row[2], row[3]))
  cur.close()
  return categories

def select_all_categories(con):
  categories = []
  cur = con.cursor()
  cur.execute('select * from categories.category')
  rows = cur.fetchall()
  for row in rows:
    categories.append(Category(row[0], row[1], row[2], row[3]))
  cur.close()
  return categories

# Получить категорию по id
def get_category(con, id):
  cur = con.cursor()
  cur.execute('select * from categories.category where id = %s', (id, ))
  row = cur.fetchone()
  cur.close()
  return Category(row[0], row[1], row[2], row[3])

# Получить подкатегории
def get_subcategories(con, parentId):
  categories = []
  cur = con.cur()
  cur.execute('select * from categories.category where parent_id = %s', (parentId, ))
  rows = cur.fetchall()
  for row in rows:
    categories.append(Category(row[0], row[1], row[2], row[3]))
  cur.close()
  return categories

# Удалить категорию
def delete_category(con, id):
  cur = con.cursor()
  cur.execute('delete from categories.category where id = %s', (id, ))
  con.commit()
  cur.close()

#endregion

#region User

def add_user(con, chat_id, first_name, last_name):
  cur = con.cursor()
  cur.execute(f"insert into users.user (chat_id, first_name, last_name, is_admin, state) values (%s, %s, %s, %s, %s)", (chat_id, first_name, last_name, False, "DEFAULT"))
  con.commit()
  cur.close()

def get_current_state(con, chat_id):
  cur = con.cursor()
  cur.execute('select state from users.user where chat_id = %s', (chat_id, ))
  row = cur.fetchone()
  cur.close()
  return row[0]

def set_state(con, state, chat_id):
  cur = con.cursor()
  cur.execute('update users.user set state = %s where chat_id = %s', (state, chat_id))
  con.commit()
  cur.close()

#endregion

def close(con):
  con.close()