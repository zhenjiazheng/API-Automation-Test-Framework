# coding=UTF-8
'''
Created on 2015年12月02日
'''

import jsonrpclib
import simplejson
from jinja2 import Template
import os
import unittest
import pymysql
import re
import time
import sys
reload(sys)
sys.setdefaultencoding('utf8')
 
# JSONRPC_ENTRY_URL = "112.74.65.224"  #"192.168.1.188:8080"
JSONRPC_ENTRY_URL = "localhost:8080"

#Database operation config
host = "localhost"
user = "test"
psw = "test"
dbname = "xw"
port = "3306"
btool = '/usr/local/mysql/bin/mysqldump'
rtool = '/usr/local/mysql/bin/mysql'
testDict = {"User1":"13554321888","User2":"13664321999","User3":"13664321000", "User4":"13664322000", "User":"13500044444","MUser1":"13798765888","MUser2":"13898765999","Password":"123456","ResourceMobile1":"13798765123","ResourceMobile2":"13809090909","ResourceMobile3":"13798765100","ResourceMobile4":"13798765101","ResourceMobile5":"13798765102","ResourceMobile6":"13798765103","ResourceMobile7":"13798765104","ResourceMobile8":"13798765105","ResourceMobile9":"13798765106","ResourceMobile10":"13798765107","ResourceMobile11":"13798765108","ResourceMobile12":"13798765109","ResourceMobile13":"13798765110","ResourceMobile14":"13798765111","ResourceMobile15":"13798765112","ResourceMobile16":"13798765113","TUser1":"13510101010","TUser2":"13510101011","TUser3":"13510101012","TUser4":"13510101013","GUser":"13800000000","BUser1":"13794491000","BUser2":"13794491001","BUser3":"13794491002", "BUser4":"13794491003", "BUser":"13794491004","BMUser1":"13794492000","BMUser2":"13794492001","BResourceMobile1":"13794493000","BResourceMobile2":"13794493001","BResourceMobile3":"13794493002","BResourceMobile4":"13794493003","BTUser1":"13794494000","BTUser2":"13794494001","BTUser3":"13794494002","BTUser4":"13794494003","BGUser":"13794495000","Admin":"13511111111","Admin2":"13522222222","Admin3":"13533333333"}
ROOT_DIR =  os.path.dirname(__file__)
folder = os.environ.get('CASE_FOLDER', "M0")
SUITE_DIR = os.path.join(ROOT_DIR, folder)#"M0")
# SUITE_DIR = os.path.join(ROOT_DIR, "test-suite")
# test-suite


sleepTime = float(os.environ.get('SLEEP_TIME', 0))

def jsonrpc(url, rest,methodname, params, rpcid=None):
    SERVER_URL = "http://"+url +rest
    api = jsonrpclib.Server(SERVER_URL, verbose=True)
    return api._request(methodname=methodname, params=params, rpcid=rpcid if rpcid else 100)



class Context(object):

    def __init__(self):
        self.lastReponse = None
        self.allResponses = []
        self.checker = None
        self.error = None
        self.valueDict = {}
        self.selectableList = []
        self.Keys = {}
        self.AllKeys ={}

def parseCaseList():
    for root, dirs, files in os.walk(SUITE_DIR):
        caseList = dirs
        return caseList


def seperateCaseStep(case):
    for root ,dirs, files in os.walk(os.path.join(SUITE_DIR,case)):
        stepList = []
        for each in files:
            each = os.path.join(os.path.join(SUITE_DIR,case),each)
            stepList.append(each)
#         print "The Case steps: "
#         print stepList
        return stepList


caseLists = parseCaseList()
# stepList = seperateCaseStep(caseLists[0])
# allStepList = []
# for i in xrange(len(caseLists)):
#     allStepList.append(seperateCaseStep(caseLists[i]))

# print allStepList
# exit()

def getValueByKey(Context,jdict,param):
    # print jdict
    if param.endswith("?"):
        param = param[:-1]
        Context.selectableList.append(param)
    if isinstance(jdict, list):
        if type(jdict).__name__ == "int":
            print "The response value is type int."
            pass
        else:
            for element in jdict:
                if type(element).__name__ == "int":
                    pass
                else:
                    getValueByKey(Context,element,param)
                    if element.has_key(param):
                        Context.valueDict.update({param:element[param]})
                    else:
                        pass
    elif isinstance(jdict, dict):
        if param in jdict.keys():
            Context.valueDict.update({param:jdict[param]})
        else:
            for x in jdict.keys():
                getValueByKey(Context,jdict[x],param)
                if x == param:
                    Context.valueDict.update({param :jdict[param]})
                    #print Context.valueDict
                else:
                    pass
    # else:
    #     Context.selectableList.append(param)

