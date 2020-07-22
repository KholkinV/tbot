from dto import category

categories = [
  category.Category(1, 'Общая информация о компании, сотрудниках', '', None),
  category.Category(2, 'Наши проекты',
    '''Мы специализируется на автоматизации деятельности в сферах: жилищно-коммунального хозяйства и учета услуг, транспортная сфера, архивная деятельность, бюджетно-финансовая деятельность и др.
    Все реализованные продукты социально значимы и приносят реальную пользу людям, например, монетизация льгот ЖКХ, система по предоставлению субсидий на оплату жилья, социально-транспортная карта, АИС питания школьников и т.п.
    Ссылка на описание проектов: http://www.xrm.ru/#/our-projects''',
  1),
  category.Category(3, 'Наши сотрудники', '', 1),
  category.Category(4, 'Наши клиенты и партнеры', '', 1),
  category.Category(5, 'Адреса наших офисов', '', 1),
  category.Category(6, 'Бонусы после испытательного срока',
  '''- ДМС, подробности здесь: https://confluence.xrm.ru/pages/viewpage.action?pageId=21300867.
  По вопросам оформления полиса ДМС можно писать Волковой Анастасии, e-mail:morik@xrm.ru.
  - Компенсация затрат на спорт, подробности здесь: https://confluence.xrm.ru/pages/viewpage.action?pageId=20580656. Получить компенсацию можно в Отделе персонала (оф. 802 П15).
  ''',
  None)
]