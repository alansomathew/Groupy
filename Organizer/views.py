from django.shortcuts import render,redirect,HttpResponse
from django.urls import reverse
from urllib.parse import urlencode
from Guest.models import *
from Organizer.models import Room,Event
import networkx as nx
from Organizer.templatetags import custom_filters
from django.shortcuts import get_object_or_404
import numpy as np
from scipy.optimize import linear_sum_assignment
from django.contrib import messages
from ast import literal_eval
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

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
            try:
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
            except Exception as e:
                    # print(e)
                messages.error(request, 'Event ID is Repeating Please Try again!')
                return render(request,"Organizer/Event.html")
            
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
    # params = urlencode({'event_id': eid})
    # url = reverse('org:check_and_reassign_rooms') + f'?{params}'
    # return redirect(url)
    return redirect(reverse('org:check_and_reassign_rooms', kwargs={'event_id': eid}))

def deleteevent(request,eid):
    data=Event.objects.get(id=eid)
    data.delete()
    return redirect('org:home')

def reopenevent(request,eid):
    data=Event.objects.get(id=eid)
    data.status=0
    data.save()
    return redirect('org:home')


def logout(request):
    del request.session["oid"]
    return redirect("Guest:home")

def allocate_groups(request,did):
    participents={}
    groups = {}
    mylist=[]
    eventdata=Event.objects.get(id=did)
    eventdata=Event.objects.get(id=did)
    pdatacount=ParticipateUser.objects.filter(events=eventdata).count()
    if pdatacount>0:
        pdata=ParticipateUser.objects.filter(events=eventdata)
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
    
    pdatacount=ParticipateUser.objects.filter(events=eventdata).count()
    if pdatacount>0:
        pdata=ParticipateUser.objects.filter(events=eventdata)
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
    try:    
        eventdata=Event.objects.get(id=cid)
        pdata=ParticipateUser.objects.filter(events=eventdata)
        roomdata=Room.objects.filter(events=eventdata)
        
        return render(request, "Organizer/Status.html", {'data': pdata, 'rdata': roomdata,})

    except Exception as e:
        messages.error(request, 'No user is registered for this event!')
        return render(request, "Organizer/Status.html",{'rdata':roomdata})



