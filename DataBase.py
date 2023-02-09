import sqlite3

if __name__!="__main__":

    Con=sqlite3.connect("AntiDeleted.db",check_same_thread=False)

    """Create Table if not exist"""
    Con.cursor().execute(
            """CREATE TABLE IF NOT EXISTS InfoMessageTarget
            ( 
                [Id] INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                [UserId] INTEGER NOT NULL,
                [Firstname] NVARCHAR(100) NOT NULL, 
                [MessageContent] NVARCHAR(2000) NOT NULL, 
                [Time] TEXT(50),
                [Date] TEXT(50),
                [MessageId] INTEGER NOT NULL
            )""").close()
    
    Con.cursor().execute(
            """CREATE TABLE IF NOT EXISTS InfoChanellTarget
            ( 
                [UserId] INTEGER PRIMARY KEY NOT NULL,
                [UserIdChanell] INTEGER NOT NULL
            )""").close()

    def Insert_InfoMessage_Target(UserId:int,Firstname:str,MessageContent:str,Time:str,Date:str,MessageId:int):
        try:
            Values=(UserId,Firstname,MessageContent,Time,Date,MessageId)
            Result=Con.cursor().execute("INSERT INTO InfoMessageTarget VALUES(NULL,?,?,?,?,?,?)",Values).rowcount
            Con.commit()
            if Result==1:
                return 200
            return 500
        except Exception as e:
            return 500
    
    def Fetch_InfoMessage_Target(MessageId:int):
        try:
            Result=Con.cursor().execute("SELECT * From InfoMessageTarget WHERE MessageId=%s"%MessageId).fetchone()
            Con.commit()
            if Result==None or len(Result)==0:
                return 404
            if Result!=None and len(Result)>0:
                return Result
            return 500
        except Exception as e:
            return 500
        
    def Insert_InfoChanell_Target(UserId:int,UserChanellId:int):
        try:
            Values=(UserId,UserChanellId)
            Result=Con.cursor().execute("INSERT INTO InfoChanellTarget VALUES(?,?)",Values).rowcount
            Con.commit()
            if Result==1:
                return 200
            return 500
        except Exception as e:
            return 500
        
        
    def Fetch_InfoChanell_Target(UserId:int):
        try:
            Result=Con.cursor().execute("SELECT UserIdChanell From InfoChanellTarget WHERE UserId=%s"%UserId).fetchone()
            Con.commit()
            if Result==None or len(Result)==0:
                return 404
            if Result!=None and len(Result)>0:
                return Result
            return 500
        except Exception as e:
            return 500

    def Delete_InfoChanell_Target(UserId:int):
        try:
            Result=Con.cursor().execute("DELETE FROM InfoChanellTarget WHERE UserId=%s"%UserId).rowcount
            Con.commit()
            if Result==None:
                return 404
            if Result>=0:
                return 200
            return 500
        except Exception as e:
            return 500