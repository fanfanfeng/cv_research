from selenium import webdriver
import time
import pyautogui as pag
# 导入支持双击操作的模块
from selenium.webdriver import ActionChains
from PIL import Image
import pymysql
import os
import urllib.request


voiceDb = pymysql.connect(host="139.199.196.148",
                              user="root",
                              password="dota.123",
                              db="tvpai_new",
                              charset="utf8"
                              )

def load_img(starImage_url,local_star):
    response = urllib.request.urlopen(starImage_url)
    img = response.read()
    with open(local_star, 'wb') as f:
        f.write(img)
    f.close()

def othercatchImg(otherRoot):
    spiderCur = voiceDb.cursor()
    sql_count = "select image from short_video_url LIMIT 1000  "
    spiderCur.execute(sql_count)
    result = spiderCur.fetchall()
    for index,i in enumerate(result):
        starImage_url = i[0].replace('.jpg','_480_270.jpg')
        local_star_path=os.path.join(otherRoot,str(index)+'.png')
        load_img(starImage_url, local_star_path)





def footBallcatchImg(urlList):
    chromedriver = r"D:\工具\chromedriver.exe"

    index=1
    browser = webdriver.Chrome(chromedriver)
    browser.maximize_window()  # 设置浏览器大小：全屏
    for i in urlList:
        browser.get(i)
        pic_path = r'D:\work\captureImg/videos/'
        # browser.quit()


        ##827,237

        #
        # 开始模拟鼠标双击操作
        # #定位到要双击的元素
        # qqq =browser.find_element_by_id("tenvideo_player")
        # #对定位到的元素执行鼠标双击操作
        # ActionChains(browser).double_click(qqq).perform()




        time.sleep(15)
        # pag.click(1227, 337, clicks=1, button='left')
        # time.sleep(1)
        # pag.click(1227, 337, clicks=2, button='left')

        # eleClick=browser.find_element_by_id('tenvideo_player')
        # eleClick.click()
        # action_chains = ActionChains(browser)
        # action_chains.double_click(eleClick).perform()
        try:
            for i in range(300):
                time.sleep(0.5)
                img_path = pic_path + '\\' + str(index) + '.png'
                browser.save_screenshot(img_path)
                index=index+1
        except Exception as e:
            print(e)
            browser.quit()
    browser.quit()




def catchImg(urlList):
    chromedriver = r"D:\工具\chromedriver.exe"

    # 创建chrome参数对象
    # opt = webdriver.ChromeOptions()

    # 把chrome设置成无界面模式，不论windows还是linux都可以，自动适配对应参数
    # opt.set_headless()
    # opt.add_argument('window-size=1920x1080') #指定浏览器分辨率
    # opt.add_argument('--hide-scrollbars') #隐藏滚动条, 应对一些特殊页面
    #
    # # 创建chrome无界面对象
    # browser = webdriver.Chrome(chromedriver, options=opt)
    index=1
    browser = webdriver.Chrome(chromedriver)
    browser.maximize_window()  # 设置浏览器大小：全屏
    for i in urlList:
        browser.get(i)
        pic_path = r'D:\work\captureImg/frames5/'
        # browser.quit()


        ##827,237

        #
        # 开始模拟鼠标双击操作
        # #定位到要双击的元素
        # qqq =browser.find_element_by_id("tenvideo_player")
        # #对定位到的元素执行鼠标双击操作
        # ActionChains(browser).double_click(qqq).perform()




        time.sleep(30)
        # pag.click(1227, 337, clicks=1, button='left')
        # time.sleep(1)
        pag.click(1227, 337, clicks=2, button='left')

        # eleClick=browser.find_element_by_id('tenvideo_player')
        # eleClick.click()
        # action_chains = ActionChains(browser)
        # action_chains.double_click(eleClick).perform()
        try:
            for i in range(320):
                time.sleep(2)
                img_path = pic_path + '\\' + str(index) + '.png'
                browser.save_screenshot(img_path)
                index=index+1
        except Exception as e:
            print(e)
            browser.quit()
    browser.quit()


def mkdir(path):
    # 去除首位空格
    path = path.strip()
    # 去除尾部 \ 符号
    path = path.rstrip("\\")
    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists = os.path.exists(path)
    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(path)
        print("jian")
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print("no jian")
        return False

def reNameFile(path):


    # 获取该目录下所有文件，存入列表中
    f = os.listdir(path)

    n = 0
    for i in f:
        # 设置旧文件名（就是路径+文件名）
        oldname = path + f[n]

        # 设置新文件名
        newname = path + 'footBall_' + str(n + 1) + '.png'

        # 用os模块中的rename方法对文件改名
        os.rename(oldname, newname)
        print(oldname, '======>', newname)

        n += 1

