import unittest
from src.ZinckLib import morseToChar


class MorseToCharTestCases(unittest.TestCase):

    def test_empty(self):
        result = morseToChar("")
        self.assertEqual(result, -1)

    def test_invalidType(self):
        with self.assertRaises(TypeError):
            morseToChar(1)

    def test_charOnly(self):
        result = morseToChar("abc")
        self.assertEqual(result, -1)

    def test_partialMorse(self):
        result = morseToChar("--.a")
        self.assertEqual(result, -1)
    
    def test_onlyDases(self):
        result = morseToChar("---")
        self.assertEqual(result, "O")
        
    def test_onlyDots(self):
        result = morseToChar("...")
        self.assertEqual(result, "S")

    def test_wrongMorse(self):
        result = morseToChar("...---.")
        self.assertEqual(result, -1)

    def test_normalUsage(self):
        result = morseToChar("-.-.")
        self.assertEqual(result, "C")
    



if __name__ == '__main__':
    unittest.main()
