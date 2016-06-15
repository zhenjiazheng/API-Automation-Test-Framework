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
import platform
import sys
import re
import time

reload(sys)
if "Windows" in platform.platform():
    sys.setdefaultencoding('gb18030')
else:
    sys.setdefaultencoding('utf-8')

print("############ Windows #############")

# JSONRPC_ENTRY_URL = "112.74.65.224"  #"192.168.1.188:8080"
JSONRPC_ENTRY_URL = "localhost:8080"

#Database operation config
host = "localhost"
user = "root"
psw = "111111"
dbname = "ppw"
port = "3306"
btool = 'E:/mysql-5.6.17-winx64/bin/mysqldump'
rtool = 'E:/mysql-5.6.17-winx64/bin/mysql'
testDict = {"Admin":"13511111111","User1":"13554321888","User2":"13664321999","User3":"13664321000", "User4":"13664322000", "User":"13500044444","MUser1":"13798765888","MUser2":"13898765999","Password":"123456","ResourceMobile1":"13798765123","ResourceMobile2":"13809090909","ResourceMobile3":"13798765100","ResourceMobile4":"13798765101","ResourceMobile5":"13798765102","ResourceMobile6":"13798765103","ResourceMobile7":"13798765104","ResourceMobile8":"13798765105","ResourceMobile9":"13798765106","ResourceMobile10":"13798765107","ResourceMobile11":"13798765108","ResourceMobile12":"13798765109","ResourceMobile13":"13798765110","ResourceMobile14":"13798765111","ResourceMobile15":"13798765112","ResourceMobile16":"13798765113","TUser1":"13510101010","TUser2":"13510101011","TUser3":"13510101012","TUser4":"13510101013","GUser":"13800000000","BUser1":"13794491000","BUser2":"13794491001","BUser3":"13794491002", "BUser4":"13794491003", "BUser":"13794491004","BMUser1":"13794492000","BMUser2":"13794492001","BResourceMobile1":"13794493000","BResourceMobile2":"13794493001","BResourceMobile3":"13794493002","BResourceMobile4":"13794493003","BResourceMobile5":"13794493004","BResourceMobile6":"13794493005","BResourceMobile7":"13794493006","BResourceMobile8":"13794493007","BResourceMobile9":"13794493008","BResourceMobile10":"13794493009","BResourceMobile11":"13794493010","BResourceMobile12":"13794493011","BResourceMobile13":"13794493012","BResourceMobile14":"13794493013","BResourceMobile15":"13794493014","BResourceMobile16":"13794493015","BTUser1":"13794494000","BTUser2":"13794494001","BTUser3":"13794494002","BTUser4":"13794494003","BGUser":"13794495000"}

ROOT_DIR =  os.path.dirname(__file__)
#folder = os.environ.get('CASE_FOLDER', "M7/client")
#folder = os.environ.get('CASE_FOLDER', "M7/merchant")
#folder = os.environ.get('CASE_FOLDER', "April/client")
#CASE_FOLDERS = os.environ.get('CASE_FOLDER',"April/client,April/merchant")
CASE_FOLDERS = os.environ.get('CASE_FOLDER',"April_Add/client")
#CASE_FOLDERS = os.environ.get('CASE_FOLDER',"M7/client,M7/merchant")
folders=CASE_FOLDERS.split(",")
SUITE_DIRS=[]
for folder in folders:
    if "Windows" in platform.platform():
        SUITE_DIRS.append(os.path.join(ROOT_DIR, folder))



sleepTime = int(os.environ.get('SLEEP_TIME', 0))

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

def parseCaseList():
    caseList = []
    numList=[]
    num=0
    for SUITE_DIR in SUITE_DIRS:
        for root, dirs, files in os.walk(SUITE_DIR):
            for each in dirs:
                if "Windows" in platform.platform():
                    caseList.append(each.encode('gb18030'))
                else:
                    caseList.append(each)
                #         print "The testcase list: "
                #         print caseList
                numList.append(num)
        num=num+1
    return caseList,numList

def seperateCaseStep(case,num):
    SUITE_DIR= SUITE_DIRS[num]
    for root ,dirs, files in os.walk(os.path.join(SUITE_DIR,case)):
         stepList = []
         for each in files:
             each = os.path.join(os.path.join(SUITE_DIR,case),each)
             stepList.append(each)
#         print "The Case steps: "
#         print stepList
    return stepList


def getValueByKey(Context,jdict,param):
    if type(jdict).__name__ == "int":
        print "The response value is type int."
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
    #else:
        #Context.selectableList.append(param)

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
        conn = pymysql.connect(host=host,user=user,passwd=psw,db=dbname)
        cur = conn.cursor()
        sql = sql.replace("\\","")
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

def notInValidator(params, value):
    mark = 0;
    for i in xrange(len(value)):
        if params != value[i]:
            mark =+ 1
    if mark == len(value):
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


