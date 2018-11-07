#!/usr/bin/env python3
import sqlite3
conn = sqlite3.connect(':memory:')
c=conn.cursor()
c.execute("CREATE TABLE Models (folder_name varchar primary key, name varchar)")
models = [
            ("default_1.yaml","Hilbert"),
            ("default_2.yaml","Ceballos"),
            ("default_3.yaml","Ceballos_new"),
         ]
c.executemany('INSERT INTO models VALUES (?,?)', models)
t = ('default_1.yaml',)
c.execute('SELECT * FROM Models WHERE folder_name=?', t)
print("Models",c.fetchall())

c.execute('''CREATE TABLE Variables (
        `symbol` varchar, 
        `description` varchar, 
        `unit` varchar, 
        `model_id` varchar, 
        primary key (`symbol`,`model_id`),
        CONSTRAINT `fk_Variables_Models`
          FOREIGN KEY (`model_id`)
          REFERENCES `Models`(`folder_name`)
        )''')
variables=[
        ("x","root carbon stock","kg","default_1.yaml"),
        ("y","leaf carbon stock","kg","default_1.yaml"),
        ("k_r","root decomprate","kg","default_1.yaml"),
        ]
c.executemany('INSERT INTO Variables VALUES (?,?,?,?)', variables)
c.execute('SELECT * FROM Variables WHERE model_id=?', ('default_1.yaml',))
print("Variables",c.fetchall())

c.execute('''CREATE TABLE StateVectorPositions(
        `pos_id` varchar, 
        `Variables_symbol` varchar, 
        `Variables_model_id` varchar, 
        primary key (`pos_id`,`Variables_symbol`),
        CONSTRAINT `fk_StateVectorPositions_Variables1`
          FOREIGN KEY (`Variables_symbol`,`Variables_model_id`)
          REFERENCES `Variables`(`symbol`,`model_id`)
        )''')
stv_pos =[
        (0,"x","default_1.yaml"),
        (1,"y","default_1.yaml"),
        ]
c.executemany('INSERT INTO StateVectorPositions VALUES (?,?,?)', stv_pos)
c.execute('SELECT * FROM StateVectorPositions WHERE Variables_model_id=?', ('default_1.yaml',))
print("Positions",c.fetchall())
c.execute('SELECT Variables_symbol FROM StateVectorPositions WHERE Variables_model_id=? ORDER BY `pos_id`', ('default_1.yaml',))
print("Statevector",c.fetchall())



#conn.commit()
#print(c.fetchone())
