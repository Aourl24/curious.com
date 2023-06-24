from django.shortcuts import render, redirect, reverse
from .models import Question, Answer, Profile,Anon,Image
from .form import QForm, AForm, PForm, UForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
#from django.db import ValueError
from django.contrib.auth.decorators import login_required
from .decorator import decorators
import time
from django.db.models import F
from notifications.signals import notify
from django.shortcuts import get_object_or_404
#from django.http import JsonRsponse
from django.dispatch import receiver
from django.contrib.auth.models import User
#from .models import Profile
from django.db.models.signals import post_save
from django.http import HttpResponse


t = 'askTemplate/'
def fview(request,filter=None):
    tags = [
    {'id':1,'title':'All Question','active':False},
    {'id':2,'title':'Recent Question','active':False},
    {'id':3,'title':'Most Popular','active':False},
    {'id':4,'title':'Most Answer','active':False}
    ]
#Home View, it display the question
    try:
        
        currentUser=Profile.objects.get(user__username=request.user)
        #uquestion=questions.unactive_question(profile=currentUser)
    except ObjectDoesNotExist:
        currentUser=None
      
    if filter == tags[2]['title']:
        questions = Question().most_popular()
        tags[2]['active'] = True
    elif filter == tags[1]['title'] :
        questions = Question().recently_add()
        tags[1]['active'] = True
    elif filter == tags[3]['title']:
        questions = Question().most_answer()
        tags[3]['active'] = True
    else:
        questions = Question.objects.all()
        tags[0]['active'] = True
        
    if request.headers.get('Hx-Request'):
        template = t +'question.html'
    else:
        template = t + 'home.html'
    context=dict(questions=questions,currentUser=currentUser,tags=tags)   
    return render(request, template,context)

# the prefix m-most, u-unactive, n-new questions   


#@login_required(login_url='account_login')
def like2view(request,id):
    error = 'unable to like'
#likeView for hx-requsst
    try:
        currentUser=Profile.objects.get(user__username=request.user)
        question=Question.objects.get(id=id)
        check=Question.objects.filter(id=id, Support=currentUser).exists()
    # checking if user already like the post, if yes we remove the user if no we add the user
        if check:
            Question.objects.get(id=id).Support.remove(currentUser)
            return render(request, t+'like2.html',{'question':question,'currentUser':currentUser})
        else:
            Question.objects.get(id=id).Support.add(currentUser)
    except ObjectDoesNotExist:
        return reverse('HomeUrl')

    return render(request, t+'like2.html',{'question':question,'error':error,'currentUser':currentUser})
                  
    
@login_required(login_url='account_login')
def Qfview(request):
# the Ask Question view
    form=QForm(request.POST)
    if form.is_valid():
        try:
            currentUser=Profile.objects.get(user__username=request.user)
            formBody=form['body'].value()
            title=form['title'].value()
            if title is None:
                l=Question.objects.create(name=currentUser, body=formBody, active=True)
            else:
                l=Question.objects.create(name=currentUser, body=formBody, active=True, title=title)
            img = request.FILES.getlist('images')
            if img:
                for i in img:
                    Image.objects.create(question=l,image=i)
            return redirect('HomeUrl')
        except ObjectDoesNotExist:
            return redirect('/login')
        
    return render(request, t+'create.html', {'form':form})
        
sav=[]
# this sav save the user session key in sview, this is avoid a user having multiple views count at the same time
          
def sview(request, id):
# show the detail view
    tags = [
    {'id':1,'title':'All Answer','active':False},
    {'id':2,'title':'Recent Answers','active':False},
    {'id':3,'title':'Most Popular','active':False},
    ]
    
    try:
        currentUser=Profile.objects.get(user__username=request.user)
    except ObjectDoesNotExist:
        currentUser=None
    
    ses=request.session.session_key
    if ses is None:
#this ses is for Anonymous User and we add the id to recognize the question that have been view
        sesi='Anonymous' + str(id)
    else:
        sesi=ses+str(id)
    question=Question.objects.get(id=id)
    
    if sesi in sav:
        pass
    else:
        question.Views=question.Views + 1
        sav.append(sesi)
#append the sesi to the sav we open outside the request
    question.save()
    answers=Answer.objects.filter(question=question, reply=None, active=True)
        
    template = t +'detail.html'
    answers=Answer.objects.filter(question=question, reply=None, active=True).order_by('-date')
    form=AForm(use_required_attribute=False)
    Recipient=question.name
        
    return render(request, template, {'question':question, 'form':form, 'answers':answers, 'currentUser':currentUser})
 
# j-to get the answer_id value from the detail template 
# co-after getting j, we get the Answer() which id is j 
# g- to get the like button value, but it was meant just to know whether the button is pressed and has nothing to do with the value
# p- same as g but was meant for the dislike button

def filter_answer(request,id,filter):
    tags = [
    {'id':1,'title':'All Answer','active':False},
    {'id':2,'title':'Recent Answers','active':False},
    {'id':3,'title':'Most Popular','active':False},
    ]
    
    question = Question.objects.get(id=id)
    try:
        currentUser=Profile.objects.get(user__username=request.user)
    except ObjectDoesNotExist:
        currentUser=None
        
    answers = Answer.objects.filter(question=question)
    if filter == tag[1]['title']:
        answers = ans.order_by('-date')
    elif filter == tag[2]['title']:
        answers == ans.order_by('like')
    
    template = t + 'answerlist.html'
    context = dict(answers=answers,currentUser=currentUser,question=question)
    return render(request,template,context)
    
