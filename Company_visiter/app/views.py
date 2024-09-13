from django.shortcuts import render ,redirect
from app.models import Registration_info , Add_new_visiter
from django.contrib import messages
from datetime import datetime ,date, timedelta
from django.core.paginator import Paginator, PageNotAnInteger
from django.contrib.auth import logout 
import re


class RegisterError(Exception):
    pass

#Login View
def Login(request):
    
    if request.method == 'POST':
        
        Username = request.POST.get("uname")
        Upassword = request.POST.get("upass")
        
        try:
            user = Registration_info.objects.get(uname=Username)
            
            if user.upass== Upassword:
                request.session['username'] = user.uname
                messages.success(request,"Login Successfully..!")
                return redirect('dashboard')
            else:
                messages.warning(request, "Invalid password. Please try again.")
                
        except Registration_info.DoesNotExist:
            messages.warning(request, "Username does not exist.")
            
        except Exception as e:
            messages.error(request,str(e))
          
    return render (request,'login.html')


#Registration view
def Register(request):
    
    if request.method == 'POST':
        
        Uname=request.POST.get("uname")
        Uemail=request.POST.get("uemail")
        Upass=request.POST.get("upass")

        pass_length=8
        upass_char_start=r"^[A-Z]"
        upass_char_int=r"^(?=.*[@])(?=.*[0-9])(?=.*[a-zA-Z]).*$" 
        uname_length=6
        uname_only_char=r"^[a-zA-Z]+"
        try:
            if len(Upass) < pass_length:
                raise RegisterError("Password length must be 8 words or more...!")
            
            if not re.match(upass_char_start, Upass):
                raise RegisterError("Password must start with an uppercase character...!")
            
            if not re.match(upass_char_int,Upass):
                raise RegisterError("Password must include characters numbers and ( @ ) special character...!")
            
            if len(Uname) < uname_length:
                raise RegisterError("Username length must be 6 character or more...!")
            
            if not re.match(upass_char_start,Uname):
                raise RegisterError("Username must start with an uppercase character...!")
            
            if not re.match(uname_only_char,Uname):
                raise RegisterError("Username must contain only letters...!")
            
            if Registration_info.objects.filter(uname=Uname).exists():
                raise RegisterError("Username already exists. Please choose another one...!")
            
            if Registration_info.objects.filter(uemail=Uemail).exists():
                raise RegisterError("Email already exists. Please choose another one...!")

            #direct save nhi kraych veriable name gheun save kraych
            reg=Registration_info(uname=Uname,uemail=Uemail,upass=Upass) 
            reg.save()
            messages.success(request,"Registration Successfully")
            return redirect('/')
        
        except Exception as e:
            messages.error(request,str(e))
            
    return render (request,'register.html')

# Forgetpass VCioew
def Forgetpass(request):
    
    if request.method == 'POST':
        
        user_email = request.POST.get('femail')
        new_password = request.POST.get('newpass')
        confirm_password = request.POST.get('cnewpass')
        
        pass_length=8
        upass_char_start=r"^[A-Z]"
        upass_char_int=r"^(?=.*[@])(?=.*[0-9])(?=.*[a-zA-Z]).*$" 
        
        try:
            if new_password!=confirm_password:
                raise RegisterError("Password do not match...!")

            if len(new_password) < pass_length:
                raise RegisterError("Password length must be 8 words or more...!")
            
            if not re.match(upass_char_start, new_password):
                raise RegisterError("Password must start with an uppercase character...!")
            
            if not re.match(upass_char_int,new_password):
                raise RegisterError("Password must include characters numbers and ( @ ) special character...!")
            
            forgetpas = Registration_info.objects.get(uemail=user_email)
            forgetpas.upass=new_password
            forgetpas.save()
            
            messages.success(request,"Password reset successfully...!")
            return redirect('login')
        
        except Registration_info.DoesNotExist:
            messages.warning(request,"Email not found...!")
            
        except Exception as e:
            messages.error(request,str(e))
        
    return render(request,'forgetpass.html')



