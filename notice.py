from win10toast import ToastNotifier

def show_toast(msg):
    toaster = ToastNotifier()
    toaster.show_toast(msg,
                       msg,threaded=True)