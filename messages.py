from db import db
import users, chains

def get_list(id):
    list = []
    sql = "SELECT M.content, U.username, M.sent_at FROM messages M, users U, chains C WHERE M.chain_id=:id AND M.user_id=U.id ORDER BY M.id"
    results = db.session.execute(sql, {"id":id}).fetchall()
    for result in results:
        if result in list:
            pass
        else:
            list.append(result)
    return list

def in_area(id):
    area = id
    sql = "SELECT :area as area, COUNT(M) FROM messages M, areas A, chains C WHERE C.id=M.chain_id AND A.id=:id AND C.area_id=A.id"
    result = db.session.execute(sql, {"id":id, "area":area})
    return result.fetchall()

def send(content, chain_id):
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = "INSERT INTO messages (content, user_id, sent_at, chain_id) VALUES (:content, :user_id, NOW(), :chain_id)"
    db.session.execute(sql, {"content":content, "user_id":user_id, "chain_id":chain_id})
    db.session.commit()
    return True