# cont = Context()
# getValueByKey(cont, jdict, "pluginId")
# print cont.valueList
# valueList = [dict(t) for t in set([tuple(d.items()) for d in cont.valueList])]
# print valueList
# exit()


def backupDB(target):
    print 'Start to backup'
    command = '%s -h%s -u%s -p%s %s > %s' % (btool, host, user, psw, dbname, target)
    #print command
    try:
        os.system(command)
        #print 'Success'
    except Exception , e :
        #print 'Fail'
        print e

def restoreDB(source):
    print 'Start to restore sql'
    command = '%s -h%s -u%s -p%s -P3306 %s < %s' % (rtool, host, user, psw, dbname, source)
    #print command
    try:
        os.system(command)
        #print 'Success'
    except Exception , e :
        #print 'Fail'
        print e


def execSql(sql):
    try:
        conn = pymysql.connect(host=host,user=user,passwd=psw,db=dbname,charset='utf8')
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        r = cur.fetchall()
        cur.close()
        conn.close()
        return r
    except Exception,e:
        print 'Mysql Error %d: %s' % (e.args[0], e.args[1])
#





def typeValidator( params, value):
#     print "inner print:"
#     print params
#     print type(params)
#     print value
#     print "inner done"
#     if type(params).__name__ == value:
    if type(params).__name__ == value:
        return True
    else:
        return False

def typeInValidator( params, value):
#     print "inner print:"
#     print params
#     print type(params)
#     print value
#     print "inner done"
#     if type(params).__name__ == value:
    for key in value:
        if type(params).__name__ == key:
            return True
        else:
            pass
    return False

def andValidator(params, value):
    if not isinstance(params, int):
        #print "Not Int params"
        return False
    if params >= value[0] and params <= value[1]:
        return True
    else:
        return False

def valuesValidator(params, value):
    mark = 0;
    for i in xrange(len(value)):
        if params == value[i]:
            mark =+ 1
    if mark == len(value):
        return True
    else:
        return False

def lenValidator(params, value):
    if len(params) == len(value) :
        return True
    else:
        return False

def equalValidator( params, value):
    if params == value:
        return True
    else:
        return False


def inValidator(param,val):
    lm = 0
    for i in range(len(val)):
        if param == val[i]:
            lm += 1
            print "Find the value in index : %d"%(i+1)
        else: pass
    if lm == 1:
        return True
    else:
        return False

def inRangeValidator(params, value):
    if params in value:
        return True
    else:
        return False

def notInValidator(params, value):
    mark = 0
    for i in xrange(len(value)):
        if params != value[i]:
            mark =+ 1
    if mark == len(value):
        return True
    else:
        return False

def greaterValidator(params, value):
    if params >= value:
        return True
    else:
        return False
#
# def nullValidator(params, value):
#     if params is None:
#         return True
#     else:
#         return False

def regValidator(params,value):
    try:
        val = re.match(value,params)
        if val.group(0):
            return True
        else:
            return False
    except:
        return False

class ValidatorRegistry(object):

    registry = {}

    @classmethod
    def register(cls,name, validate):
        cls.registry[name] = validate

    @classmethod
    def validate(cls,name, params, value):
        return cls.registry[name].validate(params, value)

def checker(newPara,typo,params,value):
    val = ValidatorRegistry()
    if typo == "type":
        if(("startAt"  in newPara or "endAt" in newPara or "createAt" in newPara or "timeStamp" in newPara or "Time" in newPara)):
              val.register("type", typeValidator(params, "long"))
              if(val.registry["type"] is False):
                   val.register("type", typeValidator(params, "int"))
        else:
           val.register("type", typeValidator(params, value))
    if typo == "len":
        val.register("len", lenValidator(params, value))
    if typo == "&&":
        val.register("&&", andValidator(params, value))
    if typo == "==":
        val.register("==", equalValidator(params, value))
    if typo == "in":
        val.register("in", inRangeValidator(params, value))
    if typo == ">=":
        val.register(">=", greaterValidator(params, value))
    if typo == "reg":
        val.register("reg", regValidator(params, value))
    if typo == "values":
        val.register("values", valuesValidator(params, value))
    if typo == "notIn":
        val.register("notIn", notInValidator(params, value))
    if typo == "typeIn":
        val.register("typeIn", typeInValidator(params, value))
    # if typo == "null":
    #     val.register("null", nullValidator(params, value))
    return val.registry[typo]


