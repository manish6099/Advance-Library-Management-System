import splash_window as sw
import login_window as lw

if __name__ == '__main__':

    splash_obj = sw.SplashScreen()
    login_obj = lw.LoginWindow()

    splash_obj.create_splash_window()
    login_obj.create_login_window()