#Dashboard
def Dashboard(request):
    username = request.session.get('username')
    totalvisitors = Add_new_visiter.objects.all()
        
    #for today visiter
    today = date.today()
    todadyvisitor_count = totalvisitors.filter(date=today).count()
        
    #For yesterday visiter
    yesterday = date.today() - timedelta(days=1)
    yesterdayvisitor_count = totalvisitors.filter(date=yesterday).count()
        
    #For last 7 days
    lastsewvendays = date.today() - timedelta(days=7)
    lastsewvendaysvisitor_count = totalvisitors.filter(date=lastsewvendays).count()
        
    #For total Visiter
    visitors_count = totalvisitors.count()
    visitors_count = str(visitors_count)
            
    param = {
            'username': username,
            'totalvisitors':visitors_count,
            'todayvisitor':todadyvisitor_count,
            'yesterdayvisitor':yesterdayvisitor_count,
            'lastsewvendaysvisitor':lastsewvendaysvisitor_count,
                }
    
    if request.method == 'POST':
        Searchfield = request.POST.get('searchfield')
        
        try:    
            name = Add_new_visiter.objects.filter(fullname__icontains=Searchfield)
            number = Add_new_visiter.objects.filter(phonenum__icontains=Searchfield)
            
            search = name | number
            if search.exists():
                paginater = Paginator(totalvisitors, 8)
                page_number = request.GET.get('page')
                try:
                    page_obj = paginater.get_page(page_number)
                except PageNotAnInteger:
                    page_obj = paginater.page(1)
                    
                para={
                    'visitors':search,
                    'page_obj':page_obj
                }
                return render(request, 'visiablebydate.html',para)
            
            if not search.exists():
                raise RegisterError("Visitor not found...!")
            
        except Exception as e:
            messages.error(request, str(e))
        
    return render(request,'dashboard.html',param)



#new Visiter
def Newvisiter(request):
    
    username = request.session.get('username')
    if request.method == 'POST':
        
        Fullname = request.POST.get('fullname')
        Email = request.POST.get('email')
        Phonenum = request.POST.get('phonenum')
        Address = request.POST.get('address')
        Whomtomeet = request.POST.get('whomtomeet')
        Department = request.POST.get('department')  
        Reasontomeet = request.POST.get('reasontomeet')
        
        phone_pat = r"^[0-9]{10}$"
        
        try:
            if not Fullname and Email and Phonenum and Address and Whomtomeet and Department and Reasontomeet:
                raise RegisterError("All fields are mandatory")
            
            if not re.match(phone_pat, Phonenum):
                raise Exception("Invalid phone number. It should contain exactly 10 digits.")

            #data get krtani for validation hmesha sapertely check kraych
            name=Add_new_visiter.objects.filter(fullname=Fullname).exists() 
            email=Add_new_visiter.objects.filter(email=Email).exists()
            
            if name or email:
                raise RegisterError("Visiter already exists...!")
            
            addvisiter = Add_new_visiter(
            fullname=Fullname, 
            email=Email, 
            phonenum=Phonenum, 
            address=Address, 
            whomtomeet=Whomtomeet, 
            department=Department,  
            reasontomeet=Reasontomeet
            )
            
            addvisiter.save()
            print(addvisiter.date)
            messages.success(request, "Visitor added successfully!")
            return redirect('newvisiter')
        
        except Exception as e:
            messages.error(request,str(e))

    return render(request, 'newvisiter.html',{'username': username,})



#manage visiter table
def Managevisiter(request):
    username = request.session.get('username')
    visitors = None
    if request.method == 'POST':
        Searchfield = request.POST.get('searchfield')
        
        try:
            name = Add_new_visiter.objects.filter(fullname__icontains=Searchfield)
            number = Add_new_visiter.objects.filter(phonenum__icontains=Searchfield)
            
            manage_search = name | number
            if not manage_search:
                raise RegisterError("No data found...!")
            
            visitors=manage_search
            
        except RegisterError as e:
            messages.error(request, str(e))
        except Exception as e:
            messages.error(request, "Something went wrong during the search...!")
        
    if not visitors:
        try:    
            visitors = Add_new_visiter.objects.all()
        except :
            messages.error(request,"Something went wrong...!")
            
    #pagenater
    paginator = Paginator(visitors, 8)
    page_number = request.GET.get('page')
    try:
        page_obj  = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    
    param = {'visitors':page_obj,'username': username}
    return render(request,'managevisiter.html',param)




