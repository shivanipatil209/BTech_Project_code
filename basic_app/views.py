from django.shortcuts import render,redirect
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import credentials
from basic_app.models import usersignup,userlogin
import MySQLdb
import pymysql
from sqlalchemy import create_engine
import os 
from django.contrib import messages
from sqlalchemy.orm import scoped_session,sessionmaker
# Create your views here.

# from .firebase1 import firefunc

cd = credentials.Certificate(
{
"type": "service_account",
"project_id": "firedjang",
"private_key_id": "6c1d9c1a5752f1c7cb954da924519b4a8ded9824",
"private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDEdZto8uR1o9Ir\nKTmDqiHDZAbZeoKrxEapumg9htNF4QnIer0qoWh6SZ87CSwKOJtYEvNIYOFu3mEG\nUad4MDuNruZT2avf0uzzWiPjbiPfhlVpd91hhskWkos38eM4BPIhlH1It3EXQVqL\nQxQ8NReTOMraGYjQ6/8xzIxT0pYM3p7PSRQMBjI8koa6uEnFprSx6gR07P09uS2A\nDIfdl94cNJd95WKifoGUhtwcsholm0cPnzon3y3bsS0ghi5hqC/P12Jk2pgR6SQW\n6/b/NyJlhk2pjef13bTrJeUZUj6Cze8xqMcrFxh8QeYAHZSjxXdFpg7Z0crAGDgl\nABT7Lei7AgMBAAECggEAAZz6b76A93SQXCaqIGKuDJbWAReTw+AxwLOvpstVPp2A\n8iZmsAR8hQ1AW9sB3dXa3aQDXzlWFFHVrk0LK7xGmOnqqUNtV1FBdZySFNAYr/X8\ng9r82h7lt4X/iCD72ho7Wmh40z7FMrKKa5bbZADwMQCNw/yIkqGrHP3G6J9MQ7dr\n/Kz39OViDvB3D5UM9oVhX8MD8jwIQrIe6M+lkB7mWN28bv5vTbbR8sUsgXTnKpR4\nM4bRbyx0RqXygmPmF5YPeIggD2w8XNT917x7D0bXZJ+QOL672g2E33C366/vH1UC\noey47eF9bkHy4pf1FMW6qDJB3jmHpgXnJ4SDcjAaCQKBgQDqgaY3zZSXLx/thj1r\nRBNiGw5VCVGmJPz3mNOx8dbGhUqNj+BPI4jJl+iEZC4yJbj607KcBVrhTs5Gu29X\n5nkYzxY90vFugd25vlGG5g0f/Qe90NIurDD4iZO2CfeUZ+USQsK7wnosoqHiJ7PF\npj0+JXQtS0Ljznw4Avbn5RV94wKBgQDWdz1YlGKSmjCLjg47khNr5unQxM/dvS0c\n4IkQ6D8EB2vR7MRrpAGP4vTKO+VImqJAXwiMkMs3nMzby/gtWMM3oQIBSfPJMytY\nM+6Uwla6nw2u8U8wTUo+emsS+3GPmtNVSjSQSqA+MoqjZZAseCUO1lx32L87jWge\nverxrl5hSQKBgCXoY1gt8VEnGwAobRFD5eY7/WsdoIc8/29+0um28EMTFOQhV98z\nHU+JMNsF3rnYgzh4tCyoaPJ27L1eWzdYWEb8YtoHmWOFtrPp4f/ufDypiHDUqsVE\nrH3gr3ID1nO0/8Cd7iCv5VQFzilixZqzrr63CzqvKdbtcAMV55fA3mKFAoGBAIB+\n3NCPxyeTHnbe3AQxF1XU+k5NPUXbrIXaugTZQbhGQgF63IyprQ3qq0Pn8w43J/Nt\nfQ/LSRa+6bbfVIjG3+Aapbrj9h6ce+HS66VRculJlsc0aX/FLzCT5EdxQ68I0ooN\ndcTmEXByk8ImfeVG7t0e7jQYNyuVI8cXfwbitEWRAoGARhx4kt2XXr09WbzQ/pnT\nDu80hT6eMQGMZ1HJlw3j8eBpN0vs8Hx6HsN4bqejyQ8ij9Wh4NsSQ3XqtBH+7wcS\n5TKG/m7js4+3pVLZ+PjMbefwFvx1cefy/NbcySTw+9K79BqsnPxwmxJ3lKQkWOL2\nkxMKG12sL/hchaaRUCHAMLE=\n-----END PRIVATE KEY-----\n",
"client_email": "firebase-adminsdk-lri3f@firedjang.iam.gserviceaccount.com",
"client_id": "114260328089911705184",
"auth_uri": "https://accounts.google.com/o/oauth2/auth",
"token_uri": "https://oauth2.googleapis.com/token",
"auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
"client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-lri3f%40firedjang.iam.gserviceaccount.com"
}
)

