from letters_mixing.alphabet import Alphabet


def get_case(letter: str) -> str:
    if letter.islower():
        return 'lowercase'
    else:
        return 'uppercase'


class LettersMixer:

    def __init__(self, target_lang: str, source_lang: str = 'russian', lesson: str = 'LESSON_1',
                 matches_step: int = 2) -> None:

        lesson = lesson.upper().strip().replace(' ', '_')
        target_lang = target_lang.lower().strip().replace(' ', '_')

        letter_dict = Alphabet().get_source_to_target_letter_dict(target_lang, source_lang)

        self._letter_dict = letter_dict[lesson]
        self._matches_step = matches_step
        self._matches_count = 0

    def mix_letters(self, text: str | list, recursion_level: int = 0) -> str:
        new_text = ''
        if isinstance(text, list):
            for line in text:
                new_text += self.mix_letters(line, recursion_level=recursion_level + 1) + ' '
        else:
            for letter in text:
                case = get_case(letter)

                if letter in self._letter_dict[case]:
                    if self._matches_count % self._matches_step == 0:
                        new_text += self._letter_dict[case][letter]
                    else:
                        new_text += letter
                    self._matches_count += 1
                else:
                    new_text += letter

        if recursion_level == 0:
            self._matches_count = 0

        return new_text


if __name__ == '__main__':
    test_text = ['Из под топота копыт пыль по полю летит', 'Во дворе трава, на траве дрова']
    letters_mixer = LettersMixer('armenian')
    print(letters_mixer.mix_letters(test_text))
