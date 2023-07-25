from django.shortcuts import render,redirect
from Guest.models import *
from Organizer.models import Room,Event
import networkx as nx
from Organizer.templatetags import custom_filters
from django.shortcuts import get_object_or_404

# Create your views here.
def home(request):
    if 'oid' in request.session:
        orgdata=organiser.objects.get(id=request.session["oid"])
        evendata=Event.objects.filter(org=orgdata)
        return render(request,"Organizer/Home.html",{'data':evendata})
    else:
        return redirect("Guest:login")

def events(request):
    if 'oid' in request.session:
        if request.method=="POST":
            data=organiser.objects.get(id=request.session["oid"])
            Event.objects.create(code=request.POST.get('txtcode'),rooms=request.POST.get('txtn'),org=data)
            counts=int(request.POST.get('txtn'))
            eventid=Event.objects.filter(org=data).last()
            ids=eventid.id
            for i in range(1,counts+1):
                names="Group"+str(i)
                #print(names)
                Room.objects.create(number=names,events=eventid)
            request.session["events"]=ids
            return redirect("org:group")
        else:
            return render(request,"Organizer/Event.html")
    else:
        return redirect("Guest:login")

def group(request):
    eventadta=Event.objects.get(id=request.session["events"])
    roomdata=Room.objects.filter(events=eventadta)
    if request.method=="POST":
        return render(request,"Organizer/Group.html",{'mess':1})
    else:
        return render(request,"Organizer/Group.html",{'room':roomdata})

def capacity(request):
    data=request.GET.get('did')
    cap,gp=data.split(",")
    roomdata=Room.objects.get(id=gp)
    roomdata.capacity=cap
    roomdata.save()
    return redirect("org:group")

def eventview(request,eid):
    data=Event.objects.get(id=eid)
    return render(request,"Organizer/eventview.html",{'data':data})

def editevent(request,eid):
    data=Event.objects.get(id=eid)
    if request.method=="POST":
        data.code=request.POST.get('txtcode')
        data.save()
        return redirect("org:home")
    else:
        return render(request,"Organizer/editevent.html",{'data':data})

def finishevent(request,eid):
    data=Event.objects.get(id=eid)
    data.status=1
    data.save()
    request.session["eid"]=eid
    return redirect("org:algo")

def logout(request):
    del request.session["oid"]
    return redirect("Guest:home")
def allocate_groups(request,did):
    participents={}
    groups = {}
    mylist=[]
    eventdata=Event.objects.get(id=did)
    eventdata=Event.objects.get(id=did)
    pdatacount=participateuser.objects.filter(events=eventdata).count()
    if pdatacount>0:
        pdata=participateuser.objects.filter(events=eventdata)
        roomsdata=Room.objects.filter(events=eventdata)
        for i in roomsdata:
            
            groups[i.number]=i.capacity
        
        for  i in pdata:
            for j in roomsdata:
                if j.number in i.rooms:
                    if j.number in mylist:
                        continue
                    else:
                        mylist.append(j.number)
            participents[i.user]=mylist
        print(mylist)
        #print(groups)
        print(participents)
        B = nx.Graph()
        B.add_nodes_from(participents.keys(), bipartite=0)
        B.add_nodes_from(groups.keys(), bipartite=1)


        for participent_name, participent_groups in participents.items():
            for group_name in participent_groups:
                B.add_edge(participent_name, group_name, weight=1)
        
        matching = nx.bipartite.maximum_matching(B, top_nodes=participents.keys())

        allocations = {}
        for participent_name, group_name in matching.items():
            if group_name not in allocations:
                allocations[group_name] = []
            allocations[group_name].append(participent_name)
        
        for group_name, participents in allocations.items():
        
            print(f" - {participent_name}-{group_name}")
            print()
        
        
        return render(request,"Organizer/ViewPart.html",{'data':allocations,'room':roomsdata})
    else:
        return render(request,"Organizer/ViewPart.html")
    