import cv2
def changeImageSize(imageRoot,resultRoot,reWidth,reHeight):

    allList=[]
    for root, dirs, filenames in os.walk(imageRoot, topdown=True):
        if dirs!=[]:
            for i_dir in dirs:
                item={}
                total_files = []
                item['category']=i_dir
                for root1, dirs1, filenames1 in os.walk(os.path.join(imageRoot,i_dir), topdown=True):
                    if filenames1 != []:
                        total_files.extend(filenames1)
                        item['files']=total_files
                        allList.append(item)
    resultPicRoot=os.path.join(resultRoot,str(reWidth)+'X'+str(reHeight))
    mkdir(resultPicRoot)
    if allList!=[]:
        for i_aList in allList:
            picPath=os.path.join(imageRoot,i_aList['category'])
            picList=i_aList['files']
            resultPicPath = os.path.join(resultPicRoot, i_aList['category'])
            mkdir(resultPicPath)
            for i_file in picList:
                if 'png' in i_file :
                    localPath_img=os.path.join(picPath,i_file)

                    # img = cv2.imread(localPath_img)
                    # print(i_file.replace(".png", ".jpg"))
                    img = Image.open(localPath_img)
                    width1, height1 = img.size
                    # 剪裁背景图片
                    cropedIm = img.crop((62, 33, width1 - 62, height1 - 33))
                    # cropedIm.show()

                    width2, height2 = cropedIm.size

                    # 缩小图片比例
                    new_img = cropedIm.resize((reWidth, int(height2 / (width2 / reWidth))), Image.ANTIALIAS)
                    width4, height4 = new_img.size
                    new_img = new_img.convert("RGB")
                    new_img.save(os.path.join(resultPicPath, i_file.replace('png', 'jpg')))



                    # img = Image.open(localPath_img)
                    # width1, height1 = img.size
                    # # 剪裁背景图片
                    # cropedIm = img.crop((62, 33,width1-62, height1-33))
                    # # cropedIm.show()
                    #
                    # width2, height2 =cropedIm.size
                    #
                    #
                    # # 缩小图片比例
                    # new_img = cropedIm.resize((reWidth, int(height2/(width2/reWidth))), Image.ANTIALIAS)
                    # width4, height4 = new_img.size


                    ##################     白色背景    #######################################
                    # white = Image.new('RGBA', (reWidth, reHeight), (0, 0, 0, 0))
                    # # new_img = Image.open(r'D:\work\captureImg\frames5\test.png')
                    # new_img = new_img.convert("RGBA")
                    # white.paste(new_img, (int((reWidth - width4) / 2), int((reHeight - height4) / 2)))
                    # # white.show()
                    # white.save(os.path.join(resultPicPath,i_file))

                    # new_img.save(os.path.join(resultPicPath,i_file.replace('png','jpg')))





if __name__ == '__main__':
    # urlList=['https://v.qq.com/x/cover/qs70opp8uzqhkmm/y0029rvharn.html','https://v.qq.com/x/cover/d34zg8fy8c4n3y8/a0029kgikxs.html',
    #          'https://v.qq.com/x/cover/vj3qcbwptczvxtq/a00290dibaa.html','https://v.qq.com/x/cover/skdciaks145rldk/s0029ko14uc.html',
    #          'https://v.qq.com/x/cover/rntrak447u2bkwj/i0029dv26x2.html','https://v.qq.com/x/cover/ypzjxvlbzv664fy/t0029pv2xmq.html',
    #          'https://v.qq.com/x/cover/15ntzpa1wxsn1av/r0029uc8z6k.html','https://v.qq.com/x/cover/a72r9c4a14m1is2/f0029amhddv.html',
    #          'https://v.qq.com/x/cover/6eyi1civhzus4jq/z0029yfanzt.html','https://v.qq.com/x/cover/h2p9xvd9epx3j17/u0029qdptns.html',
    #          'https://v.qq.com/x/cover/p1ff8ig4ineoq3u/g0029kmtjik.html','https://v.qq.com/x/cover/irt54ue66utdhmu/n00293aprn8.html'
    #     ]
    # catchImg(urlList)


    #足球采集照片
    # footBallcatchImg(['https://sports.qq.com/video/yc/'])

    #其他类型图片采集
    # otherRoot=r'D:\work\captureImg\other'
    # othercatchImg(otherRoot)

    #采集影视图片
    # footBallcatchImg(['https://v.qq.com/x/cover/vb1t9npga3tha8d.html','https://v.qq.com/x/cover/sg5p4qp1s6jbyj8.html',
    #                   'https://v.qq.com/x/cover/rzpyce9pmxayzvb.html','https://v.qq.com/x/cover/h188mdjtrh3up22.html'])


    # reNameFile(r'D:\work\captureImg\frames5\\')

    imageRoot=r'D:\work\captureImg'
    resultRoot=r'D:\work\treatImg'
    changeImageSize(imageRoot,resultRoot,500,500)
