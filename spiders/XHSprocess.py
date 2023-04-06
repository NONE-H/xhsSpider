
import pyautogui
import pyperclip

import time
from config import recordNumber
from utils import checkMatch


def XHS_browse(cfg,word):
    '''
    小红书进程,依次点击心形,让fiddler代理捕获
    '''
    pyautogui.FAILSAFE = True
    pyautogui.PAUSE = 0.5
    
    #confidence 置信度
    print('正在搜索小红书图标')
    coords = pyautogui.locateOnScreen('./image_folder/icon.png',confidence = 0.8)
    
    if checkMatch(coords):
        print('小红书图标搜索失败')
        print('1. 请检查是否打开微信小红书的图标\n')
        print('2. 请检查是否使用scale同步电脑的缩放,见README\n')
        print('3. 可能由于您导航栏颜色不同导致匹配失败,截图您导航栏中小红书图标替换image_folder文件夹中的icon.png')
        exit(0)
    #获取定位到的图中间点坐标
    x,y=pyautogui.center(coords)
    pyautogui.click(x,y,button='left')
    
    print('正在搜索返回图标')
    return_icon = pyautogui.locateOnScreen('./image_folder/return.png',confidence = 0.8)
    if return_icon!=None:
        print('返回上级页面')
        return_icon_x,return_icon_y=pyautogui.center(return_icon)
        pyautogui.click(return_icon_x,return_icon_y,button='left')

        
    coords = pyautogui.locateOnScreen('./image_folder/search.png',confidence = 0.8)
    if checkMatch(coords):
        print('找不到搜索图标')
        print('1. 请检查是否使用scale同步电脑的缩放,见README\n')
        print(f'2. 请手动截图小红书小程序搜索按钮(./image_folder/search.png)替换./image_folder/search.png')
        exit(0)
    
    nav_x,nav_y=pyautogui.center(coords)
    nav_x +=50
    pyautogui.click(nav_x,nav_y,button='left',clicks=2,interval=0.3)
    pyautogui.hotkey('ctrl','a')
    
    #keyboardInput = findKeyboardInput(word)
    #pyautogui.typewrite(keyboardInput)
    pyperclip.copy(word)
    pyautogui.hotkey('Ctrl','v')
    pyautogui.press('enter')
    
    time.sleep(2)
    coords = pyautogui.locateOnScreen('./image_folder/comprehensive_ranking.png',confidence = 0.6)
    if checkMatch(coords):
        print('找不到"综合排序"图标')
        print('1. 请检查是否使用scale同步电脑的缩放,见README\n')
        print('2. 请手动截图(./image_folder/comprehensive_ranking.png)替换./image_folder/comprehensive_ranking.png')
        exit(0)
    x,y=pyautogui.center(coords)
    pyautogui.click(x,y,button='left')
    time.sleep(0.2)
    coords = pyautogui.locateOnScreen('./image_folder/comprehensive_ranking_select.png',confidence = 0.6)
    if checkMatch(coords):
        print('找不到"(红)综合排序"图标')
        print('1. 请检查是否使用scale同步电脑的缩放,见README\n')
        print('2. 请手动截图(./image_folder/comprehensive_ranking_select.png)替换./image_folder/comprehensive_ranking_select.png')
        exit(0)
    x,y=pyautogui.center(coords)
    pyautogui.click(x,y,button='left')
    
    time.sleep(0.5)
    
    MAX_RESULT = cfg[word]['target']+5
    result_num = cfg[word]['now']
    pointer = cfg[word]['pointer']
    
    return_icon = pyautogui.locateOnScreen('./image_folder/return.png',confidence = 0.8)
    
    if return_icon == None:
        print('locate by home.png as search.png')
        home_icon = pyautogui.locateOnScreen('./image_folder/home.png',confidence = 0.8)
        home_x,home_y = pyautogui.center(home_icon)
        return_icon_x = nav_x
        return_icon_y = home_y
    else:
        return_icon_x,return_icon_y=pyautogui.center(return_icon)
    while(result_num<MAX_RESULT):
        if result_num >= cfg['SAVE_FREQUNCY']*pointer:
            recordNumber(word,result_num,pointer)
            pointer+=1
            
        coords = pyautogui.locateAllOnScreen('./image_folder/like.png',confidence = 0.9)
        roll_distance = 50
        
        x_before = 0
        y_before = 0
        for pos in coords:
            roll_distance = max(int(pos[1])-int(nav_y),roll_distance)
            x,y = pyautogui.center(pos)
            # print(x,y)
            if abs(x_before-x)<10 and abs(y_before-y)<10:
                continue
            x_before = x
            y_before = y
            if y-nav_y<100:  
                # if an item stay too close to the nav 
                # it may belong to an item checked
                continue
            pyautogui.click(x,y,button='left')
            time.sleep(1)
            pyautogui.click(return_icon_x,return_icon_y,button='left')
            result_num+=1
        pyautogui.scroll(-roll_distance)
        time.sleep(0.5)
        
    recordNumber(word,result_num)
        

'''

'''
def XHS_keep_browse(cfg,word):
    
    MAX_RESULT = cfg[word]['target']
    result_num = cfg[word]['now']
    
    if result_num>=MAX_RESULT :
        print('---------------------')
        print(f'{word} 已满足')
        print('---------------------')
        return 1
    
    MAX_RESULT+=5
    pointer = cfg[word]['pointer']
    
    pyautogui.FAILSAFE = True
    pyautogui.PAUSE = 0.5
    
    coords = pyautogui.locateOnScreen('./image_folder/icon.png',confidence = 0.8)
    
    if checkMatch(coords):
        print('小红书图标搜索失败,请检查是否打开微信小红书的图标')
        print('或者截图您导航栏中小红书图标替换image_folder文件夹中的icon.png')
        exit(0)
    #获取定位到的图中间点坐标
    x,y=pyautogui.center(coords)
    pyautogui.click(x,y,button='left')
    
    return_icon = pyautogui.locateOnScreen('./image_folder/return.png',confidence = 0.8)
    return_icon_x,return_icon_y=pyautogui.center(return_icon)
    
    coords = pyautogui.locateOnScreen('./image_folder/search.png',confidence = 0.8)
    if checkMatch(coords):exit(0)
    
    x,nav_y=pyautogui.center(coords)
    
    
    while(result_num<MAX_RESULT):
        if result_num >= cfg['SAVE_FREQUNCY']*pointer:
            recordNumber(word,result_num,pointer)
            pointer+=1
            
        coords = pyautogui.locateAllOnScreen('./image_folder/like.png',confidence = 0.9)
        roll_distance = 50
        
        x_before = 0
        y_before = 0
        for pos in coords:
            roll_distance = max(int(pos[1])-int(nav_y),roll_distance)
            x,y = pyautogui.center(pos)
            # print(x,y)
            if abs(x_before-x)<10 and abs(y_before-y)<10:
                continue
            x_before = x
            y_before = y
            if y-nav_y<100:  
                # if an item stay too close to the nav 
                # it may belong to an item checked
                continue
            pyautogui.click(x,y,button='left')
            time.sleep(1)
            pyautogui.click(return_icon_x,return_icon_y,button='left')
            result_num+=1
        pyautogui.scroll(-roll_distance)
        time.sleep(0.5)
    
    recordNumber(word,result_num)
    return 0
    
    
    
    
    
    
    
    