@login_required(login_url='account_login')
def likeV(request, id):
    try: 
        currentUser=Profile.objects.get(user__username=request.user)
            #question=Question.objects.get(id=id)
            #answers=Answer.objects.filter(question=question, reply=None, active=True).order_by('-date')
            #answers=Answer.objects.filter(question=question, reply=None, active=True).order_by('-date')
        Recipient=request.GET.get('sender')
        g=request.GET.get('lieb')
        answer=Answer.objects.get(id=id)
    except:
        pass
        #p=request.GET.get('dislike')
    Nuser= get_object_or_404(User, username=Recipient)
        #currentUser=Profile.objects.get(user__username=request.user)
    Manswer=answer.like.filter(id=currentUser.id).exists()
    print(Manswer)          
    if Manswer is True:
            #Banswer=Answer.objects.get(question=question, id=g).like.remove(currentUser)
        answer.like.remove(currentUser)
        answer.save()
        return render(request, t+'like.html',{'currentUser':currentUser,'answer':answer})
    elif Manswer is False:
        answer.like.add(currentUser)
                 #Banswer=Answer.objects.get(question=question, id=g).like.add(currentUser)
        answer.save()
                
        notify.send(request.user, recipient=Nuser, verb='Someone Like Your Answer')
        return render(request,t+'like.html',{'currentUser':currentUser,'answer':answer})
 
    #return render(request, 'like.html',{'question':question,'answer':answer, 'currentUser':currentUser})
 


@login_required(login_url='account_login') 
def pview(request,id):
        profile=Profile.objects.get(user__id=id)
# the user get the request.user through the Profile models

        Quest=Question()
        answer=Answer()
        pquestion=Quest.user_question(profile=profile)
       
# the user_question attribute is used to get the questions of the argument , the argument is user

        panswer=answer.user_answer(profile=profile)
        form=UForm()
        if request.method=='POST':
            form=UForm(request.POST, instance=request.user)
# this form is UserChangeForm that is why it has an instance
            if form.is_valid():
                form.save()       
        #messages.error(request, 'Kindly Login to View your Profile or SignUp to Create your Profile with us')
        #return redirect('/login')
        
    
        return render(request, t+'profile.html',{'pquestion':pquestion, 'panswer':panswer, 'form':form,'profile':profile} )
    
    
def aview(request):
    
    return render(request, t+'about.html')
    
def pendview(request):
    questions=Question()
    user=Profile.objects.get(user__username=request.user)
    uquestions=questions.unactive_question(profile=user)
    
    if request.method=='POST':
        gh=request.POST.get('pend')
        questions.delete_question(int(gh))
        
        
    return render(request, t+'pend.html', {'uquestions':uquestions})
    
def landview(request):
    
    return render(request, t+'landing.html')
    
    
def searchview(request):
    stquestions=None
    if request.method=='POST':
        try:
    
        
            text=request.POST.get('searchtext')
            squestions=Question.objects.filter(title__icontains=text,active=True) | Question.objects.filter(body__icontains=text, active=True)
            
        except ValueError:
            squestions=None
            stquestions=None
                
    else:
        squestions=Question()
        stquestions=Question()
    
    return render (request, t+'search.html', {'squestions':squestions,'stquestions':stquestions})
    
def notificationview(request):
    #noti=Notification.object.unread()
    noti=request.user.notifications.unread()
    noti.mark_all_as_read()
    return render(request, t+'notification.html')

@login_required(login_url='account_login')    
def dark(request):
    if 'dark' in request.GET:
        b=request.GET.get('dark')
        ses=request.session.session_key
        print(ses)
        Mode=Profile.objects.get(user__username=request.user)
        
                #h=request.session.session_key
         
                
          
                
                
             
            
        j=Mode.mode
        if j == 'Light':
            Mode.mode='Dark'
            Mode.save()
            
           
        else:
            Mode.mode='Light'
            Mode.save()
            
      
      
      
    return redirect(b)
            
@login_required(login_url='account_login')
def answerView(request,id,reply=None):
    form = AForm()
    prof = Profile.objects.get(user=request.user)
    question = Question.objects.get(id=id)
    try:
        answer = Answer.objects.get(id=reply)
    except:
        answer = ''
    if request.method== 'POST':
            form=AForm(request.POST)
            if form.is_valid():
                formCheck = form.save(commit=False)
                formCheck.question = question
                formCheck.user = prof
                if reply:
                    answer = Answer.objects.get(id=reply)
                    formCheck.reply = answer
                formCheck.save()
                
                #notify.send(request.user,recipient=Nuser, verb='Someone Answer Your Question')
                
                return redirect(question.get_absolute_url())

    template = t + 'answer.html'
    context = dict(form=form,question=question,answer=answer)
    return render(request,template,context)


def imageView(request,id):
    img = Image.objects.get(id=id)
    context = dict(img=img)
    template = t + 'image.html'
    return render(request,template,context)
    
def answerDetailView(request,id):
    answer = Answer.objects.get(id=id)
    answers = answer.replys.all()
    question = answer.question
    context = dict(answers=answers,question=question)
    template = t + 'answerdetail.html'
    return render (request,template,context)
 
    