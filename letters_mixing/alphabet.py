ARMENIAN_TO_RUSSIAN = {
    'LESSON_1': {
        'uppercase': {
            'Т': 'Տ'
        },
        'lowercase': {
            'т': 'տ'
        }
    }
}


class Alphabet:

    source_to_target_mapping = {
        'russian': {
            'armenian': ARMENIAN_TO_RUSSIAN
        }
    }

    def get_source_to_target_letter_dict(self, target_lang: str, source_lang: str = 'russian') -> dict:
        return self.source_to_target_mapping[source_lang][target_lang]