def allocate_rooms(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    participants = ParticipateUser.objects.filter(events=event)
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

def assign_participants_to_rooms(event):
    # Create a matrix to represent the capacities of the rooms
    capacities = [room.capacity for room in event.room_set.all()]
    capacities_matrix = np.array([capacities])

    # Create a matrix to represent the participant preferences (0 or 1 based on interests)
    participants = event.ParticipateUser_set.all()
    preferences_matrix = np.zeros((len(participants), len(capacities)), dtype=int)
    for i, participant in enumerate(participants):
        rooms_interested = participant.rooms.split(',')
        for j, room in enumerate(event.room_set.all()):
            if str(room.id) in rooms_interested:
                preferences_matrix[i][j] = 1

    # Use the Hungarian algorithm to solve the assignment problem (Max Flow algorithm)
    row_ind, col_ind = linear_sum_assignment(-preferences_matrix * capacities_matrix)
    
    # Update the ParticipateUser model with the assigned rooms
    for i, participant in enumerate(participants):
        if i in row_ind:
            room_index = col_ind[np.where(row_ind == i)][0]
            participant_room = event.room_set.all()[room_index]
            participant.assigned_room = participant_room
            participant.save()
        else:
            participant.assigned_room = None
            participant.save()

def manuualy(request,pk):
    event=Event.objects.get(id=pk)
    participants = ParticipateUser.objects.filter(events=event)
    rooms=Room.objects.filter(events=event)
    print(rooms)
    if request.method == 'POST':
        for participant in participants:
            room_name = request.POST.get('room_' + str(participant.id))
            print(room_name)
            roomObj=Room.objects.get(id=room_name)
            roomNumber=roomObj.number
            print(roomNumber)
            if roomNumber:
                participant.new_rooms = roomNumber
                participant.save()

        # Redirect to a success page or any other appropriate URL after saving the room assignments
        
        return redirect('org:home')
    else:
        return render(request,"Organizer/Manually.html",{'users_data':participants,'room':rooms})


def ajax_manual(request):
    if request.method == "GET":
        selected_value = request.GET.get('selected_value')
        # print(selected_value)
        user_id = request.GET.get('user_id')
        # print(user_id)
        roomObj = get_object_or_404(Room, id=selected_value)
        userObj_f = get_object_or_404(ParticipateUser, id=user_id)
        event_id=roomObj.events
        # eventObj=get_object_or_404(Event, id=event_id)
    
        

        room_number = roomObj.number
        
        
        userObj = get_object_or_404(ParticipateUser, id=user_id)
        
        count=ParticipateUser.objects.filter(events=event_id,new_rooms=room_number).count()

        rooms_list = userObj.rooms.strip('[]').replace("'", "").split(', ')

        if room_number in rooms_list:
            # The room number is present in the list of user rooms
            # Check the capacity of the selected room
            response_data = {
                     'message': 'Success',
                     'selected_value': selected_value,
                    'user_id': user_id
                }
            if roomObj.capacity > count:
                # Room is available and capacity is not full
                response_data = {
                    'message': 'Success',
                    'selected_value': selected_value,
                    'user_id': user_id
                }
            else:
                    # Room is available, but capacity is full
                messages.error(request, f"The selected room  is already full.")
                response_data = {
                    'message': 'Error',
                    'result':"The selected room  is already full.",
                    'selected_value': selected_value,
                    'user_id': user_id
                }
            
        else:
            # The room number is not present in the list of user rooms
            # Get the user name from the user object
            messages.error(request, f"The  room  is not slected by user.")
            response_data = {
                'message': 'Error',
                'result':"The  room  is not slected by user.",
                'selected_value': selected_value,
                'user_id': user_id
            }
       
        userObj_f.new_rooms=room_number
        userObj_f.save()
        return JsonResponse(response_data)




def check_and_reassign_rooms(request,event_id):
    event = Event.objects.get(id=event_id)

    roomdata = Room.objects.filter(events=event)
    try:

        # Call the check_and_reassign_rooms function with the event object
        # Get all the participating users for the event
        participating_users = ParticipateUser.objects.filter(events=event)
        if not participating_users:
            messages.error(request, 'No user is registered for this event!')
            return render(request, "Organizer/allocation.html",{'rdata':roomdata} )

        # Helper function to convert the string representation of rooms to a Python list
        def parse_rooms(rooms_str):
            return literal_eval(rooms_str)

        # Gather room preferences for each user and calculate total capacity required
        room_preferences = {}
        total_capacity_required = 0

        for user in participating_users:
            selected_rooms_str = user.rooms
            selected_rooms = parse_rooms(selected_rooms_str)
            room_preferences[user.user] = selected_rooms
            for room_name in selected_rooms:
                try:
                    room = Room.objects.get(events=event, number=room_name)
                    total_capacity_required += room.capacity
                except Room.DoesNotExist:
                    # Handle the case when a room matching the query does not exist
                    # For example, log the error or take appropriate actions
                    pass

        # Check if total capacity required exceeds the total capacity of all rooms for the event
        total_capacity_available = sum(room.capacity for room in Room.objects.filter(events=event))
        if total_capacity_required <= total_capacity_available:
            # No capacity violations, everything is fine
            return

        # If there is a capacity violation, create a directed graph for the flow network using NetworkX
        G = nx.DiGraph()

        # Add source and sink nodes to the graph
        G.add_node("source")
        G.add_node("sink")

        # Add room nodes and capacities to the graph
        for room in Room.objects.filter(events=event):
            G.add_node(room.number)
            G.add_edge("source", room.number, capacity=room.capacity)

        # Add user nodes and capacities to the graph
        for user in participating_users:
            G.add_node(user.user)
            selected_rooms = room_preferences[user.user]
            for room_name in selected_rooms:
                try:
                    room = Room.objects.get(events=event, number=room_name)
                    G.add_edge(room_name, user.user, capacity=1)
                except Room.DoesNotExist:
                    # Handle the case when a room matching the query does not exist
                    # For example, log the error or take appropriate actions
                    pass

        # Add edges from user nodes to the sink with capacity 1
        for user in participating_users:
            G.add_edge(user.user, "sink", capacity=1)

        # Find the maximum flow using the Edmonds-Karp algorithm (NetworkX implementation)
        max_flow_value, max_flow_dict = nx.maximum_flow(G, "source", "sink")

        # Once the maximum flow algorithm is applied and users are reassigned, update the 'rooms' and 'new_rooms' fields
        ignored_users = set()
        for user in participating_users:
            selected_rooms = room_preferences[user.user]
            new_room_assignment = []
            for room_name in selected_rooms:
                try:
                    room = Room.objects.get(events=event, number=room_name)
                    if max_flow_dict[room_name][user.user] == 1:
                        new_room_assignment.append(room_name)
                except Room.DoesNotExist:
                    # Handle the case when a room matching the query does not exist
                    # For example, log the error or take appropriate actions
                    pass

            if not new_room_assignment:
                ignored_users.add(user.user)
            else:
                user.new_rooms = ",".join(new_room_assignment)
                user.save()

        # Mark the ignored users
        for user in participating_users:
            if user.user in ignored_users:
                user.is_ignored = True
            user.save()

        pdata = ParticipateUser.objects.filter(events=event)
        roomdata = Room.objects.filter(events=event)

        return render(request, "Organizer/allocation.html",{'data':pdata,'rdata':roomdata} )
    except Exception as e:
        print('hello')
        print(e)
        messages.error(request, 'No user is registered for this event!')
        return render(request, "Organizer/allocation.html", )
    
def result(request,pk):
    event = Event.objects.get(id=pk)

    roomdata = Room.objects.filter(events=event)
    try:

        # Call the check_and_reassign_rooms function with the event object
        # Get all the participating users for the event
        participating_users = ParticipateUser.objects.filter(events=event)
        if not participating_users:
            messages.error(request, 'No user is registered for this event!')
            return render(request, "Organizer/allocation.html",{'rdata':roomdata} )

        # Helper function to convert the string representation of rooms to a Python li

        pdata = ParticipateUser.objects.filter(events=event)
        roomdata = Room.objects.filter(events=event)

        return render(request, "Organizer/allocation.html",{'data':pdata,'rdata':roomdata} )
    except Exception as e:
        # print('hello')
        print(e)
        messages.error(request, 'No user is registered for this event!')
        return render(request, "Organizer/allocation.html", )
    