import os, psycopg2, string, random, hashlib

def get_connection():
    url = os.environ['DATABASE_URL']
    print(url)
    connection = psycopg2.connect(url)
    return connection

def get_salt():
    charset = string.ascii_letters + string.digits
    
    salt = ''.join(random.choices(charset, k=30))
    return salt

def get_hash(password, salt):
    b_pw = bytes(password, 'utf-8')
    b_salt = bytes(salt, 'utf-8')
    hashed_password = hashlib.pbkdf2_hmac('sha256', b_pw, b_salt, 1246).hex()
    return hashed_password

def insert_user(user_name, email, address, password):
    sql = 'INSERT INTO shop_user VALUES (default, %s, %s, %s, %s, %s)'
    salt = get_salt()
    hashed_password = get_hash(password, salt)
    
    try :
        connection = get_connection()
        cursor = connection.cursor()
        
        cursor.execute(sql, (user_name, email, address, hashed_password, salt))
        count = cursor.rowcount # 更新内容を取得
        connection.commit()
    except psycopg2.DatabaseError:
        count = 0
    finally:
        cursor.close()
        connection.close()
        
    return count

def insert_goods(goods_name, detail, price, stock):
    sql = 'INSERT INTO goods VALUES (default, %s, %s, %s, %s)'
    
    try :
        connection = get_connection()
        cursor = connection.cursor()
        
        cursor.execute(sql, (goods_name, detail, price, stock))
        count = cursor.rowcount # 更新内容を取得
        connection.commit()
    except psycopg2.DatabaseError:
        count = 0
    finally:
        cursor.close()
        connection.close()
        
    return count

def delete_user(id):
    sql = 'DELETE FROM shop_user WHERE id = %s'
    
    try:
        connection = get_connection()
        cursor = connection.cursor()
        
        cursor.execute(sql, (id,))
        count = cursor.rowcount
        connection.commit()
    except psycopg2.DatabaseError:
        count = 0
    finally:
        cursor.close()
        connection.close()
        
    return count

def delete_goods(id):
    sql = 'DELETE FROM goods WHERE id = %s'
    
    try:
        connection = get_connection()
        cursor = connection.cursor()
        
        cursor.execute(sql, (id,))
        count = cursor.rowcount
        connection.commit()
    except psycopg2.DatabaseError:
        count = 0
    finally:
        cursor.close()
        connection.close()
        
    return count

def update_goods(id, name, detail, price, stock):
    sql = 'UPDATE goods SET name = %s, detail = %s, price = %s, stock = %s WHERE id = %s'
    
    try:
        connection = get_connection()
        cursor = connection.cursor()
        
        cursor.execute(sql, (name, detail, price, stock, id))
        count = cursor.rowcount
        connection.commit()
    except psycopg2.DatabaseError:
        count = 0
    finally:
        cursor.close()
        connection.close()
    
    return count

def update_user(id, name, email, address):
    sql = 'UPDATE shop_user SET name = %s, email = %s, address = %s WHERE id = %s'
    
    try:
        connection = get_connection()
        cursor = connection.cursor()
        
        cursor.execute(sql, (name, email, address, id))
        count = cursor.rowcount
        connection.commit()
    except psycopg2.DatabaseError:
        count = 0
    finally:
        cursor.close()
        connection.close()
        
    return count

def goods_buy(id,number):
    sql = 'UPDATE goods SET stock = stock - %s WHERE id = %s'
    
    try:
        connection = get_connection()
        cursor = connection.cursor()
        
        cursor.execute(sql, (number,id,))
        count = cursor.rowcount
        connection.commit()
    except psycopg2.DatabaseError:
        count = 0
    finally:
        cursor.close()
        connection.close()
        
    return count

def search_goods(key):
    connection = get_connection()
    cursor = connection.cursor()
    sql = 'SELECT id, name, detail, price, stock FROM goods WHERE name LIKE %s ORDER BY id ASC'
    key = '%' + key + '%'
    
    cursor.execute(sql, (key,))
    rows = cursor.fetchall()
    
    cursor.close()
    connection.close()
    
    return rows

def search_users(key):
    connection = get_connection()
    cursor = connection.cursor()
    sql = 'SELECT id, name, email, address FROM shop_user WHERE name LIKE %s ORDER BY id ASC'
    key = '%' + key + '%'
    
    cursor.execute(sql, (key,))
    rows = cursor.fetchall()
    
    cursor.close()
    connection.close()
    
    return rows
    
        

def select_all_goods():
    connection = get_connection()
    cursor = connection.cursor()
    sql = 'SELECT id, name, detail, price, stock FROM goods ORDER BY id ASC'
    
    cursor.execute(sql)
    rows = cursor.fetchall()
    
    cursor.close()
    connection.close()
    
    return rows

def select_all_users():
    connection = get_connection()
    cursor = connection.cursor()
    sql = 'SELECT id, name, email, address FROM shop_user ORDER BY id ASC'
    
    cursor.execute(sql)
    rows = cursor.fetchall()
    
    cursor.close()
    connection.close()
    
    return rows

def login(user_name, password):
    sql = 'SELECT hashed_password, salt FROM shop_user WHERE name = %s'
    flg = False

    try :
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql, (user_name, ))
        user = cursor.fetchone()

        if user != None:
            salt = user[1]

            hashed_password = get_hash(password, salt)

            if hashed_password == user[0]:
                flg = True
    except psycopg2.DatabaseError:
        flg = False
    finally :
        cursor.close()
        connection.close()
    
    return flg

def admin_login(user_name, password):
    sql = "SELECT hashed_password, salt FROM shop_user WHERE name = 'hatakeyama'"
    flg = False
    
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql, (user_name))
        admin = cursor.fetchone()
        
        if admin != None:
            salt = admin[1]
        
        hashed_password = get_hash(password, salt)

        if hashed_password == admin[0]:
                flg = True

    except psycopg2.DatabaseError:
        flg = False
    finally:
        cursor.close()
        connection.close()
        
    return flg