#visit by date
def Visitbydate(request):
    username = request.session.get('username')
    if request.method == 'POST':

        Frodate_srt =request.POST.get('fromdate')
        Todate_str = request.POST.get('todate')
        
        try:
            Frodate = datetime.strptime(Frodate_srt, '%Y-%m-%d').date()
            Todate = datetime.strptime(Todate_str, '%Y-%m-%d').date()
            
            if Frodate > Todate:
                raise RegisterError("From date cannot be after to date...!")
            
            visitors = Add_new_visiter.objects.filter(date__range=[Frodate,Todate])
            paginater = Paginator(visitors, 8)
            page_number = request.GET.get('page')
            try:
                page_obj = paginater.get_page(page_number)
            except PageNotAnInteger:
                page_obj = paginater.page(1)
                    
            param={
                'visitors': visitors,
                'fromdate':Frodate,
                'todate':Todate,
                'page_obj':page_obj,
                'username': username,
                }
            return render(request, 'visiablebydate.html',param)
        
        except Exception as e:
            messages.error(request, str(e))
        
    return render(request,'visitbydate.html',{'username': username,})




#visiable date
def Visiablebydate(request):
    # username = request.session.get('username')
    return render(request,'visiablebydate.html')



#update visister
def Update_visiter(request,id):
    username = request.session.get('username')
    update = Add_new_visiter.objects.get(id=id)
    if request.method == "POST":
        update.fullname = request.POST.get('fullname')
        update.email = request.POST.get('email')
        update.phonenum = request.POST.get('phonenum')
        update.address = request.POST.get('address')
        update.whomtomeet = request.POST.get('whomtomeet')
        update.department = request.POST.get('department')  
        update.reasontomeet = request.POST.get('reasontomeet')
        update.remark = request.POST.get('remark')
        
        try:
            if not update.remark:
                raise ValueError('Please add a remark.')
            
            update.save()
            messages.success(request,"Visiter update successfully...!")
            return redirect('managevisiter')
        
        except Exception as e:
            messages.error(request, str(e))
    
    para={
        'id': id,
        'fullname':update.fullname,
        'email':update.email,
        'phonenum':update.phonenum,
        'address':update.address,
        'whomtomeet':update.whomtomeet,
        'department':update.department,
        'reasontomeet':update.reasontomeet,
        'remark':update.remark,
        'username': username,
        }
    return render(request,'update_visiter.html',para)



#logout
def Logout(request):
    logout(request)
    messages.success(request,"You have been logged out successfully...!")
    return redirect("login")
    
    
    
#profile admiin
def Profile_admin(request):
    username = request.session.get('username')
    user=None
    try:
        user = Registration_info.objects.get(uname=username)
    except Exception:
        messages.error(request,"Login first...!")
    param={
        'username': username,
        'show': {
            'uname': user.uname if user else '',
            'uemail': user.uemail if user else '',
        }
           }
    return render(request,'profile.html',param)


# new password
def Newpassword(request):
    username = request.session.get('username')
    
    if request.method == 'POST':
        
        curr_pass = request.POST.get('upass')
        new_password = request.POST.get('newpassword')
        confirm_password = request.POST.get('cnewpassword')
        
        pass_length=8
        upass_char_start=r"^[A-Z]"
        upass_char_int=r"^(?=.*[@])(?=.*[0-9])(?=.*[a-zA-Z]).*$" 
        
        try:
            if new_password!=confirm_password:
                raise RegisterError("Password do not match...!")

            if len(new_password) < pass_length:
                raise RegisterError("Password length must be 8 words or more...!")
            
            if not re.match(upass_char_start, new_password):
                raise RegisterError("Password must start with an uppercase character...!")
            
            if not re.match(upass_char_int,new_password):
                raise RegisterError("Password must include characters numbers and ( @ ) special character...!")
            
            forgetpas = Registration_info.objects.get(upass=curr_pass)
            forgetpas.upass=new_password
            forgetpas.save()
            
            messages.success(request,"Password reset successfully...!")
            return redirect('newpassword')
        
        except Registration_info.DoesNotExist:
            messages.warning(request,"Email not found...!")
            
        except Exception as e:
            messages.error(request,str(e))
    
    param={
        'username': username,
           }
    return render(request,'newpassword.html',param)