firebase_admin.initialize_app(cd)
datab = firestore.client()

def home(request):
       return render(request,"basic_app/home_page.html")

def contactUs(request):
        return render(request, "basic_app/contact_us.html")

def userGuide(request):
    return render(request,"basic_app/user_guide.html")

def login(request):
    return render(request, "basic_app/login.html")

def signup(request):
    return render(request, "basic_app/signup.html")



def user_signup(request):
    if request.method == 'POST':
        if request.POST.get('username') and request.POST.get('pswd'):
            saverecord = usersignup()
            saverecord.username=request.POST.get('username')
            saverecord.pswd=request.POST.get('pswd')
            # saverecord.save()
            # print(saverecord.username)
            # messages.success(request,"Signup successfull")

            engine1 = create_engine("mysql+pymysql://{user}:{pw}@localhost/{db}"
            .format(user="root",pw="",db="text_data"))

            query = "INSERT INTO users (username,pswd) VALUES (%s,%s)"
            engine1.execute(query,(saverecord.username,saverecord.pswd))
            messages.warning(request, "Successfully signed up!!")
            return redirect('login')
        else:
            messages.error(request,"Please add all fields") 
            return render(request,'basic_app/signup.html') 
            
    else:
        
        return render(request,'basic_app/signup.html')

def user_login(request):
    if request.method == 'POST':
        if request.POST.get('username') and request.POST.get('pswd'):
            saverecord = userlogin()
            saverecord.username=request.POST.get('username')
            saverecord.pswd=request.POST.get('pswd')
            username=saverecord.username            
            pswd=saverecord.pswd
          

            # saverecord.save()
            # print(saverecord.username)
            engine1 = create_engine("mysql+pymysql://{user}:{pw}@localhost/{db}"
            .format(user="root",pw="",db="text_data"))

            db=scoped_session(sessionmaker(bind=engine1))


            usernamedata = db.execute("SELECT username from users where username=:username",{"username":username}).fetchone()
            pswddata = db.execute("SELECT pswd from users where username=:username",{"username":username}).fetchone()
            is_user=0
            print(usernamedata!=None)
            
            if(usernamedata!=None):
                if(pswd == pswddata[0]):
                    is_user =1
            else:
                is_user = 0


            if is_user==1:
                messages.success(request, "Login Successfull" )
                return redirect('predict')
                print("Successfull login")

            else:
                messages.error(request, 'Invalid Credentials')
                print("Invalid credentials")
                return render(request,'basic_app/login.html')
        else:
            messages.warning(request,"Please add all fields")
            return render(request,'basic_app/login.html')


    else:
        return render(request,'basic_app/login.html')


