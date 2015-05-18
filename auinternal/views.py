import threading

from pyramid.view import view_config
import pymongo
from pyramid.response import Response
import requests
from bs4 import BeautifulSoup
from lxml import html


d = {}
count = 0
list1 = set()


class students:
    def getdir(self):
        return self.d

    def result(self, d):
        try:
            html1 = \
                requests.post('http://coe1.annauniv.edu:80/app/app_action/annauniv_results.php'
                              , data=self.data, headers=self.headers)
        except:
            self.result(d)
        soup = BeautifulSoup(html1.text)
        tree = html.fromstring(soup.prettify())
        result_semester = tree.xpath('//response/@value0')
        result_subject = tree.xpath('//response/@value1')
        result_grade = tree.xpath('//response/@value2')
        result_status = tree.xpath('//response/@value3')
        d['result'] = [result_semester, result_subject, result_grade,
                       result_status]

    def time(self, d):
        try:
            html1 = \
                requests.post('http://coe1.annauniv.edu:80/app/app_action/annauniv_time.php'
                              , data=self.data, headers=self.headers)
        except:
            self.time(d)
        soup = BeautifulSoup(html1.text)
        tree = html.fromstring(soup.prettify())
        time_date = tree.xpath('//response/@value0')
        time_session = tree.xpath('//response/@value1')
        time_semester = tree.xpath('//response/@value2')
        time_subject = tree.xpath('//response/@value3')
        d['time'] = [time_date, time_session, time_semester,
                     time_subject]

    def iassmark(self, d):
        try:
            html1 = requests.post('http://coe1.annauniv.edu:80/app/app_action/annauniv_iassmark.php'
                                  , data=self.data, headers=self.headers)
        except:
            self.iassmark(d)
        soup = BeautifulSoup(html1.text)
        tree = html.fromstring(soup.prettify())
        ass_subject = tree.xpath('//response/@value0')
        ass_att = tree.xpath('//response/@value1')
        ass_marks = tree.xpath('//response/@value2')
        ass_subject.insert(0, 'Subject')
        ass_att.insert(0, 'Attendence')
        ass_marks.insert(0, 'Marks')
        d['iassmark'] = [ass_subject, ass_att, ass_marks]

    def iamark(self, d):
        try:
            html1 = \
                requests.post('http://coe1.annauniv.edu:80/app/app_action/annauniv_iamark.php'
                              , data=self.data, headers=self.headers)
        except:
            self.iamark(d)
        soup = BeautifulSoup(html1.text)
        tree = html.fromstring(soup.prettify())
        iass_sem = tree.xpath('//response/@value0')
        iass_subject = tree.xpath('//response/@value1')
        iass_internal = tree.xpath('//response/@value2')
        iass_absent = tree.xpath('//response/@value3')
        d['iamark'] = [iass_sem, iass_subject, iass_internal,
                       iass_absent]

    def elective(self, d):

        try:
            html1 = \
                requests.post('http://coe1.annauniv.edu:80/app/app_action/annauniv_elective.php'
                              , data=self.data, headers=self.headers)
        except:
            self.elective(d)
        soup = BeautifulSoup(html1.text)
        tree = html.fromstring(soup.prettify())
        elective_subject = tree.xpath('//response/@value1')
        d['elective'] = [elective_subject]

    def __init__(self, a):
        global count, invalid, list1
        self.reg = a
        self.headers = \
            {'Authorization': 'Basic ZW1zYXU6IUJlc3RHdW5AIzIwMTMh'}
        d = dict()
        d['_id'] = self.reg
        self.data = dict(regno=a)
        self.d = dict()
        if (count < 10 or self.reg[:len(self.reg) - 3] != invalid):

            html1 = \
                requests.post('http://coe1.annauniv.edu:80/app/app_action/annauniv_profile.php'
                              , data=self.data, headers=self.headers)
            error = "<?xml version='1.0' encoding='ISO-8859-1' ?><sdp><response LayoutType='Table' row='2' column='0' id='tableHeader'><val type='Text' def='Student Profile'/><val type='Text' def='No Record Found'/></response></sdp>"
            if html1.text.replace("\n", "").replace("\t", "") == error.replace("\n", "").replace("\t", ""):
                self.d['profile'] = 1
            else:
                list1.add(self.reg)
                print self.reg, "\t", len(list1)
                count = 0
                soup = BeautifulSoup(html1.text)
                tree = html.fromstring(soup.prettify())
                profile = tree.xpath('//response/@value')
                d['profile'] = profile
#======================thread implementation=======================
                therds = []
                p2 = threading.Thread(target=self.elective, args=(d, ))
                therds.append(p2)
                p3 = threading.Thread(target=self.iamark, args=(d, ))
                therds.append(p3)
                p4 = threading.Thread(target=self.iassmark, args=(d, ))
                therds.append(p4)
                p5 = threading.Thread(target=self.time, args=(d, ))
                therds.append(p5)
                p6 = threading.Thread(target=self.result, args=(d, ))
                therds.append(p6)
                [i.start() for i in therds]
                [i.join() for i in therds]
#======================normal implementation=======================
                # self.elective(d)
                # self.iamark(d)
                # self.iassmark(d)
                # self.time(d)
                # self.result(d)
                conn = pymongo.MongoClient()
                db = conn.student
                db.student.save(d)
                self.d = d


@view_config(route_name='home', renderer='templates/mytemplate.jinja2')
def my_view(request):
    return {'project': 'auinternal'}


@view_config(route_name="table", renderer='templates/table.jinja2')
def table(request):
    id = request.POST.items()
    # find=db.student.find_one({'_id':str(id[0][1])})
    student = students(str(id[0][1]))
    find = student.getdir()
    if find['profile'] == 1:
        return Response(
            "<html><head><script>alert('Invalid Reg_No');window.location = '/login';</script></head></html>")
    return dict(title=find['profile'][2], table=find['iassmark'], len=len(find['iassmark'][1]))


@view_config(route_name="login", renderer='templates/login.jinja2')
def login(request):
    return ()


@view_config(route_name='formcheck', renderer='templates/table.jinja2')
def form(request):
    maonj = request.POST.items()
    return dict(title='table', table=maonj, len=2)


@view_config(route_name='session')
def myview(request):
    session = request.session
    if 'abc' in session:
        session['fred'] = 'yes'
    session['abc'] = '123'
    if 'fred' in session:
        manoj = session['abc']
        session.invalidate()
        return Response(manoj)
    else:
        return Response('Fred was not in the session')