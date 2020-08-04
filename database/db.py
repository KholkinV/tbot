import psycopg2
from dto.category import Category
from dto.visit import Visit
import datetime

def connect():
  con = psycopg2.connect(
    host = 'localhost',
    database = 'tbot',
    user = 'tbotuser',
    password = 'qwe0151360'
  )
  return con

# todo
# with conn:
#   with conn.cursor() as cur:
#       cur.execute(SQL1)

#region Category

# Добавить категорию
def add_category(con, name, info, parentId):
  cur = con.cursor()
  cur.execute(f"insert into tbot.category (name, info, parent_id) values (%s, %s, %s)", (name, info, parentId))
  con.commit()
  cur.close()

# Получить все категории с parentId = null
def select_categories(con):
  categories = []
  cur = con.cursor()
  cur.execute('select * from tbot.category where parent_id isnull')
  rows = cur.fetchall()
  for row in rows:
    categories.append(Category(row[0], row[1], row[2], row[3]))
  cur.close()
  return categories

# получить категории по id
def select_categories_names_by_ids(con, ids):
  categories = {}
  with con.cursor() as cur:
    cur.execute('select id, name from tbot.category where id in %s', (ids, ))
    rows = cur.fetchall()
    for row in rows:
      categories[row[0]] = row[1]
    cur.close()
    return categories

def select_all_categories(con):
  categories = []
  cur = con.cursor()
  cur.execute('select * from tbot.category')
  rows = cur.fetchall()
  for row in rows:
    categories.append(Category(row[0], row[1], row[2], row[3]))
  cur.close()
  return categories

# Получить категорию по id
def get_category(con, id):
  cur = con.cursor()
  cur.execute('select * from tbot.category where id = %s', (id, ))
  row = cur.fetchone()
  cur.close()
  return Category(row[0], row[1], row[2], row[3])

# Получить подкатегории
def get_subcategories(con, parentId):
  categories = []
  with con.cursor() as cur:
    cur.execute('select * from tbot.category where parent_id = %s', (parentId, ))
    rows = cur.fetchall()
    for row in rows:
      categories.append(Category(row[0], row[1], row[2], row[3]))

    return categories

# Удалить категорию
def delete_category(con, id):
  cur = con.cursor()
  cur.execute('delete from tbot.category where id = %s', (id, ))
  con.commit()
  cur.close()

#endregion

#region User

def add_user(con, chat_id, first_name, last_name):
  cur = con.cursor()
  cur.execute(f"insert into tbot.user (chat_id, first_name, last_name, is_admin, state) values (%s, %s, %s, %s, %s)", (chat_id, first_name, last_name, False, "DEFAULT"))
  con.commit()
  cur.close()

def get_current_state(con, chat_id):
  cur = con.cursor()
  cur.execute('select state from tbot.user where chat_id = %s', (chat_id, ))
  row = cur.fetchone()
  cur.close()
  return row[0]

def set_state(con, state, chat_id):
  cur = con.cursor()
  cur.execute('update tbot.user set state = %s where chat_id = %s', (state, chat_id))
  con.commit()
  cur.close()

# получить пользователей по id
def select_user_names_by_ids(con, ids):
  users = {}
  with con.cursor() as cur:
    cur.execute('select chat_id, first_name, last_name from tbot.user where chat_id in %s', (ids, ))
    rows = cur.fetchall()
    for row in rows:
      users[row[0]] = row[1] + ' ' + row[2]
    cur.close()
    return users

def is_user_exists(con, chat_id):
  with con.cursor() as cur:
    cur.execute('select count(*) from tbot.user where chat_id = %s', (chat_id, ))
    row = cur.fetchone()
    return int(row[0]) != 0

#endregion

# region stats

# сохранить просмотр категории
def save_visit(con, visit: Visit):
  cur = con.cursor()
  cur.execute(f"insert into tbot.visits (category_id, chat_id, visit_date) values (%s, %s, %s)", (visit.category_id, visit.chat_id, visit.visit_date))
  con.commit()
  cur.close()

# получить общее количество просмотров
def get_visits_count(con):
  cur = con.cursor()
  cur.execute('select count(*) from tbot.visits')
  row = cur.fetchone()
  cur.close()
  return row[0]

# получить количество просмотров за последнюю неделю
def get_visits_count_last_week(con):
  cur = con.cursor()
  cur.execute('select count(*) from tbot.visits where visit_date > now() - interval \'1 week\'')
  row = cur.fetchone()
  cur.close()
  return row[0]

# получить количество посещений по категориям
def get_visits_count_by_categories(con):
  visits_dict = {}
  with con.cursor() as cur:
    cur.execute('select category_id from tbot.visits')
    rows = cur.fetchall()
    for row in rows:
      if visits_dict.get(row[0]) is None:
        visits_dict[row[0]] = 1
      else:
        visits_dict[row[0]] = visits_dict[row[0]] + 1
    return visits_dict

# получить подробную статистику по категории
def get_user_visits_stats(con, category_id):
  visits_dict = {}
  with con.cursor() as cur:
    cur.execute('select chat_id from tbot.visits where category_id = %s', (category_id, ))
    rows = cur.fetchall()
    for row in rows:
      if visits_dict.get(row[0]) is None:
        visits_dict[row[0]] = 1
      else:
        visits_dict[row[0]] = visits_dict[row[0]] + 1
    return visits_dict

# endregion

def close(con):
  con.close()