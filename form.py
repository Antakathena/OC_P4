class Form():
    """
    Définit la classe des formulaires. Rôle : recueillir les infos joueurs et tournament et les ajouter à la db
    On doit pouvoir y ajouter les questions
    Elle doit afficher les questions
    Elle doit vérifier les réponses
    Elle doit enregistrer les réponses (et transformer si nécessaire)

    Attr : les réponses?
    Méthodes : init, add_question, remove_question?, getanswer, transform_into_another_type...,
               save_answers, draw (est ce que ça veut bien dire créer la vue?
    
    Ajouter une classe question :
    Attr : les questions
    Méthode : create list of question ?
    
    """
   
class Form(models.ModelForm):
    class Meta:
        model = UnModelAvecUnUserField
        fields = ('liste', 'avec', 'les', 'champs', 'du', 'formulaire')

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super().save(commit=False)
        # C'est ici, dans save() qu'on récupère l'utilisateur à partir de la request
        instance.user = self.request.user
        if commit:
            instance.save()
        return instance

class FormView(CreateView):   
    form_class = MonSuperForm
    template_name = 'chemin/vers/mon/template' 
    success_url = reverse_lazy('home') 

    def get_form_kwargs(self): 
        kwargs = super().get_form_kwargs() 
        kwargs['request'] = self.request
        return kwargs