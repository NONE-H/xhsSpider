
from config import initialConfig, readConfigFile, resetConfig, writeConfigFile
from XHSprocess import XHS_browse, XHS_keep_browse
import argparse

from fiddler_process import fiddlerClean, fiddlerSaveData
from selenium_process import getXHScontent
from utils import PictureResize, leftClick, saveArticles,saveToSql


def main(args):
      
    key_word = args.key_word

    if args.reset:
        resetConfig(args,key_word)
        print('配置文件已重置')
        return 
    
    data = readConfigFile()
    if args.scale != 100:
        data['SCREEN_SCALING'] = args.scale
        print('changing image scale...')
        PictureResize(100,args.scale)
        writeConfigFile(data)
        return 
    
    if args.file_explain:
        print('直接进行解析')
        for word in key_word:
            articles = getXHScontent(word)
            saveArticles(word,articles)
        return
    
    initialConfig(args,key_word)
    cfg = readConfigFile()

    if args.keep:
        for word in key_word:
            if XHS_keep_browse(cfg,word)==0:
                print(f'小红书数据采集完成{word}')
                fiddlerSaveData(word)
                print(f'fiddler数据导出完成')
                fiddlerClean()
                print(f'fiddler数据清理完毕')
                # 返回代码编辑器,以便程序输出信息查看
                # 如果不是vscode,请截取你的底部导航栏的代码编辑器(如pycharm)的截图,并替换(./image_folder/codeIDE.png)
                leftClick('./image_folder/codeIDE.png')
                # articles = getXHScontent(word)
                # saveArticles(word,articles)
    
    for word in key_word:
        print(1)
        XHS_browse(cfg,word)
        print(f'小红书数据采集完成{word}')
        fiddlerSaveData(word)
        print(f'fiddler数据导出完成')
        try:
            fiddlerClean()
        except:
            print(f'对于该文件: {word}_fiddler.txt')
            print(f'您可将它移动到/data文件夹下,执行如下命令以单独解析此文件')
            print(f'\n python main.py {word} -f \n')
            print(f'fiddler数据清理完毕')
            exit(0)
        # articles = getXHScontent(word)
        # saveArticles(word,articles)
        
    print('All jobs have been finished!')
    
    
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    # 中断之后继续执行
    parser.add_argument("--keep",action='store_true')
    # 按当前关键字参数重置配置文件信息，配置信息初始化,不会执行程序
    parser.add_argument('--reset',action='store_true')
    # 关键字 | 多参数
    parser.add_argument('key_word',  metavar='N', type=str, nargs='*')
    # 采集数量
    # 微信小程序小红书最大100,请勿调大，可以调小
    parser.add_argument('--target',default=100,type=int)
    # 配置文件位置 | 程序会主动检查,如需重置内容可使用--reset指令
    parser.add_argument('--scale',default=100,type=int)
    # 单独执行fiddler文件解析
    parser.add_argument('--file-explain','-f',action='store_true')
    args = parser.parse_args()

    # 小红书小程序点击获取id
    # main(args)

    # selenium 爬取网页
    articles = getXHScontent(args.key_word[0])

    # 导入mysql
    saveToSql(args.key_word[0])


    # saveArticles(word, articles)