from kivymd.app import MDApp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.lang import Builder


Builder.load_file("calculator/calculator.kv")
 

class CalculatorWidget(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.valid = False

        home_mt1 = self.ids.home_mt1
        away_mt1 = self.ids.away_mt1
        home_mt2 = self.ids.home_mt2
        away_mt2 = self.ids.away_mt2
        home_mt3 = self.ids.home_mt3
        away_mt3 = self.ids.away_mt3
        home_mt4 = self.ids.home_mt4
        away_mt4 = self.ids.away_mt4
        home_mt5 = self.ids.home_mt5
        away_mt5 = self.ids.away_mt5
        self.head_2_head = [
            {'scores': {'home': home_mt1, 'away': away_mt1}},
            {'scores': {'home': home_mt2, 'away': away_mt2}},
            {'scores': {'home': home_mt3, 'away': away_mt3}},
            {'scores': {'home': home_mt4, 'away': away_mt4}},
            {'scores': {'home': home_mt5, 'away': away_mt5}}
        ]

    def next_button(self):
        if self.is_valid():
            self.parent.parent.transition.direction = "left"
            self.parent.parent.current = "alternatives_screen"

    def is_valid(self):
        counter = len(self.head_2_head)
        print('Total loops ', counter)
        for i in range(counter):
            self.head_2_head[i]['scores']['home'].focus = True
            self.valid = self.validate(self.head_2_head[i]['scores']['home'])
            if self.valid:
                self.valid = self.validate(self.head_2_head[i]['scores']['away'])
                if not self.valid:
                    self.set_focus(self.head_2_head[i]['scores']['away'])
            else:
                self.set_focus(self.head_2_head[i]['scores']['home'])
                self.valid = False
        return self.valid

    @staticmethod
    def set_focus(instance):
        instance.focus = True
        instance.color = [1, 0, 0, 1]

    @staticmethod
    def validate(instance):
        if instance.text == "":
            instance.required = True
            instance.helper_mode = "on_error"
            instance.helper_text_mode = "persistent"
            instance.helper_text = "Field required"
            instance.focus = True
            return False
        elif len(instance.text) > 3:
            instance.helper_mode = "on_error"
            instance.helper_text_mode = "persistent"
            instance.helper_text = "Maximum input (3)"
            instance.focus = True
            return False
        else:
            instance.helper_text_mode = "on_focus"
            instance.helper_text = "Enter scores"
            return True


class AlternativesWidget(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        min_alternative = self.ids.min_alternative
        max_alternative = self.ids.max_alternative
        hh1_odds = self.ids.hh1_odds
        hh2_odds = self.ids.hh2_odds
        min_alt_over = self.ids.min_alt_over
        min_alt_under = self.ids.min_alt_under
        max_alt_over = self.ids.max_alt_over
        max_alt_under = self.ids.max_alt_under

        self.alternatives = [
            {'alternative': min_alternative},
            {'alternative': max_alternative}
        ]

        self.odds = [
            {'odds': hh1_odds},
            {'odds': hh2_odds},
            {'odds': min_alt_over},
            {'odds': min_alt_under},
            {'odds': max_alt_over},
            {'odds': max_alt_under}
        ]

    @staticmethod
    def set_focus(instance):
        instance.focus = True
        instance.color = [1, 0, 0, 1]

    def is_valid_alternative(self):
        for i in range(len(self.alternatives)):
            valid = self.validate(self.alternatives[i]['alternative'], maximum=6, text="Enter Alt by Bookies")
            if not valid:
                self.set_focus(self.alternatives[i]['alternative'])
                return False
        return True

    def is_valid_odds(self):
        for i in range(len(self.odds)):
            valid = self.validate(self.odds[i]['odds'])
            if not valid:
                self.set_focus(self.odds[i]['odds'])
                return False
        return True

    @staticmethod
    def validate(instance, maximum=4, text="Enter odds"):
        if instance.text == "":
            instance.required = True
            instance.helper_mode = "on_error"
            instance.helper_text_mode = "persistent"
            instance.helper_text = "Field required"
            return False
        elif len(instance.text) > maximum:
            instance.helper_mode = "on_error"
            instance.helper_text_mode = "persistent"
            instance.helper_text = "Max input {}".format(maximum)
            return False
        else:
            instance.helper_text_mode = "on_focus"
            instance.helper_text = text
            return True

    def back_button(self):
        self.parent.parent.transition.direction = "right"
        self.parent.parent.current = "scores_screen"

    def calculate(self):
        if self.is_valid_alternative() and self.is_valid_odds():
            self.parent.parent.current = "results_screen"


class ResultsWidget(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.results_win = self.ids.results_content_win
        self.calculator = CalculatorWidget()

        mt1_label = Label(text="MT1: " + self.calculator.head_2_head[0]['scores']['home'].text)
        self.results_win.add_widget(mt1_label)
    
    def add_content(self, content):
        self.content_window.clear_widget()
        self.content_window.add_widget(content)

    def home(self):
        # self.clear_all()
        self.parent.parent.direction = "left"
        self.parent.parent.current = "scores_screen"
    
    def clear_all(self):
        pass


class MainCalculatorWindow(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        scores_screen = self.ids.scores_screen
        alternatives_screen = self.ids.alternatives_screen
        results_screen = self.ids.results_screen

        scores_screen.add_widget(CalculatorWidget())
        alternatives_screen.add_widget(AlternativesWidget())
        results_screen.add_widget(ResultsWidget())


class CalculatorApp(MDApp):
    def build(self):
        self.title = "Basket Calculator"
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Teal"

        return MainCalculatorWindow()


if __name__ == '__main__':
    calc = CalculatorApp()
    calc.run()
