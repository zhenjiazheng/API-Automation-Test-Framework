#coding=UTF-8
'''
Author: Zheng.zhenjia
'''
import codecs
import os
def CaseFind(fo):
    curr_path=os.path.abspath(__file__)
    print curr_path
    cfgfile_dir=os.path.dirname(curr_path)
    print cfgfile_dir
    json = os.path.realpath(os.path.join(cfgfile_dir,fo))
    print json
    return json

def jsonTransfer(fo,string):
    json = CaseFind(fo)
    for root ,dirs, files in os.walk(json):
        for each in files:
            if each.endswith(".json"):
                each = os.path.abspath(os.path.join(root,each))
                fd = codecs.open(each,'r','utf-8')
                lin = fd.read()
                fd.close()
                fd = codecs.open(each,'w','utf-8')
                if string in lin:
                    fd.write(str(lin).replace('"time":""','"month":""'))
                else:
                    fd.write(str(lin))
                fd.close()

            else:
                pass

def jsonString(fo,action):
    json = CaseFind(fo)
    for root ,dirs, files in os.walk(json):
        if len(dirs) > 0:
            print len(dirs)
            for i in xrange(len(dirs)):
                if dirs[i]:
                    if action == 1:
                        if i < 9:
                            os.rename("/Users/zhengandy/Desktop/API/%s/%s"%(fo,dirs[i]), "/Users/zhengandy/Desktop/API/%s/%s"%(fo,("00%d"%(i+1)+dirs[i])))
                        if 9 <= i < 99:
                            os.rename("/Users/zhengandy/Desktop/API/%s/%s"%(fo,dirs[i]), "/Users/zhengandy/Desktop/API/%s/%s"%(fo,("0%d"%(i+1)+dirs[i])))
                        if 99 <= i < 999:
                            os.rename("/Users/zhengandy/Desktop/API/%s/%s"%(fo,dirs[i]), "/Users/zhengandy/Desktop/API/%s/%s"%(fo,("%d"%(i+1)+dirs[i])))
                    if action == 2:
                        # Remove the case number.
                        print "/Users/zhengandy/Desktop/API/%s/%s"%(fo,dirs[i])
                        os.rename("/Users/zhengandy/Desktop/API/%s/%s"%(fo,dirs[i]), "/Users/zhengandy/Desktop/API/%s/%s"%(fo,dirs[i][3:]))

# jsonString("M7",1)｀
# jsonTransfer("Admin(3.1.2)","finance_getBusinessRewardDetail")

jsonString("13 June/client",1)