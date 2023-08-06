import uuid
import hashlib
import sqlite3


class DB:
    def __init__(self):
        self.file = 'database.db'

        self.CreateConnection()
        self.CreateTable()

    def __del__(self):
        self.EndConnection()

    def CreateConnection(self):
        self.conn = sqlite3.connect(self.file)
        self.conn.execute("PRAGMA foreign_keys = ON")

        self.cur = self.conn.cursor()

    def EndConnection(self):
        self.cur.close()
        self.conn.close()

    def CreateTable(self):
        UserTableQuery = '''
            CREATE TABLE IF NOT EXISTS Users (
                UserName    TEXT        PRIMARY KEY,
                Question    TEXT,
                Answer      TEXT,
                Password    TEXT
            )
        '''

        CompanyTableQuery = '''
            CREATE TABLE IF NOT EXISTS Company (
                CompanyID   TEXT        PRIMARY KEY,
                UserID      TEXT,
                Name        TEXT,
                FOREIGN KEY(UserID) REFERENCES Users(UserName) ON DELETE CASCADE
            )
        '''

        with self.conn:
            for query in [UserTableQuery, CompanyTableQuery]:
                self.cur.execute(query)

    def AddNewUser(self, UserName, Question, Answer, Password):
        Answer = hashlib.sha256(Answer.encode()).hexdigest()
        UserName = hashlib.sha256(UserName.encode()).hexdigest()
        Question = hashlib.sha256(Question.encode()).hexdigest()
        Password = hashlib.sha256(Password.encode()).hexdigest()

        details = (UserName, Question, Answer, Password)

        with self.conn:
            self.cur.execute('''INSERT INTO Users (UserName, Question, Answer,
            Password) VALUES (?, ?, ?, ?)''', details)

    def AddCompany(self, UserID, company):
        CompanyID = uuid.uuid4().hex

        with self.conn:
            self.cur.execute('''INSERT INTO Company (CompanyID, UserID, Name)
            VALUES (?, ?, ?)''', (CompanyID, UserID, company))

    def Login(self, UserName, Password):
        with self.conn:
            UserName = hashlib.sha256(UserName.encode()).hexdigest()
            Password = hashlib.sha256(Password.encode()).hexdigest()

            RetrievedData = self.cur.execute('''SELECT UserName FROM Users WHERE
            UserName=? AND Password=?''', (UserName, Password)).fetchall()

            if RetrievedData:
                return True

            return False

    def GetCompanyName(self, UserID):
        with self.conn:
            companies = self.cur.execute('''SELECT Name FROM Company WHERE
            UserID=?''', (UserID,)).fetchall()

            if companies:
                return [comp.split()[0] for company in companies for comp in company]

            return []

    def RemoveCompany(self, CompanyName):
        with self.conn:
            CompanyDetails = self.cur.execute('''SELECT CompanyID, UserID, Name FROM Company''').fetchall()

            if CompanyDetails:
                for comp_id, user_id, comp_name in CompanyDetails:
                    if CompanyName in comp_name:
                        self.cur.execute('''DELETE FROM Company WHERE Name=?''', (comp_name,))

    def UserExists(self, UserName):
        UserName = hashlib.sha256(UserName.encode()).hexdigest()
        AllUsers = self.cur.execute('''SELECT UserName FROM Users''').fetchall()

        if AllUsers:
            return UserName in AllUsers[0]

        return False

    def ResetDetails(self, UserName):
        if self.UserExists(UserName):
            with self.conn:
                UserName = hashlib.sha256(UserName.encode()).hexdigest()
                details = self.cur.execute('''SELECT Question, Answer FROM Users WHERE UserName=?''', (UserName,)).fetchone()

                return details

        return False

    def ResetPassword(self, UserName, Password):
        with self.conn:
            UserName = hashlib.sha256(UserName.encode()).hexdigest()
            Password = hashlib.sha256(Password.encode()).hexdigest()

            self.cur.execute('''UPDATE Users set Password=? WHERE UserName=?''', (Password, UserName))
