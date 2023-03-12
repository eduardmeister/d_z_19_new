from dao.model.user import User


class UserDAO:
    def __init__(self, session):
        self.session = session

    def get_one(self, id):
        return self.session.query(User).get(id)

    def get_by_username(self, username):
        return self.session.query(User).filter(User.username == username).first()

    def get_all(self):
        return self.session.query(User).all()

    def create(self, user):
        ent = User(**user)
        self.session.add(ent)
        self.session.commit()
        return ent

    def delete(self, id):
        user = self.get_one(id)
        self.session.delete(user)
        self.session.commit()

    def update(self, user):
        user = self.get_one(user.get("id"))
        user.username = user.get("username")
        user.password = user.get("password")
        user.role = user.get("role")

        self.session.add(user)
        self.session.commit()
