from controller.timer_controller import TimerController
from view.main_window import MainWindow

if __name__ == "__main__":
    timer_controller = TimerController()
    print(f"TimerController instance: {timer_controller}")  # Debug
    main_window = MainWindow(timer_controller)
    main_window.run()
