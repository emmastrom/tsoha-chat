from db import db
import users, areas, messages

def get_list():
    sql = "SELECT C.subject, C.opening_message, U.username, C.area_id FROM chains C, users U WHERE C.user_id=U.id ORDER BY C.id"
    result = db.session.execute(sql)
    return result.fetchall()

def get_my_chains(user_id):
    sql = "SELECT id, subject, opening_message FROM chains WHERE user_id=:user_id ORDER BY id" 
    return db.session.execute(sql, {"user_id":user_id}).fetchall()

def in_area(id):
    area = id
    sql = "SELECT :area AS area, COUNT(*) FROM chains WHERE area_id=:id"
    result = db.session.execute(sql, {"id":id, "area":area})
    return result.fetchall()

def get_id(id):
    sql = "SELECT id FROM chains WHERE area_id=:id"
    result = db.session.execute(sql, {"id":id})
    return result.fetchall()

def create(area_id, subject, opening_message):
    user_id = users.user_id()
    sql = "INSERT INTO chains (area_id, subject, opening_message, user_id) VALUES (:area_id, :subject, :opening_message, :user_id)"
    db.session.execute(sql, {"area_id":area_id, "subject":subject, "opening_message":opening_message, "user_id":user_id})
    db.session.commit()

def get_subject(id):
    sql = "SELECT subject FROM chains WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    return result.fetchone()[0]

def get_opening_message(id):
    sql = "SELECT opening_message FROM chains WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    return result.fetchone()[0]

def edit_subject(id, subject):
    sql = "UPDATE chains SET subject=:subject WHERE id=:id"
    db.session.execute(sql, {"id":id, "subject":subject})
    db.session.commit()

def edit_opening_message(id, opening_message):
    sql = "UPDATE chains SET opening_message=:opening_message WHERE id=:id"
    db.session.execute(sql, {"id":id, "opening_message":opening_message})
    db.session.commit()
