from sqlitedict import SqliteDict
from dataclasses import dataclass
from typing import Union
@dataclass
class UserID:
    def __init__(self, index:Union[int, str]):
        self.id = str(index)
@dataclass
class GuildID:
    def __init__(self, index:Union[int, str]):
        self.id = str(index)
class Database:
    """HoBase by !KaBoT#6547 (discord)"""
    def __init__(self, filename:str="example.sqlite", table:str="unnamed" ,autocommit:bool=False):
        self.filename = filename
        self.db = SqliteDict(filename, tablename=table, autocommit=autocommit)
        self.__closed = 0
        self.autocommit = autocommit
    def __len__(self):
        return len(self.db)
    def __repr__(self):
        if self.__closed == 0:
            info = f"<database, status opened, file '{self.filename}' with '{len(self.db)}' variables, autocommit '{self.autocommit}'>"
        elif self.__closed == 1:
            info = f"<database, status closed>"
        return info
    def delete(self, id:Union[UserID, GuildID], obj:str=None, guildid:GuildID=None):
        if (type(id) is UserID and type(guildid) is type(None) or type(id) is GuildID) and type(obj) is type(None):
            self.db[id.id] = {}
        elif (type(id) is UserID and type(guildid) is GuildID) and type(obj) is type(None):
            self.db[id.id][guildid.id] = {}
        elif (type(id) is UserID and type(guildid) is GuildID) and type(obj) is not type(None):
            self.set({obj:None}, id=id, guildid=guildid)
        elif (type(id) is UserID and type(guildid) is type(None) or type(id) is GuildID) and type(obj) is not type(None):
            self.set({obj:None}, id=id)
    def get(self, id:Union[UserID, GuildID], guildid:GuildID=None):
        """Get something from somewhere"""
        if type(id) is UserID and type(guildid) is type(None) or type(id) is GuildID:
            return self.db[id.id]
        elif type(id) is UserID and type(guildid) is GuildID:
            return self.db[guildid.id][id.id]
    def set(self, inp:dict, id, guildid:GuildID=None):
        """Set something in somewhere"""
        if type(id) is UserID and type(guildid) is type(None) or type(id) is GuildID:
            try:
                self.db[id.id] = {**self.db[id.id], **inp}
                return 0
            except KeyError:
                self.db[id.id] = inp
                return 0
        elif type(id) is UserID and type(guildid) is GuildID:
            try:
                self.db[guildid.id][id.id] = {**self.db[guildid.id][id.id], **inp}
                return 0
            except KeyError:
                try:
                    self.db[guildid.id][id.id] = inp
                    return 0
                except KeyError:
                    self.db[guildid.id] = {id.id: inp}
                    return 0
    def open(self, filename:str="example.sqlite", autocommit:bool=False):
        """Open another database file"""
        self.filename = filename
        self.db = SqliteDict(filename, autocommit=autocommit)
        self.__closed = 0
    def commit(self):
        self.db.commit()
    def close(self):
        """Close database file"""
        self.db.close()
        self.__closed = 1