# print "Pretest:"
# print checker("&&","hello",["hell0","world","start"])
# print checker("&&",10,[3,30])
# print "-"*100






def runCase(context, files):
    flag = False
    for fname in files:

        print "*"*100
        print "\nThis is the step : %d.\n" %(files.index(fname)+1)
        print "*"*100 + "\n"
        #json_filename = os.path.join(root, fname)
        context.checker = {}
        #print json_filename
        raw_json_str = open(fname).read()
        #raw_json_str = open(json_filename).read()
        try:
            t = Template(raw_json_str)
            json_str = t.render(LAST = context.lastReponse, ALL = context.allResponses , DICT = testDict)
        except Exception,e:
            print e
            return False

        # ...
        d = simplejson.loads(json_str)
        rest = d["request"]["rest"]
        methodname = d["request"]["method"]
        params = d["request"]["params"]
        context.checker = d
        context.lastReponse = []
        context.valueDict = {}
        context.selectableList = []
        context.error = None

        if "SQLHandler" == methodname:
            try:
                result=execSql(d["request"]["params"])
                print result
                if "SELECT" in d["request"]["params"]:
                    print d["request"]["params"]
                    context.lastReponse = result[0][0]
                    #print context.lastReponse
                    context.allResponses.append(context.lastReponse)
                elif "UPDATE" in d["request"]["params"]:
                    print d["request"]["params"]
                    context.lastReponse = result
                    context.allResponses.append(context.lastReponse)
                elif "INSERT" in d["request"]["params"]:
                    print d["request"]["params"]
                    context.lastReponse = result
                    context.allResponses.append(context.lastReponse)
                else:
                    pass
            except Exception,e:
                print e
            #Perform the sql query or handle
        else:
            try:
                context.lastReponse = jsonrpc(JSONRPC_ENTRY_URL, rest, methodname, params)
                # print context.lastReponse
                context.allResponses.append(context.lastReponse)

                #return json_resp, d
            except jsonrpclib.jsonrpc.ProtocolError, e:
                error_info = e.args[0]
                print u"ProtocolError: {}, Message: {}".format(error_info[0], error_info[1])
        #         return  e
                context.error = "{}".format(error_info[0])
                context.lastReponse = "ERROR"
                print context.error
            except Exception, e:
                print e
                return False
            try:
                if context.checker.has_key("result"):
                    if not isinstance(context.lastReponse, dict):
                        if context.checker["result"] is None:
                            if context.lastReponse is None:
                                flag = True
                            elif context.lastReponse == "ERROR":
                                print "Response Error."
                                return False

                        elif context.lastReponse == "ERROR":
                            print "Response Error."
                            return False

                        elif type(context.lastReponse).__name__ == "int" or "str":
                            for typo in context.checker["result"].keys():
                                if checker("result",typo, context.lastReponse,context.checker["result"][typo]):
                                    flag = True
                    # if isinstance(context.lastReponse, list):
                    #     if len(context.lastReponse) > 0:
                    #         for item in context.checker["result"].keys():
                    #             getValueByKey(context, context.lastReponse, item)
                    else:
                        for item in context.checker["result"].keys():
                            getValueByKey(context, context.lastReponse, item)
                        value = list(set(context.selectableList))
                        for para  in context.checker["result"].keys() :
                            # print "The checker key: %s , value: %s"%(para,context.checker["result"][para])
                            if para.endswith("?"):
                                newPara = para[:-1]
                            else:
                                newPara = para

                            if newPara not in value:
                                # print newPara
                                for typo in context.checker["result"][para].keys():
                                    if type(context.valueDict[newPara]).__name__ == "unicode":
                                        params = context.valueDict[newPara].encode("utf-8")
                                    else:
                                        params = context.valueDict[newPara]
                                    # print params
                                    if type(context.checker["result"][para][typo]).__name__ == "unicode":
                                        valueEx = context.checker["result"][para][typo].encode("utf-8")
                                    else:
                                        valueEx = context.checker["result"][para][typo]
                                    print valueEx,params
                                    if params is None:
                                        print "The return value of %s is null."%newPara
                                        flag = True
                                    elif checker(newPara,typo, params,valueEx):
                                    # if checker(newPara,typo, params,valueEx):
                                            flag = True
                                    else:
                                        print "Parameter %s checker is FAIL."%para
                                        return False
                            else:
                                for each in value:
                                    new_key = each+"?"
                                    if new_key not in context.checker["result"].keys():
                                        if new_key not in context.valueDict.keys():
                                            print "Parameter %s checker is FAIL."%new_key[:-1]
                                            return False
                                        else:
                                            for typo in context.checker["result"][new_key].keys():
                                                if type(context.valueDict[each]).__name__ == "unicode":
                                                    params = context.valueDict[each].encode("utf-8")
                                                else:
                                                    params = context.valueDict[each]

                                                if type(context.checker["result"][new_key][typo]).__name__ == "unicode":
                                                    valueEx = context.checker["result"][new_key][typo].encode("utf-8")
                                                else:
                                                    valueEx = context.checker["result"][new_key][typo]
                                                if checker(newPara,typo, params,valueEx):
                                                    flag = True
                                                else:
                                                    print "Parameter %s checker is FAIL."%para
                                                    return False
                            if flag:
                                print "Parameter %s checker is PASS."%para
                elif context.checker.has_key("error"):
            #         d = simplejson.loads(jsonString)
                    if context.error:
                        if context.checker["error"]["code"] == int(context.error):
                            print "PASS"
                            flag = True
                        else:
                            print "The expected error code {0} is not equal the error code in response {1}  ".format(context.checker["error"]["code"],context.error)
                            return False
                    else:
                        print "The expected error code {0} is not response.".format(context.checker["error"]["code"])
                        return False

            except Exception ,e:
                print e
                return False
        # time.sleep(2)
        time.sleep(sleepTime)
    if flag:
        return True





