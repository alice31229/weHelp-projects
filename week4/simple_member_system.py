import uvicorn
from fastapi import FastAPI, Request, Form
from starlette.middleware.sessions import SessionMiddleware
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from urllib.parse import quote_plus

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key='SECRET_KEY')
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

user_list = {'username': 'test', 'password': 'test'}


# 首頁
@app.get("/") 
async def welcome_home(request: Request):
    return templates.TemplateResponse(
        request=request, 
        name="homePage.html")

# 驗證帳號、密碼 
@app.post("/signin") 
def verify_account(request: Request, username: str = Form(None), password: str = Form(None)):    
    pass_or_not = False
    if username == user_list["username"] and password == user_list["password"]:
        pass_or_not = True

    # router redirect handle
    if pass_or_not:

        # set logIn session
        request.session.update({"SIGNED-IN": True})
        return RedirectResponse(url='/member', status_code=303)

    else:
        error_message = ''
        if username == None or password == None:
            error_message = '請輸入帳號、密碼'
        else:
            error_message = '帳號、或密碼輸入錯誤'
        
        error_message = quote_plus(error_message.encode("utf-8"))
        redirect_url = f"/error?message={error_message}"
        return RedirectResponse(redirect_url, headers={"message": error_message})
        

# 登入成功
@app.get("/member") 
def memberLogSucceed(request: Request):
    if request.session.get('SIGNED-IN'):
        return templates.TemplateResponse(
            request=request, 
            name="loginSucceed.html")
    else:
        return RedirectResponse(url='/')

# 登入失敗
@app.post("/error") 
def memberLogFail(request: Request, message: str):
    return templates.TemplateResponse(
        request=request, 
        name="loginFail.html", 
        context={'message': message}
    )

# 登出
@app.get("/signout")
def logOut(request: Request):
    # set log out session
    request.session.update({"SIGNED-IN": False})
    return RedirectResponse(url='/')

# 正整數平方
@app.post("/square/{integer}")
def print_result(request: Request, integer: str):
    result = int(integer)**2
    return templates.TemplateResponse(
        request=request, name="calculateSquare.html", context={"result": result}
    )

# 正整數平方 後端再轉一次
# @app.get("/square/{integer}")
# def print_result(request: Request, integer: str):
#     result = int(integer)**2
#     print(result)
#     return templates.TemplateResponse(
#         request=request, name="calculateSquare.html", context={"result": result}
#     )

# @app.post("/square")
# def recieve_num(integer: str = Form(None)):
#     redirect_url = f"/square/{integer}"
#     return RedirectResponse(redirect_url, status_code=303, headers={"integer": integer})


if __name__ == '__main__':
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
