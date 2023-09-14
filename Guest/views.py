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
                    # print(is_private)
                    edata=Event.objects.get(code=request.POST.get('txtcode'),status=0)
                    privatecode=request.POST.get('txttotal')
                    userObjC=ParticipateUser.objects.filter(privatecode=privatecode).count()
                    if (userObjC>0 ):
                        userObj=ParticipateUser.objects.get(privatecode=privatecode).count()  
                        eid=edata.id
                        uid=userObj.id
                        request.session["eventId"]=eid
                        request.session["userId"]=uid
                        return redirect("Guest:interest")
                                  
                    else:
                        pObj=PrivateCodes.object.get(event=edata,code=privatecode)
                        if pObj:
                            return render(request,"Guest/Event.html",{'mess':3})
                        pCode=pObj.code
                        ParticipateUser.objects.create(user=request.POST.get('txtn'),events=edata,privatecode=pCode)
                        ldata=ParticipateUser.objects.filter(user=request.POST.get('txtn')).last()
                        ids=edata.id
                        idm=ldata.id
                        request.session["edata"]=ids
                        request.session["ldata"]=idm
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