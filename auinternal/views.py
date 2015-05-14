from pyramid.view import view_config
import pymongo
conn=pymongo.MongoClient()
db=conn.student

@view_config(route_name='home', renderer='templates/mytemplate.jinja2')
def my_view(request):
    return {'project': 'auinternal'}


@view_config(route_name="table", renderer='templates/home.jinja2')
def table(request):
    find=db.student.find_one({'_id':'110113205003'})
    return dict(title='table', table=find['iassmark'],len=len(find['iassmark'][1]))

