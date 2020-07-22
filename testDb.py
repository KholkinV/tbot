from database import db

con = db.connect()

#db.addCategory(con, "Общая информация о компании, сотрудниках", None, None)
#db.deleteCategory(con, 3)
#row = db.get_current_state(con, 382350841)
#print (row[0])
categories = db.select_all_categories(con)
for category in categories:
  print (category.name)

con.close()