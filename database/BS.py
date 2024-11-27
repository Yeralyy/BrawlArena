import sqlite3
import os.path

class BS_DB():
    def __init__(self, database="bsdb.db"):
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(BASE_DIR, "bsdb.db")
        self.con = sqlite3.connect(database=db_path)
        self.cur = self.con.cursor()

    # save data to db
    def save_data(
            self,
            user_id,
            name,
            phone_number,
            parallel,
            invite_link,
            is_admin=0
    ) -> bool:
        with self.con:
            try:
                self.cur.execute(
                        '''INSERT INTO users 
                        ("telegram_id", "name", "phone_number", "parallel", "is_admin", "invite_link")
                        VALUES(?, ?, ?, ?, ?, ?)''', (
                            user_id, 
                            name, 
                            phone_number,   
                            parallel,
                            is_admin,
                            invite_link
                            )
                            )
                print(f"[INFO] Succefully saved data for {user_id}")            
                return True
            except Exception as ex:
                print(f"[INFO] Failed saving data for {user_id}: {ex}")
                return False

    def save_user_mode(self, user_id, mode):
        with self.con:
            try:
                if mode == "solo":
                    self.cur.execute('''UPDATE users SET solo = ? WHERE telegram_id = ?''', (
                    1,
                    user_id
                        )
                    )
                
                if mode == "duo":
                    self.cur.execute('''UPDATE users SET duo = ? WHERE telegram_id = ?''', (
                        1,
                        user_id
                        )
                    )
                return True

            except Exception as ex:
                print(ex)
                return False

    def is_user_in_db(self, user_id):  
            with self.con:
                try:
                    if self.cur.execute('''SELECT 1 FROM users WHERE telegram_id = ?''', (user_id,)).fetchone() is not None:
                        return True
                    else:
                        return False
                except Exception as ex:
                    return False
    
    def is_user_admin(self, user_id):
        with self.con:
            try: 
                res = (self.cur.execute('''SELECT is_admin FROM users WHERE telegram_id = ?''', (user_id,)).fetchone())
                if res == (1, ):
                    return True
                else:
                    return False    
            except Exception as ex:
                print(f"[DB EXCEPTION] {ex}")
                return False

    def count_users(self):
        with self.con:
            try:
                return self.cur.execute(
                    '''SELECT COUNT(*) FROM users'''
                ).fetchone()
            except Exception as ex:
                print(f"[EXCEPTION] {ex}")
                return False


    def user_info(self, user_id: int):
        with self.con:
            try:
                return self.cur.execute(
                    '''SELECT "name", "phone_number", "parallel", "invite_link", "solo", "duo" FROM users WHERE telegram_id = ?''', (user_id, )
                ).fetchone()
            except Exception as ex:
                print(ex)
                return False

    def solo_players_info(self):
        with self.con:
            try:
                res = self.cur.execute(
                '''SELECT "name", "phone_number", "parallel", "invite_link" FROM users WHERE  solo= ?''', (1, )
                ).fetchall()
                return (len(res), res)
            except Exception as ex:
                print(ex)
                return False


    def duo_players_info(self):
        with self.con:
            try:
                res = self.cur.execute(
                '''SELECT "name", "phone_number", "parallel", "invite_link" FROM users WHERE  duo= ?''', (1, )
                ).fetchall()
                return (len(res), res)
            except Exception as ex:
                print(ex)
                return False

    def fetchall_users(self):
        with self.con:
            try:
                return self.cur.execute('''SELECT telegram_id FROM users''').fetchall()
            except Exception as ex:
                print(ex)


    def is_user_solo(self, user_id):
        with self.con:
            try: 
                res = (self.cur.execute('''SELECT solo FROM users WHERE telegram_id = ?''', (user_id,)).fetchone())
                if res == (1, ):
                    return True
                else:
                    return False    
            except Exception as ex:
                print(f"[DB EXCEPTION] {ex}")
                return False

    def is_user_duo(self, user_id):
        with self.con:
            try: 
                res = (self.cur.execute('''SELECT duo FROM users WHERE telegram_id = ?''', (user_id,)).fetchone())
                if res == (1, ):
                    return True
                else:
                    return False    
            except Exception as ex:
                print(f"[DB EXCEPTION] {ex}")
                return False

# if __name__ == "__main__":
#     db = BS_DB()
#     print(db.save_user_mode(user_id=5398848258, mode="duo"))
#     print(db.duo_players_info())
