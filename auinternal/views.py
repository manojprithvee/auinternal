from pyramid.view import view_config
import pymongo
from pyramid.response import Response
from student import student
conn=pymongo.MongoClient()
db=conn.student

@view_config(route_name='home', renderer='templates/mytemplate.jinja2')
def my_view(request):
    return {'project': 'auinternal'}


@view_config(route_name="table", renderer='templates/table.jinja2')
def table(request):
    id=request.POST.items()
    find=db.student.find_one({'_id':str(id[0][1])})
    return dict(title='table', table=find['iassmark'],len=len(find['iassmark'][1]))



@view_config(route_name="login", renderer='templates/login.jinja2')
def login(request):
    return ()


@view_config(route_name='formcheck', renderer='templates/table.jinja2')
def form(request):
    maonj=request.POST.items()
    return dict(title='table', table=maonj ,len=2)



@view_config(route_name='session')
def myview(request):
    session = request.session
    if 'abc' in session:
        session['fred'] = 'yes'
    session['abc'] = '123'
    if 'fred' in session:
        manoj=session['abc']
        session.invalidate()
        return Response(manoj)
    else:
        return Response('Fred was not in the session')