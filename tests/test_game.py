# tests/test_game.py
import unittest
from lab3_client import load_config, button_click, reset_board, computer_move

class TestTicTacToe(unittest.TestCase):
    def test_load_config(self):
        port, baud_rate, timeout = load_config()
        self.assertEqual(port, 'COM5')
        self.assertEqual(baud_rate, 9600)
        self.assertEqual(timeout, 1)

    def test_button_click(self):
        # Перевірте, чи кнопка заблокована після кліку
        # Тут потрібен мокінг, оскільки tkinter важко тестувати без графічного інтерфейсу
        pass

    def test_reset_board(self):
        # Тест на перевірку, чи дійсно дошка скидується
        pass

    def test_computer_move(self):
        # Тест для перевірки ходу комп'ютера
        pass

if __name__ == '__main__':
    unittest.main()
