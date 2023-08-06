import sys
import argparse

from mecord import utils
from mecord import xy_user
from mecord import mecord_service
from mecord import mecord_widget
from mecord import store

parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
subparsers = parser.add_subparsers()
parser_widget = subparsers.add_parser("deviceid", help="获取当前设备ID")
parser_widget = subparsers.add_parser("widget", help="widget模块")
parser_widget.add_argument("init", type=str, default=None, help="创建widget, 注意: 需要在空目录调用")
parser_widget.add_argument("public", type=str, default=None, help="发布模块")
parser_service = subparsers.add_parser("service", help="service模块")
parser_service.add_argument("start", type=str, default=None, help="start task loop service")

def service():
    if xy_user.User().isLogin() == False:
        print('please login first! \nUsage: mecord deviceid & Use Mecord Application scan it')
        return
    if len(sys.argv) <= 2:
        print('please set command! Usage: mecord service start')
        return

    command = sys.argv[2]
    service = mecord_service.MecordService()
    if command == 'start':
        if service.is_running():
            print('Service is already running.')
        else:
            print('Starting service...')
            service.start()
    elif command == 'stop':
        if not service.is_running():
            print('Service is not running.')
        else:
            print('Stopping service...')
            service.stop()
    elif command == 'restart':
        print('Restarting service...')
        service.restart()
    elif command == 'status':
        if service.is_running():
            print('Service is running.')
        else:
            print('Service is not running.')
    else:
        print("Unknown command:", command)
        print("Usage: python service.py [start|stop|restart|status]")
        
def widget():
    if xy_user.User().isLogin() == False:
        print('please login first! \nUsage: mecord deviceid & Use Mecord Application scan it')
        return
    if len(sys.argv) <= 2:
        print('please set command! Usage: mecord widget [init|publish]')
        return

    command = sys.argv[2] 
    if command == 'init':
        mecord_widget.createWidget()
    elif command == 'publish':
        mecord_widget.publishWidget()
    else:
        print("Unknown command:", command)
        print("Usage: mecord widget [init|publish]")
        
def deviceid():
    xy_user.User().loginIfNeed()
    uuid = utils.generate_unique_id()
    utils.displayQrcode(uuid)
    print("your deviceid is : " + uuid)

module_func = {
    "widget": widget,
    "service": service,
    "deviceid": deviceid,
}

def main():
    module = sys.argv[1]
    if module in module_func:
        module_func[module]()
    else:
        print("Unknown command:", module)
        print("Usage: mecord [login|service|widget]")
        sys.exit(0)
        
if __name__ == '__main__':
    main()