'''
def Nifty_table(request):
    # gn = getNifty50()
    r = requests.get("https://appfeeds.moneycontrol.com/jsonapi/market/marketmap&format=&type=0&ind_id=9")
    res = r.json()
    # Dump data as string
    data = json.dumps(res)
    print(data)

    # Extract specific node content.
    # print(res["item"])
    
    
    pd.set_option('display.max_columns', None)
    nifty_df = pd.json_normalize(res["item"])
    # print(pd.json_normalize(res["item"]).head(5))
    nifty_df = pd.DataFrame(nifty_df)
    # print(nifty_df.head(5))
    nifty_df = nifty_df.drop(columns=['url','stk_details'])
    nifty_df['Sno'] = range(1, len(nifty_df) + 1)
    nifty_df = nifty_df[['Sno','id','shortname','mktcap','lastvalue','change','percentchange','direction','volume']]
    df = pd.DataFrame(nifty_df)
    json1 = nifty_df.to_json()
    print(type(json1))
    json1 = json.loads(json1)
    print("bs yrr,chl ja",json1)
    print("11",type(json1))
    print("lalaa",json1['Sno'])
    # print("AAAA",json1['item'][0][id] )

    

    #   response=requests.get(url).json()
    # #logger.info(response)
    # print("HHHHHH")
    # return render(request,'fake_news.htm',{'response':response})
    
    return render(request,'app1/modules/nifty50.html',{'response':json1})

#     from django.http import JsonResponse
# from .models import Students

# def jsondata(request):
# 	data list(Students.objects.values())
# 	return JsonResponse(data,safe = False)



    # json = dataFrame.to_json()



   
# def fireupdates(request):
#     doc_ref = datab.collection(u'usersInfo').document(u'ID6')
#     doc_ref.set({
#         u'first': u'bla',
#         u'last': u'cla',
#     })
#     return render(request,'app1/modules/firebasetry.html')

#  if request.method == 'POST':
#         if request.POST.get('checknews'):
#             print("yayyyyyyyyyy")
#             gn = getNews()
#             gn.getNews=request.POST.get('checknews')
#             payload=gn.getNews
#             #payload = "/hi there"
#             url1 = "http://108f5f7fbbdf.ngrok.io/cn"
#             url=url1+"/"+payload
#             print(url)
#     response=requests.get(url).json()
#     #logger.info(response)
#     print(response)
#     print("HHHHHH")
#     return render(request,'fake_news.htm',{'response':response})

# def nifty50(request):
#     res = r.json()
#     # Dump data as string
#     data = json.dumps(res)
#     print(data)

#     # Extract specific node content.
#     # print(res["item"])
    
    
#     pd.set_option('display.max_columns', None)
#     nifty_df = pd.json_normalize(res["item"])
#     # print(pd.json_normalize(res["item"]).head(5))
#     nifty_df = pd.DataFrame(nifty_df)
#     # print(nifty_df.head(5))
#     nifty_df = nifty_df.drop(columns=['url','stk_details'])
#     nifty_df['Sno'] = range(1, len(nifty_df) + 1)
#     nifty_df = nifty_df[['Sno','id','shortname','mktcap','lastvalue','change','percentchange','direction','volume']]
#     df = pd.DataFrame(nifty_df)

#     # html_nifty(df)--
#      # # Parses the dataframe into an HTML element with 3 Bootstrap classes assigned.
#     # html = df.to_html(classes=["table-bordered", "table-striped", "table-hover"])
#     # # print(nifty_df.head(5))
#     return render(request,'app1/modules/nifty50.html')





# def html_nifty(df_nifty_html):--
#     df_nifty_html = df_nifty_html
#     print(df_nifty_html)



    #Dash app
    # Indices_layout = html.Div([
            
    # dbc.Jumbotron([
    #                dash_table.DataTable(
    # data=df_nifty_html.to_dict('records'),
    # columns=[{'id': c, 'name': c} for c in df_nifty_html.columns],
    # style_cell_conditional=[
    #     {
    #         'if': {'column_id': c},
    #         'textAlign': 'left'
    #     } for c in ['Date', 'Region']
    # ],

    # style_as_list_view=True,
    # )
       
    # ])
    
    # ], style={'marginLeft': 80, 'marginRight': 80, 'marginTop': 40, 'marginBottom': 20, 'background-color':'#8EB9E3 ', 'font_size':14})
    # app = JupyterDash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP,'https://bootswatch.com/sandstone/'],suppress_callback_exceptions=True)

    # app.run_server(mode='external',port=8052)
'''








