from typing import Dict


class Locale():
    locale: str = 'zh_CN'
    valid_locales: set = {'zh_CN', 'en'}
    translations: Dict[str, Dict] = {}

    def __init__(self):
        pass

    def add_locale(self, locale_name: str, translations: Dict[str, str]):
        if locale_name not in self.valid_locales:
            raise Exception('invalid locale selection:%s' % locale_name)
        locale_dic = self.translations.get(locale_name)
        if locale_dic is None:
            self.translations[locale_name] = translations
        else:
            for k in translations:
                if locale_dic.get(k) is None:
                    locale_dic[k]=translations[k]

    def translate(self, text: str) -> str:
        if self.locale=='en':
            return text
        locale = self.translations.get(self.locale)
        if locale is not None:
            translation = locale.get(text)
            if translation is not None:
                return translation
        return text

    def _(self, text: str) -> str:
        return self.translate(text)


pmlocale = Locale()
pmlocale.locale = 'zh_CN'
if __name__ == '__main__':
    l = pmlocale
    l.locale = 'zh_CN'
    l.add_locale('en', {'interpreter': 'interpreter'})
    l.add_locale('en', {'console': 'console'})
    l.add_locale('zh_CN', {'console': '控制台'})
    l.add_locale('zh_CN', {'interpreter': '解释器'})
    s = l.translate('interpreter')
    # print(s)
