from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from myapp.models import*
from django.contrib.auth.hashers import make_password,check_password
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

@csrf_exempt
def all_login(request):
     if request.method=="POST":
          print("post recived")
          username=request.POST['username']
          password=request.POST['password']
          print(username)
          print(password)

          data=authenticate(username=username,password=password)
          print(data)

          if data is not None:
               login(request,data)

               if data.is_superuser:
                    return render(request,'admin/dashboard.html')
               try:
                    doc_data=data.doctor
                    if doc_data.status != "Accepted":
                        return render(
                            request,
                            'all_login.html',
                            {'error': 'Your doctor account is not approved by admin.'}
                        )
                    request.session['doc_id']=doc_data.id
                    return render(request,'doctor/dr_dash.html')
               except doctor.DoesNotExist:
                    print("id not found")
               else:
                     return render(request,'all_login.html')
          return render(request,'all_login.html')
                    


     return render(request,'all_login.html')


def dash_view(request):
     return render(request,'admin/dashboard.html')
     



def admin_login(request):
    if request.method == 'POST':
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request, user)
            if user.groups.filter(name="Admin").exists():
                 
                return render(request,'admin/dashboard.html')
            elif user.groups.filter(name="Doctor").exists():
                 return
                 


            else:
                print("login failed")
                return render(request,'admin/login.html')
        else:
             return
    else:            
        return render(request,'admin/login.html')
    print('please enter details')

def admin_dash(request):
     return render(request,'admin/dashboard.html')

def admin_doctor(request):
    data=doctor.objects.all()

    return render(request,'admin/doctors.html',{'data':data})

def doctor_register(request):
   
    if request.method == 'POST':
        name=request.POST['name']
        email=request.POST['email']
        phone=request.POST['phone']
        specialization=request.POST['specialization']
        qualification=request.POST['qualification']
        experience=request.POST['experience']
        password=request.POST['password']
        photo=request.FILES.get('photo')

        obj_user=User.objects.create_user(
             username=email,
             password=password,
             
        )




        obj=doctor()
        


        obj.name=name
        obj.email=email
        obj.phone=phone
        obj.specialization=specialization
        obj. qualification= qualification
        obj.experience=experience
        obj.photo=photo
        obj.user=obj_user
       

        obj.save()
        return render(request,'all_login.html')

    return render(request,'doctor/register.html')

def dr_login(request):
    if request.method == 'POST':
        username=request.POST['username']
        password=request.POST['password']
        try:

            data=authenticate(username=username,password=password)
            if check_password(password,data.password):
               return redirect('myapp/dr_dash')
            else:
                return render(request,'doctor/dr_login.html',{'msg':'invalid password'})

        except doctor.DoesNotExist:
                            return render(request,'doctor/dr_login.html',{'msg':'user id not existed'})
    return render(request,'doctor/dr_login.html')

def dr_dash(request):
    return render(request,'doctor/dr_dash.html')

def dr_schedules(request):
     doc_id=request.session['doc_id']
     if request.method == 'POST':
          
          date=request.POST['date']
          day=request.POST['day']
          from_time=request.POST['from_time']
          to_time=request.POST['to_time']

          obj=dr_schedule()

          obj.doctors_id=doc_id
          obj.date=date
          obj.day=day
          obj.from_time=from_time
          obj.to_time=to_time
          

          obj.save()

          return redirect('/myapp/view_schedule/')
     data=dr_schedule.objects.filter(doctors_id=doc_id)
     return render(request,'doctor/dr_schedule.html',{'data':data})


def vschedule(request,rid):
     data=dr_schedule.objects.filter(doctors_id=rid)
     schedules=[]

     for i in data:
          schedules.append({
               "id":i.id,
                "date":str(i.date),
                "day":i.day,
                "from_time":str(i.from_time),
                "to_time":str(i.to_time,)
          })
     return JsonResponse(schedules,safe=False)

def view_schedule(request):

    doc_id = request.session.get('doc_id')

    if doc_id is None:
        return render(request, 'all_login.html')

    data = dr_schedule.objects.filter(
        doctors_id=doc_id
    )

    return render(
        request,
        'doctor/view_schedule.html',
        {'data': data}
    )


def edit_schedule(request, rid):
    doc_id = request.session.get('doc_id')

    if doc_id is None:
        return render(request, 'all_login.html')

    try:
        obj = dr_schedule.objects.get(
            id=rid,
            doctors_id=doc_id
        )
    except dr_schedule.DoesNotExist:
        return redirect('/myapp/view_schedule/')

    if request.method == 'POST':
        obj.date = request.POST['date']
        obj.day = request.POST['day']
        obj.from_time = request.POST['from_time']
        obj.to_time = request.POST['to_time']

        obj.save()

        return redirect('/myapp/view_schedule/')

    return render(
        request,
        'doctor/edit_schedule.html',
        {'data': obj}
    )

def delete_schedule(request, rid):
    doc_id = request.session.get('doc_id')

    if doc_id is None:
        return render(request, 'all_login.html')

    try:
        obj = dr_schedule.objects.get(
            id=rid,
            doctors_id=doc_id
        )

        obj.delete()

    except dr_schedule.DoesNotExist:
        pass

    return redirect('/myapp/view_schedule/')

