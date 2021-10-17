from typing import Callable, List

from OC_P4.models.player import Player


class Field:
    def __init__(self, validate: Callable, convert: Callable, question_view):
        self.validate = validate
        self.convert = convert
        self.answer = None
        self.question_view = question_view

    def ask(self):
        while True:
            self.question_view.draw()
            answer = input()
            if self.validate(answer):
                try:
                    self.answer = self.convert(answer)
                    return self.answer
                except (TypeError, ValueError):
                    pass


class QuestionView:
    def __init__(self, question):
        self.question = question

    def draw(self):
        print(self.question, end="> ")

class Form():
    """
    Définit la classe des formulaires.
    Rôle : recueillir les infos et générer une action retour (u.a poss les ajouter à la db)
    On doit pouvoir y ajouter les questions
    Elle doit afficher les questions
    Elle doit vérifier les réponses
    Elle doit enregistrer les réponses (et transformer si nécessaire)

    Attr : les questions, les réponses (selon l'implémentation du formulaire)
    Méthodes : init, add_question, remove_question?, getanswer, transform_into_another_type...,
               save_answers, draw (est ce que ça veut bien dire créer la vue?

    """
    def __init__(self, fields: List[Field], callback):
        self.fields = fields
        self.callback = callback

    def execute(self):
        for field in self.fields:
            field.ask()
        self.callback(self.fields)


class FormPlayer(Form):
    def __init__(self, callback=Player):
        super().__init__(
                fields=[Field(str.isdigit, int, QuestionView("Age du capitaine"))],
                callback=callback
            )
        

formulaire_ajouter_tournoi = Form(champs=[...])

formulaire_ajouter_joueurs_new = FormPlayer.prendre_exemplaire()
formulaire_ajouter_joueurs_new.draw()
formulaire_ajouter_joueurs_new.executer()
# données stockées dans le formulaire


"""   
def save(self, commit=True):
    # trouver comment sauvegarder à partir des champs remplis
    instance = super().save(commit=False)
    instance.player = self.request.player
    if commit:
        instance.save()
    return instance
"""