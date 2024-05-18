import os
import uvicorn
import mysql.connector
from pydantic import BaseModel
from fastapi import FastAPI, Request, Form
from starlette.middleware.sessions import SessionMiddleware
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from urllib.parse import quote_plus

# fastAPI settings
app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key='SECRET_KEY')
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

class member_message_info(BaseModel):
    member_id: str
    message: str

class member_message_deletion(BaseModel):
    message_id: str
    member_id: str

class member_name_check(BaseModel):
    member_id: str
    username: str

class member_name_update(BaseModel):
    #member_id: str
    name: str
    

# MySQL settings
mysql_secret_code = os.environ.get('ENV_MYSQL_PASSWORD')

# MySQL settings
#db = mysql.connector.connect(
db = mysql.connector.pooling.MySQLConnectionPool(
    pool_name = "sql_pool",
    host="localhost", 
    user="root", 
    password=mysql_secret_code, 
    database="website")

#Cursor = db.cursor()


# 首頁
@app.get("/") 
def welcome_home(request: Request):
    
    return templates.TemplateResponse(request=request, 
                                      name="homePage.html")

@app.get("/api/member")
def respond_match_member(request: Request, username: str):

    response_json = {"data": None}

    try:
        query = "SELECT id, name, username FROM member WHERE username = %s;"
        account = (username,)

        con = db.get_connection()
        Cursor = con.cursor(dictionary=True)
        Cursor.execute(query, account)
        fetch_result = Cursor.fetchall()

        if fetch_result == []:

            return response_json

        else:
            response_json['data'] = fetch_result[0]
            return response_json
    
    except:

        return response_json

    finally:
        Cursor.close()
        con.close()
    

@app.patch("/api/member")
def update_name(request: Request, member_info: member_name_update):

    response_json = {}

    try:
        update_query = 'UPDATE member SET name = %s WHERE username = %s;'
        account = (member_info.name, request.session.get('username'))

        con = db.get_connection()
        Cursor = con.cursor(dictionary=True)
        Cursor.execute(update_query, account)
        con.commit()

        response_json['ok'] = True

        return response_json

    except:

        response_json['error'] = True

        return response_json

    finally:
        
        Cursor.close()
        con.close()
        

# 驗證帳號、密碼 
@app.post("/signin") 
def verify_account(request: Request, username: str = Form(None), password: str = Form(None)):    

    # check signed up or not
    try:
        query = "SELECT id, name, username FROM member WHERE username = %s AND password = %s"
        account = (username, password)

        con = db.get_connection()
        Cursor = con.cursor(dictionary=True)
        Cursor.execute(query, account)
        fetch_result = Cursor.fetchall()

        # check the index
        id_result = fetch_result[0]['id']
        name = fetch_result[0]['name']
        username_result = fetch_result[0]['username']

        # set logIn session
        request.session.update({"SIGNED-IN": True, 
                                "member_id": id_result,
                                "member_name": name,
                                "member_username": username_result})
        
        return RedirectResponse(url='/member', status_code=303)

    except:
        error_message = ''
        if username == None or password == None:
            error_message = '請輸入帳號、密碼'
        
        else:
            error_message = '帳號或密碼輸入錯誤'
        
        error_message = quote_plus(error_message.encode("utf-8"))
        redirect_url = f"/error?message={error_message}"
        return RedirectResponse(redirect_url, headers={"message": error_message})
    
    finally:
        Cursor.close()
        con.close()
        

# 登入成功
@app.get("/member") 
def memberLogSucceed(request: Request):

    if request.session.get('SIGNED-IN'):

        try:

            # get all messages
            sql = '''SELECT message.id, member.name, message.content,
                     CASE WHEN member.id = %s THEN True
                          ELSE False
                     END AS own_message_judge
                     FROM message
                     JOIN member
                     ON message.member_id = member.id
                     ORDER BY message.time DESC;'''
            message_info = (request.session.get('member_id'),)
            con = db.get_connection()
            Cursor = con.cursor(dictionary=True)
            Cursor.execute(sql, message_info)
            result_messages = Cursor.fetchall()

            return templates.TemplateResponse(request=request, 
                                              name="loginSucceed.html",
                                              context={'name': request.session.get('member_name'),
                                                       'member_id': request.session.get('member_id'),
                                                       'user_messages': result_messages})
        except:

            error_message = '伺服器錯誤'
            quote_plus(error_message.encode("utf-8"))
            redirect_url = f"/error?message={error_message}"
            
            return RedirectResponse(redirect_url, headers={"message": error_message})
            
        finally:
            Cursor.close()
            con.close()
    else:
        return RedirectResponse(url='/')