def algo(request):
    participents={}
    groups = {}
    mylist=[]
    eventdata=Event.objects.get(id=request.session["eid"])
    
    pdatacount=participateuser.objects.filter(events=eventdata).count()
    if pdatacount>0:
        pdata=participateuser.objects.filter(events=eventdata)
        roomsdata=Room.objects.filter(events=eventdata)
        for i in roomsdata:
            
            groups[i.number]=i.capacity
        
        for  i in pdata:
            for j in roomsdata:
                if j.number in i.rooms:
                    if j.number in mylist:
                        continue
                    else:
                        mylist.append(j.number)
            participents[i.user]=mylist
        print(mylist)
        #print(groups)
        print(participents)
        B = nx.Graph()
        B.add_nodes_from(participents.keys(), bipartite=0)
        B.add_nodes_from(groups.keys(), bipartite=1)


        for participent_name, participent_groups in participents.items():
            for group_name in participent_groups:
                B.add_edge(participent_name, group_name, weight=1)
        
        matching = nx.bipartite.maximum_matching(B, top_nodes=participents.keys())

        allocations = {}
        for participent_name, group_name in matching.items():
            if group_name not in allocations:
                allocations[group_name] = []
            allocations[group_name].append(participent_name)
        
        for group_name, participents in allocations.items():
        
            print(f" - {participent_name}-{group_name}")
            print()
        
        
        return render(request,"Organizer/ViewPart.html",{'data':allocations,'room':roomsdata})
    else:
        return render(request,"Organizer/ViewPart.html")
    
    # eventdata=event.objects.get(id=did)
    # roomdata=room.objects.filter(events=eventdata)
    
    # print(groups)
    # return render(request,"Organizer/Home.html")
    
def eventstatus(request,cid):
    eventdata=Event.objects.get(id=cid)
    pdata=participateuser.objects.filter(events=eventdata)
    roomdata=Room.objects.filter(events=eventdata)
    
    return render(request,"Organizer/Status.html",{'data':pdata,'rdata':roomdata})


def allocate_rooms(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    participants = participateuser.objects.filter(events=event)
    rooms = Room.objects.filter(events=event)

    # Create a directed graph
    graph = nx.DiGraph()

    # Add source and sink nodes to the graph
    graph.add_node('source')
    graph.add_node('sink')

    # Add participant nodes and edges from source to participants
    for participant in participants:
        graph.add_node(participant)
        graph.add_edge('source', participant, capacity=1)  # Set capacity to 1 for participant to limit allocation to one room

    # Add room nodes and edges from rooms to sink
    for room1 in rooms:
        graph.add_node(room1)
        graph.add_edge(room1, 'sink', capacity=room1.capacity)

    # Add edges between participants and rooms based on preferences and remaining capacity
    for participant in participants:
        room_preferences_ids = [int(room_id) for room_id in participant.rooms.split(',') if room_id.isdigit()]
        for room_id in room_preferences_ids:
            room2 = get_object_or_404(Room, id=room_id)
            if room2 in rooms and room2.remaining_capacity > 0:
                graph.add_edge(participant, room2, capacity=1)  # Set capacity to 1 to limit allocation to one participant

    # Run Maximum Flow algorithm
    flow_dict = nx.maximum_flow(graph, 'source', 'sink')[1]

    # Process results
    allocated_rooms = {}
    for participant, allocations in flow_dict.items():
        allocated_rooms[participant] = [room for room, flow in allocations.items() if flow > 0]

    # print(allocated_rooms)

    return render(request, "Organizer/allocation.html", {'event': event, 'participants':participants,'allocated_rooms': allocated_rooms})


def manuualy(request,pk):
    if request.method == 'POST':
        participants = participateuser.objects.get(id=pk)
        print(pk)
        print(participants.rooms)
        room=request.POST.get('flexRadioDefault')
        print(room)
        participants.rooms=room
        participants.save()
        return redirect("org:home")
    else:
        return render(request,"Organizer/Status.html",)

