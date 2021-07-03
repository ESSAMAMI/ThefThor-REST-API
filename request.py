from pymongo import MongoClient

#Creating a pymongo client
client = MongoClient('mongodb://mymongodbusername:qzdihgvolihgseoihfoqzdhaqzoiuufhaqozzfhgao@mongo:27017/')
if client:
	print('YES')
#Getting the database instance
db = client['db_project']
print("Database created........")
user = db.user
user.delete_many({})
users_ = [
    {
        "_id":1,
        "name":"SIMON Arnaud",
        "login":"a.simon@admin.com",
        "pwd":"arnaud$$98",
        "trial_version":"2021-09-09",
        "last_connection":"2021-03-02"
    },
    {
        "_id":2,
        "name":"ESSAMAMI Hamza",
        "login":"h.essamami@admin.com",
        "pwd":"essamami$$97",
        "trial_version":"2021-12-09",
        "last_connection":"2021-03-02"
    },
    {
        "_id":3,
        "name":"NIZONDET-RENAUD Nathanaël",
        "login":"n.nizondet@admin.com",
        "pwd":"nathanel$$98",
        "trial_version":"2021-06-09",
        "last_connection":"2021-03-02"
    }
]
user.insert_many(users_)
#Verification
print("List of databases after creating new one")
print(client.list_database_names())

################################################## ALERTS #########################################
notifications = db.notifications
notifications.delete_many({})
notifications_ = [
    {
        "_id":1,
        "user_id":1,
        "tag":"Alerte annomalie detecte",
        "message":"Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc nec dapibus enim, id lobortis lectus. Cras sodales magna vel eros elementum scelerisque. Quisque in dictum magna, a molestie enim. Morbi at ipsum non justo rhoncus mollis sit amet eget metus. Nunc blandit mi massa, non ullamcorper magna luctus at. Fusce eget purus ac urna finibus venenatis. Vestibulum faucibus, nunc vel iaculis feugiat, est orci lobortis dui, sed efficitur turpis purus non dolor.",
        "date_submit":"2021-04-26"
    },
    {
        "_id":2,
        "user_id":2,
        "tag":"Alerte personne intrusive détéctée",
        "message":"Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc nec dapibus enim, id lobortis lectus. Cras sodales magna vel eros elementum scelerisque. Quisque in dictum magna, a molestie enim. Morbi at ipsum non justo rhoncus mollis sit amet eget metus. Nunc blandit mi massa, non ullamcorper magna luctus at. Fusce eget purus ac urna finibus venenatis. Vestibulum faucibus, nunc vel iaculis feugiat, est orci lobortis dui, sed efficitur turpis purus non dolor.",
        "date_submit":"2021-04-26"
    },
    {
        "_id":3,
        "user_id":2,
        "tag":"Alerte annomalie",
        "message":"Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc nec dapibus enim, id lobortis lectus. Cras sodales magna vel eros elementum scelerisque. Quisque in dictum magna, a molestie enim. Morbi at ipsum non justo rhoncus mollis sit amet eget metus. Nunc blandit mi massa, non ullamcorper magna luctus at. Fusce eget purus ac urna finibus venenatis. Vestibulum faucibus, nunc vel iaculis feugiat, est orci lobortis dui, sed efficitur turpis purus non dolor.",
        "date_submit":"2021-04-26"
    },
    {
        "_id":4,
        "user_id":2,
        "tag":"Alerte annomalie entrepot",
        "message":"Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc nec dapibus enim, id lobortis lectus. Cras sodales magna vel eros elementum scelerisque. Quisque in dictum magna, a molestie enim. Morbi at ipsum non justo rhoncus mollis sit amet eget metus. Nunc blandit mi massa, non ullamcorper magna luctus at. Fusce eget purus ac urna finibus venenatis. Vestibulum faucibus, nunc vel iaculis feugiat, est orci lobortis dui, sed efficitur turpis purus non dolor.",
        "date_submit":"2021-04-25"
    },
    {
        "_id":5,
        "user_id":2,
        "tag":"Alerte une personne à votre domicile",
        "message":"Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc nec dapibus enim, id lobortis lectus. Cras sodales",
        "date_submit":"2021-04-28"
    },
    {
        "_id":6,
        "user_id":3,
        "tag":"Alerte une personne à votre domicile",
        "message":"Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc nec dapibus enim, id lobortis lectus. Cras soda",
        "date_submit":"2021-04-28"
    }



    
    
]
notifications.insert_many(notifications_)
for dict_ in db.notifications.find(): 
    print(dict_)