def orValidator( params, value):
    if params == value:
        return True
    else:
        return False

def inRangeValidate(params, value):
#     print  type(params)
#     print params
#     print value
    if params in value:
        return True
    else:
        return False

def selectableValidate(params, value):
    if params not in value:
        return True
    else:
        return False


def greaterValidate(params, value):
    if params >= value:
        return True
    else:
        return False

def regValidate(params,value):
    try:
        val = re.findall(value,params)
        if val:
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
    if typo == "||":
        val.register("||", equalValidator(params, value))
    if typo == "in":
        val.register("in", inRangeValidate(params, value))
    if typo == "?":
        val.register("?", selectableValidate(params, value))
    if typo == ">=":
        val.register(">=", greaterValidate(params, value))
    if typo == "reg":
        val.register(">=", regValidate(params, value))
    if typo == "values":
        val.register("values", valuesValidator(params, value))
    if typo == "notIn":
        val.register("notIn", notInValidator(params, value))
    if typo == "typeIn":
        val.register("typeIn", typeInValidator(params, value))

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
            t = Template(raw_json_str.decode("utf-8"))
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
                    print context.lastReponse
                    context.allResponses.append(context.lastReponse)
                elif "UPDATE" in d["request"]["params"]:
                    print d["request"]["params"]
                    context.lastReponse = result
                    context.allResponses.append(context.lastReponse)
                elif "INSERT" in d["request"]["params"]:
                    print d["request"]["params"]
                    context.lastReponse = result
                    context.allResponses.append(context.lastReponse)
                elif "DELETE" in d["request"]["params"]:
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
                #print context.lastReponse
                context.allResponses.append(context.lastReponse)

                #return json_resp, d
            except jsonrpclib.jsonrpc.ProtocolError, e:
                error_info = e.args[0]
                print u"ProtocolError: {}, Message: {}".format(error_info[0], error_info[1])
        #         return  e
                context.error = "{}".format(error_info[0])
                context.lastReponse="ERROR"
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
                                    # print valueEx,params
                                    if params is None:
                                        print "The return value of %s is null."%newPara
                                        flag = True
                                    elif checker(newPara,typo, params,valueEx):
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




# getValueByKey(Context,jdict,"content")
# print value
# value = list(set(value))
# print value
#             
# def main():
#     caseLists = parseCaseList()   
#     stepList = seperateCaseStep(caseLists[0])
#     context = Context()
#     runCase(context, stepList)

caseLists,numLists = parseCaseList()
#stepList = seperateCaseStep(caseLists[0])
allStepList = []
for i in xrange(len(caseLists)):
    allStepList.append(seperateCaseStep(caseLists[i],numLists[i]))



class UnitTest(unittest.TestCase):
    restoreDB("%s/restore.sql" % os.path.dirname(os.path.abspath(__file__)))
    def setUp(self):
        unittest.TestCase.setUp(self)
        #backupDB("%s/backup.sql" % os.path.dirname(os.path.abspath(__file__)))


    def tearDown(self):
       unittest.TestCase.tearDown(self)
       restoreDB("%s/delete.sql" % os.path.dirname(os.path.abspath(__file__)))

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



def suite():
    arglists = []
    CaseNameLists = caseLists
    #print CaseNameLists
    for i in xrange(len(caseLists)):
        stepList = seperateCaseStep(caseLists[i],numLists[i])
        arglists.append(stepList)
    #print arglists
    item = int(os.environ.get('UT_ITEM', -1))
    print (item)
    print '-' * 60
    if item == -1:
        print 'current test suite is ALL TESTS'
    else:
        print 'current test item is: %d' % item
    print '-' * 60

    if item == -1:
        for i in xrange(len(arglists)):
            test_func = "test_" + CaseNameLists[i]
            setattr(UnitTest, test_func,
                UnitTest.getTestFunc(arglists[i]))
    else:
        item=item-1
        test_func = "test_" + CaseNameLists[item]
        setattr(UnitTest, test_func,
            UnitTest.getTestFunc(arglists[item]))
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(UnitTest))
    return suite

if __name__ == "__main__":
    # unittest.main()
   # restoreDB("%s/backup.sql" % os.path.dirname(os.path.abspath(__file__)))
   a="INSERT INTO `transaction` (`id`, `user_id`, `amount`, `type`, `create_time`, `remark`, `subject`, `tid`, `category`) VALUES(2,6,20,1,DATE_SUB(NOW(),INTERVAL 3 DAY),\\'发布信息\\',2,2,2)"
   print a
   a=a.replace("\\","")
   print a
   #print execSql("INSERT INTO `transaction` (`id`, `user_id`, `amount`, `type`, `create_time`, `remark`, `subject`, `tid`, `category`) VALUES(1,6,10,1,DATE_SUB(NOW(),INTERVAL 2 DAY),'小旺推广',1,1,1)")
#     print execSql("SELECT status from service where id = 2")

# main()

