import os
import time
import random
link_root='https://bigfam.bioinformatics.nl/api/gcf/get_member_links?gcf_id='  #所有的list下载路径所共有的部分
for i in range(29955):  #一共29955个GCF，从GCF_00001到GCF_29955
    count0=5-len(str(i+1))    #要将1转换成00001，看1的长度，计算0的数量.循环i从0开始，所以要+1
    strnumb=count0*str(0)+str(i+1)  #在数字前加若干个0，如 8前面加4个0，18前面加3个0，188前面加2个0
    GCF_number='GCF_'+str(strnumb)  #在序号前面加GCF_，和数据库保持一致
    print(GCF_number)
    GCF_list_file='GCF_list/'+GCF_number+'.txt'
    link=link_root+str(i+200946)  #根据对应关系，生成GCF对应的link.对应关系在OneNote记录中,i=0,GCF_00001,200946
    print(link)
    if os.path.exists(GCF_list_file) == False:  #判断文件是否存在，下过的就不下了
        #os.system('wget %s -O %s' % (link,GCF_list_file))  #用wget下载对应链接的文件
        os.system('powershell curl -o "%s" "%s"' % (GCF_list_file,link))   #BIGFAM国内访问巨慢，需要翻墙，但是服务器不好翻，这是windows的版本
        t=random.randint(1000,3000)*0.001 #设置一个随机的暂停时间，有些网站会把固定间隔的访问视作攻击，同时不暂停的访问容易被拉黑。生成1到3的随机数等待
        print('delay',t,'s\n')
        time.sleep(t)   #等待一定的时间