@csrf_exempt
def cancel_appointment(request):
    if request.method == "POST":

        appointment_id = request.POST['appointment_id']
        user_id = request.POST['user_id']

        obj = appoinment.objects.get(
            id=appointment_id,
            users_id=user_id
        )

        obj.status = "cancelled"
        obj.save()

        return JsonResponse({
            'status': 'successful',
            'message': 'Appointment cancelled'
        })

    return JsonResponse({
        'status': 'failed',
        'message': 'POST required'
    })


@csrf_exempt
def update_appointment(request):
    if request.method == "POST":

        appointment_id = request.POST['appointment_id']
        date = request.POST['date']
        time = request.POST['time']

        obj = appoinment.objects.get(id=appointment_id)

        obj.date = date
        obj.time = time

        obj.save()

        return JsonResponse({
            'status': 'successful',
            'message': 'Appointment updated successfully'
        })

    return JsonResponse({
        'status': 'failed',
        'message': 'Only POST method allowed'
    })


def dr_fees(request):

    doc_id=request.session['doc_id']
    if request.method == 'POST':
        
        fees=request.POST['fees']

        obj=dr_fee()
        obj.doctors_id=doc_id
        obj.fees=fees

        obj.save()
     
        return redirect('/myapp/dr_fees/')

    data=dr_fee.objects.filter(doctors_id=doc_id)
    return render(request,'doctor/dr_fee.html',{'data':data})

def doctor_appointments(request):

    doc_id = request.session.get('doc_id')

    if doc_id is None:
        return render(request, 'all_login.html')

    data = appoinment.objects.filter(
        schedule__doctors_id=doc_id
    )

    return render(
        request,
        'doctor/dr_appointments.html',
        {'data': data}
    )


def appointment_status(request, rid, status):

    obj = appoinment.objects.get(id=rid)

    obj.status = status
    obj.save()

    return redirect('/myapp/dr_appointments/')


def doctor_ratings(request):

    doc_id = request.session.get('doc_id')

    if doc_id is None:
        return render(request, 'all_login.html')

    data = rating.objects.filter(doctors_id=doc_id)

    return render(
        request,
        'doctor/dr_ratings.html',
        {'data': data}
    )
    
def accept(request,rid):
    res=doctor.objects.get(id=rid)
    res.status="Accepted"
    res.save()
    return redirect('/myapp/doctors/')

def reject(request,rid):
    res=doctor.objects.get(id=rid)
    res.status="Rejected"
    res.save()
    return redirect('/myapp/doctors/')

def view_doctors(request):
     data=doctor.objects.all()

     all_doctors=[]

     for i in data:
          all_doctors.append({
               'id':i.id,
               'name':i.name,
               'email':i.email,
               'phone':i.phone,
               'specialization': i.specialization,
            'qualification': i.qualification,
            'experience': i.experience,
            'photo': i.photo.url if i.photo else '',
          })
     return JsonResponse(all_doctors, safe=False)




def admin_users(request):
    data=user.objects.all()
    return render(request,'admin/users.html',{'data':data})
def user_accept(request,rid):
    res=user.objects.get(id=rid)
    res.status="Accepted"
    res.save()
    return redirect('/myapp/users/')

def user_reject(request,rid):
    res=user.objects.get(id=rid)
    res.status="Rejected"
    res.save()
    return redirect('/myapp/users/')

@csrf_exempt
def users_reg(request):

    if request.method == 'POST':
        name=request.POST['name']
        email=request.POST['email']
        phone=request.POST['phone']
        dob=request.POST['dob']
        gender=request.POST['gender']
        
        password=request.POST['password']
        if User.objects.filter(username=email).exists():
             return JsonResponse({
                  'message':'already registered'
             })
                  
             

        data=User.objects.create_user(
             username=email,
             password=password,
        )

        obj=user()

        obj.name=name
        obj.email=email
        obj.phone=phone
        obj.dob=dob
        obj.gender=gender
        obj.user=data
       

        obj.save()

        return JsonResponse({
             'status':'success',
             'message':'Regisration successful',
             'user_id':obj.id 
        })
    return JsonResponse ({
         'status':"failed",
         'message':'registration unsuccesful'
    })

@csrf_exempt
def users_login(request):
     if request.method == 'POST':

          username=request.POST['email']
          password=request.POST['password']

          data=authenticate(username=username,password=password)
          print("authenticate data:",data)

          if data is not None:
               obj=user.objects.get(user=data)
               print("custom user id:",obj.id)
               return JsonResponse({
                    'status':'successful',
                    'message':'Login Succesful',
                    'user_id':obj.id
               })
     return JsonResponse({
        'status':'failed',
        'message': 'Invalid email or password'
     })



