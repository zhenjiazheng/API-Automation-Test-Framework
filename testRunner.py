# -*- coding: utf-8 -*-
'''
Author: Zheng.zhenjia
'''

from unittest import TestSuite
from HTMLTestRunner import HTMLTestRunner as tr
from testReport import TestReport
# from sendEmail import sendEMail
import platform



DASH='__'

def testsuite():
#     moduleNames=build_testsuite()
    if "Windows" in platform.platform():
        moduleNames = ["jsonRPC-Windows"]
    else:
        moduleNames = ["jsonRPCTest"]
    testsuite=TestSuite()

    for module_name in moduleNames:
        #print module_name
        import importlib
        m = importlib.import_module(module_name)
        #modules=map(__import__,moduleNames)
        testsuite.addTest(m.suite())
        #suite.addTest(element(module.suite()))
    return testsuite


def main():
    global report_file, runner, fp, Report_title
#     tolist=cfgValue.mailToList
#    tolist = mailToList = ["zzj@echiele.com","liubaohua@echiele.com","yehaiyuan@echiele.com","xiaowang@echiele.com"]
    #dbOperation().BackupDB("%s/backup.sql" % os.path.dirname(os.path.abspath(__file__)))
    reportTitle = "Report"#cfgValue.M4Report
    report_file = TestReport.generate_report(reportTitle)
    #print 'report_file: ',report_file
    runner = tr()
    fp = file(report_file, 'wb')
    Report_title = reportTitle + DASH + testsuite.__name__
    runner = tr(stream=fp, title=Report_title, description=report_file)
    runner.run(testsuite())
    fp.close()
    #dbOperation().RestoreDB("%s/backup.sql" % os.path.dirname(os.path.abspath(__file__)))
    #send_the_Mail(report_file, tolist)


if __name__ == '__main__':
    main()