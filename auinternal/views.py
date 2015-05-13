from pyramid.view import view_config


@view_config(route_name='home', renderer='templates/mytemplate.jinja2')
def my_view(request):
    return {'project': 'auinternal'}


@view_config(route_name="table", renderer='templates/home.jinja2')
def table(request):
    return dict(title='table', table=[["name","rollno"],['manoj', 1], ['ashwin', 2],['manoj', 1], ['ashwin', 2],['manoj', 1], ['ashwin', 2],['manoj', 1], ['ashwin', 2],['manoj', 1], ['ashwin', 2],['manoj', 1], ['ashwin', 2],['manoj', 1], ['ashwin', 2],['manoj', 1], ['ashwin', 2],['manoj', 1], ['ashwin', 2],['manoj', 1], ['ashwin', 2],['manoj', 1], ['ashwin', 2],['manoj', 1], ['ashwin', 2],['manoj', 1], ['ashwin', 2],['manoj', 1], ['ashwin', 2],['manoj', 1], ['ashwin', 2],['manoj', 1], ['ashwin', 2],['manoj', 1], ['ashwin', 2],['manoj', 1], ['ashwin', 2],['manoj', 1], ['ashwin', 2],['manoj', 1], ['ashwin', 2],['manoj', 1], ['ashwin', 2],['manoj', 1], ['ashwin', 2],['manoj', 1], ['ashwin', 2],['manoj', 1], ['ashwin', 2],['manoj', 1], ['ashwin', 2],['manoj', 1], ['ashwin', 2],['manoj', 1], ['ashwin', 2],['manoj', 1], ['ashwin', 2],['manoj', 1], ['ashwin', 2],['manoj', 1], ['ashwin', 2],['manoj', 1], ['ashwin', 2],['manoj', 1], ['ashwin', 2],['manoj', 1], ['ashwin', 2],['manoj', 1], ['ashwin', 2],['manoj', 1], ['ashwin', 2],['manoj', 1], ['ashwin', 2],['manoj', 1], ['ashwin', 2]])