#
# caseLists = parseCaseList()
# stepList = seperateCaseStep(caseLists[0])
# allStepList = []
# for i in xrange(len(caseLists)):
#     allStepList.append(seperateCaseStep(caseLists[i]))



class UnitTest(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)
        backupDB("%s/backup.sql" % os.path.dirname(os.path.abspath(__file__)))


    def tearDown(self):
        unittest.TestCase.tearDown(self)
        restoreDB("%s/backup.sql" % os.path.dirname(os.path.abspath(__file__)))

    def Testcase(self,each):

#         for each in allStepList:
        context = Context()
        self.assertTrue(runCase(context,each), "TestFail")

    @staticmethod
    def getTestFunc(stepList):
        def func(self):
            self.Testcase(stepList)
        return func

# def __generateTestCases():
#     arglists = []
#     CaseNameLists = caseLists
#     print CaseNameLists
#     for i in xrange(len(caseLists)):
#         stepList = seperateCaseStep(caseLists[i])
#         arglists.append(stepList)
#     print arglists
# #     #item = GT().run()
# #     item = int(os.environ.get('UT_ITEM', -1))
# #     print '-' * 60
# #     if item == -1:
# #         print 'current test suite is ALL TESTS'
# #     else:
# #         print 'current test item is: %d' % item
# #     print '-' * 60
# #     if item == -1:
#     for i in xrange(len(arglists)):
#         test_func = "test_" + CaseNameLists[i]
#         setattr(UnitTest, test_func,
#             UnitTest.getTestFunc(arglists[i]))
# #     else:
# #         test_func = "test_" + CaseNameLists[item]
# #         setattr(ExecuteTest, test_func,
# #             ExecuteTest.getTestFunc(*arglists[item]))
# __generateTestCases()

# restoreDB("%s/backup.sql" % os.path.dirname(os.path.abspath(__file__)))

def suite():
    arglists = []
    CaseNameLists = caseLists
    print CaseNameLists
    for i in xrange(len(caseLists)):
        stepList = seperateCaseStep(caseLists[i])
        arglists.append(stepList)
    print arglists
    item = int(os.environ.get('UT_ITEM', -1))

    print '-' * 60
    if item == -1:
        print 'current test suite is ALL TESTS'
    else:
        print 'current test item is: %d' % (item+1)
    print '-' * 60

    if item == -1:
        for i in xrange(len(arglists)):
            test_func = "test_" + CaseNameLists[i]
            setattr(UnitTest, test_func,
                UnitTest.getTestFunc(arglists[i]))
    else:
        test_func = "test_" + CaseNameLists[item]
        setattr(UnitTest, test_func,
            UnitTest.getTestFunc(arglists[item]))
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(UnitTest))
    return suite

if __name__ == "__main__":
    # unittest.main()
    restoreDB("%s/backup.sql" % os.path.dirname(os.path.abspath(__file__)))
    # backupDB("%s/backup.sql" % os.path.dirname(os.path.abspath(__file__)))
#     print execSql("UPDATE service set `status` = 1 where id = 2")
#     print execSql("SELECT status from service where id = 2")

# main()

