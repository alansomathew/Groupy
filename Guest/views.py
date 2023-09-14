from django.shortcuts import render,redirect
from .models import *
from Organizer.models import *
from django.contrib import messages

# Create your views here.
def neworg(request):
    if request.method=="POST":
        organiser.objects.create(username=request.POST.get('txtuname'),password=request.POST.get('txtpass'),name=request.POST.get('txtname'),email=request.POST.get('txtemail'))
        return redirect("Guest:login")
    else:
        return render(request,"Guest/Organizer.html")

def home(request):
    return render(request,"Guest/Home.html")

def login(request):
    error="Invalid UserName and Password"
    if request.method=="POST":
        ocount=organiser.objects.filter(username=request.POST.get('email'),password=request.POST.get('pass')).count()
        if ocount>0:
            odata=organiser.objects.get(username=request.POST.get('email'),password=request.POST.get('pass'))
            request.session["oid"]=odata.id 
            return redirect("org:home")
        else:
            return render(request,"Guest/Login.html",{'mess':error})    
    else:
        return render(request,"Guest/Login.html",)    

def participate(request):
    if request.method=="POST":
        try:
            evntdatacount=Event.objects.filter(code=request.POST.get('txtcode'),status=1).count()
            if evntdatacount>0:
                return render(request,"Guest/Event.html",{'mess':1})
            else:
                is_private=request.POST.get('txt_private')
                
                if is_private == 'public':
                    edata=Event.objects.get(code=request.POST.get('txtcode'),status=0)
                    ParticipateUser.objects.create(user=request.POST.get('txtn'),events=edata)
                    ldata=ParticipateUser.objects.filter(user=request.POST.get('txtn')).last()
                    ids=edata.id
                    idm=ldata.id
                    request.session["edata"]=ids
                    request.session["ldata"]=idm
                    return redirect("Guest:interest")
                else:
                    event_code = request.POST.get('txtcode')
                    username = request.POST.get('txtn')
                    private_code = request.POST.get('txttotal')
                    is_private = request.POST.get('txt_private')

                    event = Event.objects.get(code=event_code, status=0,is_private=True)  # Get the event

                    # Check if the event is private
                    if event:
                        # Check if the private code exists for the event
                        private_code_obj = PrivateCodes.objects.filter(event=event, code=private_code).first()
                        if private_code_obj:

                            
                            # Check if a user with the same private code and username already exists
                            user_exists = ParticipateUser.objects.filter(privatecode=private_code, user=username).exists()
                            if user_exists:
                                messages.warning(request, 'You have already registered for this event with the same private code.')
                                userObj=ParticipateUser.objects.get(user=username, events=event, privatecode=private_code)
                                eId=event.id
                                uId=userObj.id
                                request.session["event_id"]=eId
                                request.session["user_id"]=uId
                                return redirect("Guest:change_interest")
                            else:
                                st=private_code_obj.status
                                if st:
                                    messages.warning(request, 'The private code is already used.')
                                    return render(request,"Guest/Event.html",)
                                # Create a new participant
                                else:
                                    ParticipateUser.objects.create(user=username, events=event, privatecode=private_code)
                                    private_code_obj.status=True
                                    private_code_obj.save()
                                    ldata=ParticipateUser.objects.filter(user=username, events=event, privatecode=private_code).last()
                                    ids=event.id
                                    idm=ldata.id
                                    request.session["edata"]=ids
                                    request.session["ldata"]=idm
                                    messages.success(request, 'Registration successful.')
                                    return redirect("Guest:interest")
                        else:
                            messages.error(request, 'Invalid private code for this event.')
                    else:
                        # Event is not private, create a new participant
                        messages.error(request, 'the event is not a private event.')

                    return redirect("Guest:interest")
            
        except Exception as e:
            print(e)
            messages.error(request,"Event code is not Valid please try with a new one")
            return render(request,"Guest/Event.html",)
    else:
        return render(request,"Guest/Event.html")

def interest(request):
    edata=Event.objects.get(id=request.session["edata"])
    gdata=Room.objects.filter(events=edata)
   
    if request.method=="POST":
        pdata=ParticipateUser.objects.get(id=request.session["ldata"])
        pdata.rooms=request.POST.getlist('inte')
        pdata.save()
        return redirect("Guest:participate")
    else:
        return render(request,"Guest/Group.html",{'data':gdata})
    
def change_interest(request):
    edata=Event.objects.get(id=request.session["event_id"])
    gdata=Room.objects.filter(events=edata)
    user_record = ParticipateUser.objects.get(id=request.session["user_id"])
    user_preferences = user_record.rooms 

    context = {
    'data': gdata,
    'user_preferences': user_preferences
}
    if request.method=="POST":
        pdata=ParticipateUser.objects.get(id=request.session["ldata"])
        pdata.rooms=request.POST.getlist('inte')
        pdata.save()
        return redirect("Guest:participate")
    else:
        return render(request,"Guest/change_preference.html",context)

def groups(request):
    ldata=ParticipateUser.objects.get(id=request.session["ldata"])
    #print(ldata)
    if request.GET.get('did')=="yes":
        roomdata=ldata.rooms
        if roomdata=="":
            roomdata=roomdata+str(request.GET.get('cid'))
            ldata.rooms=roomdata
            ldata.save()
            return redirect("Guest:interest")
        else:
            roomdata=roomdata+","+str(request.GET.get('cid'))
            ldata.rooms=roomdata
            ldata.save()
            return redirect("Guest:interest")
        # gp=room.objects.get(id=request.GET.get('cid'))
        # counts=int(gp.capacity)
        # dcount=ParticipateUser.objects.filter(rooms=gp).count()
        # if dcount>counts:
        #     return redirect("Guest:home")
        # else:
        #     ldata.rooms=gp
        #     ldata.save()
        #     return redirect("Guest:interest")
    else:
        return redirect("Guest:interest")