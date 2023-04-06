from flask import Flask,render_template,session,redirect,request
from utils.getData import *
from utils.querys import *
from word_cloud_picture import get_img
import random
app = Flask(__name__)
app.secret_key = 'This is a app.secret_Key , You Know ?'


@app.route('/')
def index():
    return redirect('/login')

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        request.form = dict(request.form)
        if 'passwordCheked' in request.form:
            # 注册
            if request.form['password'] != request.form['passwordCheked']:
                return '两次密码不符'
            else:
                def filter_fn(item):
                    return request.form['email'] in item

                users = query('select * from user', [], 'select')
                filter_list = list(filter(filter_fn, users))
                if len(filter_list):
                    return '该用户名已被注册'
                else:
                    query('insert into user(email,password) values(%s,%s)',
                           [request.form['email'], request.form['password']])
            session['email'] = request.form['email']
            return redirect('/home', 301)

        else:
            # 登录
            def filter_fns(item):
                return request.form['email'] in item and request.form['password'] in item

            users = query('select * from user', [], 'select')
            login_success = list(filter(filter_fns, users))
            if not len(login_success):
                return '邮箱或密码错误'

            session['email'] = request.form['email']
            return redirect('/home', 301)
    else:
        return render_template('login.html')

@app.route('/loginout',methods=['GET','POST'])
def loginout():
    session.clear()
    return redirect('/login')

@app.route('/home',methods=['GET','POST'])
def home():
    email = session['email']
    if request.method == 'GET':
        dataLen, wordLen, maxDianZan, allData, maxAddress, maxTypes, typesData, types,addressData = getHomeData()
        return render_template('index.html',
                               dataLen=dataLen,
                               wordLen=wordLen,
                               maxDianZan=maxDianZan,
                               allData=allData,
                               email=email,
                               maxAddress=maxAddress,
                               maxTypes=maxTypes,
                               typesData=typesData,
                               types=set(types),
                               typeNow='all',
                               addressRow=list(addressData.keys()),
                               addressColumns=list(addressData.values())
                               )
    else:
        type = request.form['selectType']
        dataLen, wordLen, maxDianZan, allData, maxAddress, maxTypes, typesData, types,addressData= getHomeData(type)
        return render_template('index.html',
                               dataLen=dataLen,
                               wordLen=wordLen,
                               maxDianZan=maxDianZan,
                               allData=allData,
                               email=email,
                               maxAddress=maxAddress,
                               maxTypes=maxTypes,
                               typesData=typesData,
                               types=set(types),
                               typeNow = type,
                               addressRow=list(addressData.keys()),
                               addressColumns=list(addressData.values())
                               )

@app.route('/detail/<int:id>',methods=['GET','POST'])
def detail(id):
    email = session['email']
    detailData = getDetailDataById(id)
    return render_template('detail.html',email=email,detailData=detailData[0])

@app.route('/time_t/<type>',methods=['GET','POST'])
def time_t(type):
    email = session['email']
    row,columns = getTimeData(type)
    dataLen, wordLen, maxDianZan, allData, maxAddress, maxTypes, typesData, types, addressData = getHomeData(type)
    result = getCommentTimeData()
    return render_template('time_t.html',row=row,columns=columns,type=type,types=set(types),result=result,email=email)

@app.route('/headerCount_t')
def headerCount_t():
    email = session['email']
    row,columns = getHeaderCountData()
    typeData = getCountByType()
    return render_template('headerCount_t.html',row=row,columns=columns,typeData=typeData,email=email)

@app.route('/careArticle_t')
def careArticle_t():
    email = session['email']
    row,columns = getArticleData()
    return render_template('careArticle_t.html',row=row,columns=columns,email=email)

@app.route('/tag_t',methods=['GET','POST'])
def tag_t():
    type='all'
    email = session['email']
    if request.method == 'GET':
        dicData = getTagData()
    else:
        type = request.form['selectType']
        dicData = getTagData(type)
    dataLen, wordLen, maxDianZan, allData, maxAddress, maxTypes, typesData, types, addressData = getHomeData(type)
    return render_template('tag_t.html',dicData=dicData,typeNow=type,types=set(types),email=email)

@app.route('/content_c',methods=['get','post'])
def content_c():
    email = session['email']
    typeList = getTypeList()
    img_name = random.randint(1, 9999999999)
    type = typeList[0]
    if request.method == 'POST':
        type = request.form.get('selectType')
    get_img('content', r'.\static\1.jpg', f'.\static\{img_name}.png',type)

    return render_template('content_c.html',email=email,typeList=typeList,img_name=img_name)

@app.route('/tag_c',methods=['GET','POST'])
def tag_c():
    typeList = getTypeList()
    email = session['email']
    img_name = random.randint(1, 9999999999)
    type = typeList[0]
    if request.method == 'POST':
        type = request.form.get('selectType')
    get_img('content', r'.\static\2.jpg', f'.\static\{img_name}.png',type)
    return render_template('tag_c.html', email=email, typeList=typeList,img_name=img_name)


@app.before_request
def before_requre():
    pat = re.compile(r'^/static')
    if re.search(pat,request.path):
        return
    if request.path == "/login" :
        return
    uname = session.get('email')
    if uname:
        return None

    return redirect("/login")

if __name__ == '__main__':
    app.run()
