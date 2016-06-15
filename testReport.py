import time,os

#from common.testConfig  import *

class TestReport(object):
    '''
    '''
    folder = os.environ.get('CASE_FOLDER', "M0")
    if "/" in folder:
        fl = folder.split("/")
        folder = fl[0]+"_"+fl[1]
    else:
        pass

    def __init__(self):
        pass
        
      
        
    @classmethod
    def generate_report(self,root_dir = None):
        #cfg=getTestConfig('config.txt')
        #project_code=cfg['testconfig']['project_code']
        self.report_conf = self.make_root_dir(root_dir)
        print self.report_conf

        reportfile = self.get_report_file("API_" + self.folder+ "_" + self.get_reportger_timestr())
        report_file_full_name = os.path.join(self.report_conf, reportfile)
        return report_file_full_name

        
        
      
    '''
        filename="./TestReport.html"  
        fp=file(filename,'wb')
        runner = HTMLTestRunner.HTMLTestRunner(stream=fp,title='Report_title',description='Report_description')  
     '''

        
       


    @classmethod
    def make_root_dir(self, root_dir = None):
        self.report_conf = dict(root_run = os.path.dirname(os.path.abspath(__file__)))
#         print self.report_conf
#         print root_dir

        if not root_dir:
#             root_dir = os.path.realpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", 'Report'))
            root_dir = os.path.realpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Report'))

        Report_dir = os.path.realpath(os.path.join(root_dir, self.folder))

        if not os.path.exists(Report_dir):
            os.makedirs(Report_dir)

        self.report_conf = Report_dir

        return self.report_conf


    @classmethod
    def get_reportger_timestr(self):
        return time.strftime("%Y%m%d%H%M")


    @classmethod
    def get_report_format(self):
        reportformat = '%(asctime)s %(levelname)-8s %(message)s'

        return reportformat


    @classmethod
    def get_report_file(self, filename_id):
        reportfile = "%s.html" % (filename_id)

        return reportfile


    @classmethod
    def get_report_filename_linux(self, reportfile_fullname):
        return reportfile_fullname.replace("\\", "/")


      





if __name__ == "__main__":
    
    '''
    '''
    
    report_conf = TestReport.generate_report()
    print report_conf
   