# 登入或註冊失敗
@app.post("/error") 
def memberLogFail(request: Request, message: str):
    return templates.TemplateResponse(request=request, 
                                      name="loginFail.html", 
                                      context={'message': message})

# 登出
@app.get("/signout")
def logOut(request: Request):
    # set log out session
    request.session.update({"SIGNED-IN": False,
                            "member_id": '-1',
                            "member_name": '',
                            "member_username": ''})

    # delete id, name, username
    # request.session.pop('member_id')
    # request.session.pop('member_name')
    # request.session.pop('member_username')

    return RedirectResponse(url='/')

# 註冊
@app.post("/signup")
def apply_member(request: Request, name: str=Form(None), usernameUp: str=Form(None), passwordUp: str=Form(None)):

    try:

        # check db for whether already applied or not
        sql = "SELECT * FROM member WHERE username = %s"
        account = (usernameUp,)
        con = db.get_connection()
        Cursor = con.cursor(dictionary=True)
        Cursor.execute(sql, account)
        cnt_result = Cursor.fetchall()[0]['username']

        error_message = '帳號已經被註冊'
        error_message = quote_plus(error_message.encode("utf-8"))
        redirect_url = f"/error?message={error_message}"
        return RedirectResponse(redirect_url, headers={"message": error_message})

    except:

        sql = "INSERT INTO member (name, username, password) VALUES (%s, %s, %s)"
        apply_form = (name, usernameUp, passwordUp)
        Cursor.execute(sql, apply_form)
        con.commit()

        return RedirectResponse(url='/', status_code=303)
    
    finally:

        Cursor.close()
        con.close()

# 新增留言
@app.post("/createMessage")
def create_message(request: Request, message_info: member_message_info):
    
    message = message_info.message
    member_id = message_info.member_id

    # check the current log in status
    if int(member_id) == int(request.session.get("member_id")):

        try:

            # insert message into the message db table
            query = '''INSERT INTO message (member_id, content) VALUES (%s, %s);'''
            message_info = (member_id, message)
            con = db.get_connection()
            Cursor = con.cursor(dictionary=True)
            Cursor.execute(query, message_info)
            con.commit()

            return RedirectResponse(url='/member', status_code=303)
        
        except:
            error_message = '伺服器錯誤'
            quote_plus(error_message.encode("utf-8"))
            redirect_url = f"/error?message={error_message}"
            
            return RedirectResponse(redirect_url, headers={"message": error_message})
        
        finally:
            Cursor.close()
            con.close()

    else:
        
        return RedirectResponse(url='/', status_code=303)

# 刪除留言
@app.post("/deleteMessage") 
def delete_message(request: Request, message_info: member_message_deletion):

    member_id = message_info.member_id
    message_id = message_info.message_id

    # get member_id
    session_member_id = request.session.get("member_id")

    if int(member_id) == int(session_member_id):

        try:
            # delete the message from the message db table based on the delete btn clicked
            query = "DELETE FROM message WHERE id = %s;"
            message_info = (message_id,)

            con = db.get_connection()
            Cursor = con.cursor(dictionary=True)
            Cursor.execute(query, message_info)
            con.commit()

            return RedirectResponse(url='/member', status_code=303)
        
        except:
            error_message = '伺服器錯誤'
            quote_plus(error_message.encode("utf-8"))
            redirect_url = f"/error?message={error_message}"
            
            return RedirectResponse(redirect_url, headers={"message": error_message})
        
        finally:
            Cursor.close()
            con.close()


    else:
        
        return RedirectResponse(url='/', status_code=303)
        


if __name__ == '__main__':
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
