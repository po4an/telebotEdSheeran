# -*- coding: utf-8 -*-
import sqlite3



class SQLighter:
    def __init__(self, database):
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    def select_all(self):
       """Получаем все строки"""
       with self.connection:
           return self.cursor.execute('select * from music').fetchall()

    def select_single(self, rownum):
        """Получаем одну строку с номером rownum"""
        with self.connection:
            return self.cursor.execute('select * from music where id = {}'.format(rownum)).fetchall()

    def count_rows(self):
        """Считаем количество строк"""
        with self.connection:
            result = self.cursor.execute('select * from music').fetchall()
            return len(result)

    def close(self):
        """Закрываем текущуу соединение"""
        self.connection.close()

