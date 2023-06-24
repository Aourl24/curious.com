from django.shortcuts import render
from ask.models import Question,Answer
from django.apps import apps
from django.forms import ModelForm

t = 'freezyTemplate/'

class FreezyAdmin:
    templates = {}
    
    def __init__(self,title):
        self.title = title
        self.models = []
        
    def __str__(self):
        return self.title
        
    def register_model(self,**item):
        print(item)
        for k,v in item.items():
            for i in v:
                model = apps.get_model(k,i)
                objects = model.objects.all()
                self.models.append({'name':model.__name__,'label':model._meta.app_label,'model':model,'objects':objects}) 
        return self.models
   
    #def register_template(self)



def overviewPage(request):
    template = t+'overview.html'
    freezy = FreezyAdmin('Curious')
    models = freezy.register_model(ask=['Question','Answer'],auth=['User','Group'])
    print(models)
    context = dict(models=models)
    return render(request,template,context)
    
def detailviewPage(request,name,label):
    mod = apps.get_model(label,name)
    subject_items = mod.objects.all()
    template = t + 'detail.html'
    context = dict(subject=name,subject_items=subject_items,label=label)
    return render(request,template,context)
    
    
def itemDetail(request,id,label,model):
    mod = apps.get_model(label,model)
    item = mod.objects.get(id=id)
    get_fields = item._meta.get_fields()
    fields = [{'name':i.name,'value':getattr(item,i.name)} for i in get_fields]
    template = t + 'itemdetail.html'
    context = dict(item=item,fields=fields)
    return render(request,template, context)