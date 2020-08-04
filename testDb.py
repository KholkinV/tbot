from database import db
from dto.visit import Visit
import datetime

con = db.connect()
# visit = Visit
# visit.chat_id = 382350841
# visit.category_id = 5
# visit.visit_date = datetime.datetime.today()

# db.save_visit(con, visit)

# count = db.get_visits_count_last_week(con)
# print(count)

visits = db.get_visits_count_by_categories(con)
categories = db.select_categories_names_by_ids(con, tuple(visits.keys()))

result = {}
for visit in visits.keys():
  print(categories[visit] + ' ' + str(visits[visit]))

# for key in visits.keys():
#   print(str(key) + ' ' + str(visits[key]))


#db.deleteCategory(con, 3)
#row = db.get_current_state(con, 382350841)
#print (row[0])
# categories = db.select_all_categories(con)
# for category in categories:
#   print (category.name)

con.close()