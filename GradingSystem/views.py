from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth import get_user_model
# importing the faculties table here
from .models import Faculties
from .models import UsersReview
from .models import Contact
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from . utils import generate_token
from django.core.mail import EmailMessage
from django.conf import settings
from django.views.generic import View
User = get_user_model()


# Create your views here.


def home(request):

    # messages.warning(
    #     request, 'Error please you need to be a student of methodist')
    # messages.success(request, 'Hey Welcome student of Methodist')
    # messages.info(request, 'Hey this is an info message')
    # messages.error(request, 'This is an error message')
    return render(request, 'index.html')


def review(request):

    if request.user.is_authenticated:

        faculties = Faculties.objects.all()

        return render(request, 'review.html', {'faculties': faculties})
    messages.warning(request, 'please login before you can access that page')
    return render(request, 'index.html')


def contact(request):
    if request.method == 'POST':
        contactName = request.POST['name']
        contactEmail = request.POST['email']
        contactSubject = request.POST['subject']
        contactMessage = request.POST['message']
        # print(contactName, contactEmail, contactSubject, contactMessage)
        contactFeedback = Contact.objects.create(
            contactName=contactName, contactEmail=contactEmail, contactSubject=contactSubject, contactMessage=contactMessage)
        contactFeedback.save()
        message = f"Name: {contactName} \n emial : {contactEmail} \n message: {contactMessage}"
        adminEmail = 'alexanderemmanuel1719@gmail.com'

        email_message = EmailMessage(
            contactSubject,
            message,
            settings.EMAIL_HOST_USER,
            [adminEmail],
        )
        if email_message.send():
            messages.info(
                request, 'Thanks, We get back to you as soon as possible')
            return render(request, 'index.html')
        else:
            messages.warning(request, "Please Try Again, Something Went Wrong")

    return render(request, 'contact.html')


def aboutUs(request):
    return render(request, 'about.html')


def createAccount(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        mobile = request.POST['mobile']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            MucgEmail = 'mucg.edu.gh'
            emailCheck = email.split('@')
            if MucgEmail != emailCheck[1].lower():
                messages.warning(
                    request, f'{first_name}, Please Use your school email to register!!')
                return redirect(createAccount)
            # to check if the email already exist
            elif User.objects.filter(email=email).exists():
                messages.warning(
                    request, ' Email already Used, Please Use another Email !!')
                return redirect(createAccount)
            else:
                user = User.objects.create_user(
                    first_name=first_name, last_name=last_name, mobile=mobile, email=email, password=password)
                user.is_active = False
                user.save()
                # print(first_name, last_name, mobile,
                #       email, password, password2)

                current_site = get_current_site(request)
                email_subject = ' Activate your Account'
                message = render_to_string('activate.html',
                                           {
                                               'user': user,
                                               'domain': current_site.domain,
                                               'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                                               'token': generate_token.make_token(user)
                                           }



                                           )
                email_message = EmailMessage(
                    email_subject,
                    message,
                    settings.EMAIL_HOST_USER,
                    [email],
                )
                email_message.send()
                messages.info(
                    request, f"{first_name} Your account has been created successfully")
                return redirect('login')

        else:
            messages.warning(
                request, " Password and repeat Password are not the same, Try Again !")
            return redirect('createAccount')

    else:
        return render(request, 'createAccount.html')


def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        print(email, password)
        user = auth.authenticate(email=email, password=password)

        if user is not None:
            auth.login(request, user)
            messages.info(
                request, f"{user.first_name} You Logged in successfully ")
            return redirect('review')
        else:
            messages.warning(request, "Invalid Credentials"
                             )
            return redirect('login')
    else:
        return render(request, 'login.html')


def logout(request):
    auth.logout(request)
    messages.info(request, 'Goodbye!!!')
    return redirect('/')


class ActivateAccountView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)

        except Exception as identifier:
            user = None

        if user is not None and generate_token.check_token(user, token):
            user.is_active = True
            user.save()
            messages.add_message(request, messages.INFO,
                                 'account activated successfully')
            return redirect('login')
        return render(request, 'activate_failed.html', status=401)


def review_form(request):
    if request.method == 'POST':
        lecturerName = request.POST['lecturerName']
        lecturerCourse = request.POST['lecturerCourse']
        courseCode = request.POST['courseCode']
        communicationSkills = request.POST['communicationSkills']
        listeningSkills = request.POST['listeningSkills']
        userReview = request.POST['userReview']

        print(lecturerName, lecturerCourse, courseCode,
              communicationSkills, listeningSkills, userReview)

        # UsersReview = UsersReview.objects.create(lecturerName=lecturerName, lecturerCourse=lecturerCourse, courseCode=courseCode,
        #                                          communicationSkills=communicationSkills, listeningSkills=listeningSkills, userReview=userReview)
        # UsersReview.save()
        feedback = UsersReview.objects.create(lecturerName=lecturerName, lecturerCourse=lecturerCourse, courseCode=courseCode,
                                              communicationSkills=communicationSkills, listeningSkills=listeningSkills, userReview=userReview)
        feedback.save()
        email_subject = 'MUCG STUDENT FEEDBACK'
        message = f'lecturerName: {lecturerName}\n lecturerCourse: {lecturerCourse} \n courseCode: {courseCode} \n communication skills: {communicationSkills} \n listening Skills: {listeningSkills} \n Feedback-comment: {userReview}'
        email_message = EmailMessage(
            email_subject,
            message,
            settings.EMAIL_HOST_USER,
            ['alexanderemmanuel1719@gmail.com'],
        )
        email_message.send()

        messages.info(
            request, 'Message sent successfully . Thanks for the review')
        return render(request, 'review_form.html')

    else:
        return render(request, 'review_form.html')
