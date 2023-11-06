from dataclasses import dataclass
from typing import List
import requests
import prettytable
import json
import re


@dataclass
class Gerund:
    word: str
    translation: str

    @staticmethod
    def from_dict(obj: dict) -> 'Gerund':
        word = str(obj.get("word"))
        translation = str(obj.get("translation"))
        return Gerund(word, translation)


@dataclass
class Conjugation:
    word: str
    translation: str
    pronoun: str
    is_irregular: bool = False

    @staticmethod
    def from_dict(obj: dict) -> 'Conjugation':
        word = str(obj.get("word"))
        translation = str(obj.get("translation"))
        pronoun = str(obj.get("pronoun"))
        is_irregular = bool(obj.get("isIrregular", False))
        return Conjugation(word, translation, pronoun, is_irregular)


@dataclass
class Pronouns:
    yo: Conjugation
    tu: Conjugation
    el_ella_usted: Conjugation
    nosotros: Conjugation
    vosotros: Conjugation
    ellos_ellas_ustedes: Conjugation
    vos: Conjugation

    @staticmethod
    def from_conjugations(conjugations: List[Conjugation]) -> 'Pronouns':
        for conjugation in conjugations:
            match conjugation:
                case Conjugation(pronoun="yo"):
                    yo = conjugation
                case Conjugation(pronoun="tú"):
                    tu = conjugation
                case Conjugation(pronoun="él/ella/Ud."):
                    el_ella_usted = conjugation
                case Conjugation(pronoun="nosotros"):
                    nosotros = conjugation
                case Conjugation(pronoun="vosotros"):
                    vosotros = conjugation
                case Conjugation(pronoun="ellos/ellas/Uds."):
                    ellos_ellas_ustedes = conjugation
                case Conjugation(pronoun="vos"):
                    vos = conjugation
        return Pronouns(yo, tu, el_ella_usted, nosotros, vosotros,
                        ellos_ellas_ustedes, vos)


@dataclass
class Paradigms:
    present_indicative: Pronouns
    preterite_indicative: Pronouns
    imperfect_indicative: Pronouns
    conditional_indicative: Pronouns

    @staticmethod
    def from_dict(obj: dict) -> 'Paradigms':
        present_indicative = Pronouns.from_conjugations(
            [Conjugation.from_dict(o)
             for o in obj.get("presentIndicative")])
        preterite_indicative = Pronouns.from_conjugations(
            [Conjugation.from_dict(o)
             for o in obj.get("preteritIndicative")])
        imperfect_indicative = Pronouns.from_conjugations(
            [Conjugation.from_dict(o)
             for o in obj.get("imperfectIndicative")])
        conditional_indicative = Pronouns.from_conjugations(
            [Conjugation.from_dict(o)
             for o in obj.get("conditionalIndicative")])
        return Paradigms(present_indicative, preterite_indicative,
                         imperfect_indicative, conditional_indicative)


@dataclass
class Verb:
    infinitive: str
    is_reflexive: int
    is_reflexive_variation: bool
    infinitive_translation: str
    past_participle: Gerund
    gerund: Gerund
    paradigms: Paradigms

    @staticmethod
    def from_dict(obj: dict) -> 'Verb':
        infinitive = str(obj.get("infinitive"))
        is_reflexive = int(obj.get("isReflexive"))
        is_reflexive_variation = bool(obj.get("isReflexiveVariation"))
        infinitive_translation = str(obj.get("infinitiveTranslation"))
        past_participle = Gerund.from_dict(obj.get("pastParticiple"))
        gerund = Gerund.from_dict(obj.get("gerund"))
        paradigms = Paradigms.from_dict(obj.get("paradigms"))
        return Verb(infinitive, is_reflexive, is_reflexive_variation,
                    infinitive_translation, past_participle, gerund, paradigms)


class SpanishVerb:

    BASE_URL = "https://www.spanishdict.com"
    CONGUATION_URL = f"{BASE_URL}/conjugate"

    def fetch_conjugation(self, verb: str):
        page = requests.get(f"{self.CONGUATION_URL}/{verb.strip()}").text
        data = re.search(r"window.SD_COMPONENT_DATA?.=.?(.*);", page).group(1)
        parsed = json.loads(data)
        return parsed.get('verb')

    def conjugate(self, verb: str):
        verb: Verb = Verb.from_dict(self.fetch_conjugation(verb))
        self.build_participle_table(verb)
        self.build_conjugation_table("Present Indicative",
                                     verb.paradigms.present_indicative)
        self.build_conjugation_table("Preterite Indicative",
                                     verb.paradigms.preterite_indicative)
        self.build_conjugation_table("Imperfect Indicative",
                                     verb.paradigms.imperfect_indicative)
        self.build_conjugation_table("Conditional Indicative",
                                     verb.paradigms.conditional_indicative)

    def build_participle_table(self, verb: Verb):
        table = prettytable.PrettyTable()
        table.title = "Participles"
        table.field_names = ["Past", "Present"]
        table.add_row([verb.past_participle.word, verb.gerund.word])
        print(table)

    def build_conjugation_table(self, paradigm: str, pronouns: Pronouns):
        table = prettytable.PrettyTable()
        table.title = paradigm
        table.header = False
        table.preserve_internal_border = True
        table.add_row([pronouns.yo.word, pronouns.nosotros.word])
        table.add_row([pronouns.tu.word, pronouns.vosotros.word])
        table.add_row([pronouns.el_ella_usted.word,
                      pronouns.ellos_ellas_ustedes.word])
        print(table)


if __name__ == '__main__':
    from sys import argv
    if len(argv) > 1:
        SpanishVerb().conjugate(argv[1])
    else:
        print(f"Usage: {argv[0]} VERB")