@csrf_exempt
def book_appointment(request):
     if request.method == 'POST':
          user_id = request.POST['user_id']
          schedule_id = request.POST['schedule_id']
          date = request.POST['date']
          time = request.POST['time']

          user_data =user.objects.get(id=user_id)
          schedule_data=dr_schedule.objects.get(id=schedule_id)

          obj=appoinment()

          obj.users=user_data
          obj.schedule=schedule_data
          obj.date=date
          obj.time=time

          obj.save()

          return JsonResponse({
               'status':'successful',
               'message':'appoinment booked'
          })
     return JsonResponse({
          'status':'failed',
          'message':'only post allowed'
     })

@csrf_exempt
def appointment_view(request):
     if request.method == 'POST':
          user_id=request.POST['user_id']

          data=appoinment.objects.filter(users_id=user_id)

          appointments=[]

          for i in data:

               appointments.append({
                    'id':i.id,
                    'doctor_name':i.schedule.doctors.name,
                    'doctor_id':i.schedule.doctors.id,
                    'specialization':i.schedule.doctors.specialization,
                   
                    'date': str(i.date),
                    'time': str(i.time),
                    'status': i.status,
               })
          return  JsonResponse(appointments,safe=False)
     return JsonResponse({
        'status': 'failed',
        'message': 'only post allowed'
    })

@csrf_exempt
def add_rating(request):
     if request.method == 'POST':

          user_id=request.POST['user_id']
          doctor_id=request.POST['doctor_id']
          comment=request.POST['comment']
          ratings=request.POST['rating']
         

          u_data=user.objects.get(id=user_id)
          d_data=doctor.objects.get(id=doctor_id)

          obj=rating()

          obj.users=u_data
          obj.doctors=d_data
          obj.comment=comment
          obj.ratings=ratings
          

          obj.save()

          return JsonResponse({
               "status":"successful",
               "message":"Rating Added Succesfully"
          })
          
     return JsonResponse({
          "status":"failed",
          "message":"failed"
     })

def view_rating(request,rid):
      #if request.method == 'POST':
          d_data=rating.objects.filter(doctors_id=rid)

          l_rating=[]

          for i in d_data:
               l_rating.append({

                    'doctor_name':i.doctors.name,
                    'rating':i.ratings,
                    'comment':i.comment,
                    'user_name':i.users.name

               })

          return JsonResponse(l_rating,safe=False)




     


    
    
@csrf_exempt
def add_complaint(request):

    if request.method == 'POST':

        user_id = request.POST['user_id']
        complaint_text = request.POST['complaint']
        date = request.POST['date']

        user_data = user.objects.get(id=user_id)

        obj = complaint()

        obj.userprofile = user_data
        obj.complaint = complaint_text
        obj.date = date

        obj.save()

        return JsonResponse({
            'status': 'successful',
            'message': 'Complaint Added Successfully'
        })

    return JsonResponse({
        'status': 'failed',
        'message': 'Only POST allowed'
    })


@csrf_exempt
def view_complaints(request):

    if request.method == 'POST':

        user_id = request.POST['user_id']

        data = complaint.objects.filter(userprofile_id=user_id)

        complaints = []

        for i in data:

            complaints.append({
                'id': i.id,
                'date': i.date,
                'complaint': i.complaint,
                'reply': i.reply if i.reply else '',
                'status': i.status
            })

        return JsonResponse(complaints, safe=False)

    return JsonResponse({
        'status': 'failed',
        'message': 'Only POST allowed'
    })

@csrf_exempt
def add_feedback(request):
    if request.method == 'POST':

        user_id = request.POST['user_id']
        feedback_text = request.POST['feedback']
        date = request.POST['date']

        user_data = user.objects.get(id=user_id)

        obj = feedback()
        obj.userprofile = user_data
        obj.feedback = feedback_text
        obj.date = date

        obj.save()

        return JsonResponse({
            'status': 'successful',
            'message': 'Feedback Added Successfully'
        })

    return JsonResponse({
        'status': 'failed',
        'message': 'Only POST allowed'
    })


def admin_complaint(request):
    data=complaint.objects.all()
    return render(request,'admin/complaint.html',{'data':data})

def comp_reply(request,rid):
    res=complaint.objects.get(id=rid)
    if request.method == "POST":
        reply=request.POST['reply']
        res.reply=reply
        res.status="replied"

        res.save()
        return redirect('/myapp/complaint/')
    return render(request,'admin/comp_reply.html',{'data':res})


def admin_reply(request):
    return render(request,'admin/reply.html')

def admin_feedback(request):

    data=feedback.objects.all()
    return render(request,'admin/feedback.html',{'data':data})

def reports(request):

    total_doctors = doctor.objects.count()
    total_users = user.objects.count()
    total_appointments = appoinment.objects.count()
    total_ratings = rating.objects.count()
    total_complaints = complaint.objects.count()
    total_feedback = feedback.objects.count()

    return render(request, 'admin/report.html', {
        'total_doctors': total_doctors,
        'total_users': total_users,
        'total_appointments': total_appointments,
        'total_ratings': total_ratings,
        'total_complaints': total_complaints,
        'total_feedback': total_feedback,
    })
    
def user_logout(request):
    logout(request)
    return redirect('/myapp/login/')