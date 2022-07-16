from kivymd.app import MDApp
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window

from calculator.calculator import MainCalculatorWindow

Window.size = (310, 580)


class MainWindow(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.calculator = self.ids.calculator_screen

        self.calculator.add_widget(MainCalculatorWindow())


class MainApp(MDApp):
    def build(self):
        self.title = "Basket Calculator"
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Teal"
        return MainWindow()


if __name__ == '__main__':
    calc = MainApp()
    calc.run()
