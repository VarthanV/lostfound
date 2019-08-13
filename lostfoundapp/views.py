from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.core.exceptions import SuspiciousOperation
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.shortcuts import get_object_or_404
from django.contrib.auth import login, logout
from . models import Profile, Loser, Founder, FounderImage, LoserImage, MatchedRecord
import base64
import face_recognition
import datetime
import threading
import imdirect
from django.http import HttpResponse
from django.core.files.base import ContentFile
import uuid
import pytz
from . import align_faces
import os
import requests
from lostfoundapp.sendmail import *
dir_path = "/Users/vishnuvarthan/Desktop/lostfound/media"

headers = {
    "Content-Type": "application/json",
    "Authorization": "key=AAAAGUBo5V8:APA91bHLjHZ_5QDdzfCV9N7uAK6000ihsnQ9JEJg0gw_NcOUag9beUxgIF6rKRoW2nR99iy3ninu2ejQFhuzDD-6a89goLP8HkFOpqTKy-pj0_26lGDzMwyTKU_xV0Nnp8SGHB9qeVFG"
}


def sendnotif(record):
    for i in range(2):
        responses = [f"Your Child is found in{record.founder.location} ", f"The child you posted is in {record.loser.location}"]
        ids = [record.loser.loser.user.profile.device_id,
               record.founder.founder.user.profile.device_id]
        body = {
            "to": str(ids[i]),
            "notification": {
                "title": "Child Found",
                "body": responses[i] ,

                "sound": "default"
            },


        }

        response = requests.post('https://fcm.googleapis.com/fcm/send',
                                 headers=headers, json=body)
        print(response.status_code)


def losttesting(obj):

    media_path = os.path.join(os.getcwd(), "media")
    target_img_path = os.path.join(media_path, str(obj.img))
    target_img = face_recognition.load_image_file(target_img_path)
    print(target_img)
    target_img_enc = face_recognition.face_encodings(target_img)[0]
    all_objs = FounderImage.objects.filter(location=obj.location)
    if len(all_objs):

        for img_obj in all_objs:
            temp_img = face_recognition.load_image_file(img_obj.img)
            temp_img_enc = face_recognition.face_encodings(temp_img)[0]
            results = face_recognition.compare_faces(
                [target_img_enc], temp_img_enc)
            if results[0] == True:
                print("Found a match ")
                record = MatchedRecord()
                record.loser = obj
                record.founder = img_obj
                record.save()
                thread = threading.Thread(target=sendnotif, args=(record,))
                thread.start()
                send_mail_loser(record.founder.founder.user.email, record.founder.founder.user.username,
                                record.founder.founder.user.profile.phone_number)
                send_mail_founder(record.loser.loser.user.email, record.loser.loser.user.username,
                                  record.loser.loser.user.profile.phone_number)

            else:
                print("Not Found")


def foundtesting(obj):

    media_path = os.path.join(os.getcwd(), "media")
    target_img_path = os.path.join(media_path, str(obj.img))
    target_img = face_recognition.load_image_file(target_img_path)
    print(target_img)
    target_img_enc = face_recognition.face_encodings(target_img)[0]
    all_objs = LoserImage.objects.filter(location=obj.location)
    if len(all_objs):

        for img_obj in all_objs:
            temp_img = face_recognition.load_image_file(img_obj.img)
            temp_img_enc = face_recognition.face_encodings(temp_img)[0]
            results = face_recognition.compare_faces(
                [target_img_enc], temp_img_enc)
            if results[0] == True:
                print("Found a match ")
                record = MatchedRecord()
                record.loser = img_obj
                record.founder = obj
                record.save()
                thread = threading.Thread(target=sendnotif, args=(record,))
                thread.start()
                send_mail_loser(record.founder.founder.user.email, record.founder.founder.user.username,
                                record.founder.founder.user.profile.phone_number)
                send_mail_founder(record.loser.loser.user.email, record.loser.loser.user.username,
                                  record.loser.loser.user.profile.phone_number)


class LoginView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        if not request.user.is_authenticated:
            user = User.objects.get(email=request.POST.get('email'))

            if user is None:
                raise SuspiciousOperation
            user = authenticate(username=user.username,
                                password=request.POST.get('password'))
            if not user:
                raise SuspiciousOperation
            login(request, user)
            token, dummy = Token.objects.get_or_create(user=user)
            profile = Profile.objects.get(user=user)
            profile.device_id = request.POST.get('deviceid')
            profile.save()
            return Response({"token": token.key, 'username': user.username})


class RegisterView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        if User.objects.filter(username=request.POST.get('username')).exists() or User.objects.filter(email=request.POST.get('email')).exists():
            raise SuspiciousOperation
        else:
            user = User()
            user.email = request.POST.get('email')
            user.username = request.POST.get('username')
            user.set_password(request.POST.get('password'))
            user.save()
            profile = Profile()
            profile.user = user
            profile.location = request.POST.get('location')
            profile.phone_number = request.POST.get('phonenumber')
            profile.save()
            return Response({'registered': True})


class LostPostView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def post(self, request):
        dir_path = "/Users/vishnuvarthan/Desktop/lostfound/media"
        #date = request.POST.get('date').replace('/', ' ')
        #tz = pytz.timezone('Asia/Kolkata')
        #date = tz.localize(dt=datetime.datetime.strptime(date, r'%d %m %Y %I:%M %p'))
        if not hasattr(request.user, 'loser'):
            loser = Loser()
            loser.user = request.user
            loser.description = request.POST.get('description')
            loser.save()

        data = request.POST.get('image')

        name = str(uuid.uuid4())

        data = ContentFile(base64.b64decode(data), name=f"{name}.jpg")

        loser_img = LoserImage()
        loser_img.img = data
        loser_img.loser = request.user.loser
        loser_img.location = request.POST.get('location').title()
        loser_img.save()
        ab_path = os.path.join(dir_path, str(loser_img.img))
        align_faces.align_face(ab_path)

        print(ab_path)
        image = imdirect.imdirect_open(ab_path)
        print(loser_img.img)
        image.save(ab_path)
        thread = threading.Thread(target=losttesting, args=(loser_img,))
        thread.start()
        return Response({})


class FoundPostView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def post(self, request):
        if not hasattr(request.user, 'founder'):
            founder = Founder()
            founder.user = request.user
            founder.description = request.POST.get('description')
            founder.save()
        name = str(uuid.uuid4())
        data = request.POST.get('image')
        data = ContentFile(base64.b64decode(
            data), name=f'{name}.jpg')
        founder_img = FounderImage()
        founder_img.img = data
        founder_img.founder = request.user.founder
        founder_img.location = request.POST.get('location').title()
        founder_img.save()
        ab_path = os.path.join(dir_path, str(founder_img.img))

        print(ab_path)
        image = imdirect.imdirect_open(ab_path)
        align_faces.align_face(ab_path)
        thread = threading.Thread(target=foundtesting, args=(founder_img,))
        thread.start()

        return Response({})


class FounderHomeView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request):
        records = []
        for image in request.user.founder.founderimage_set.all():
            for record in image.matchedrecord_set.all():
                temp = {
                    'loser_name': record.loser.loser.user.username,
                    'loser_num': record.loser.loser.user.profile.phone_number,

                    'loser_location': record.loser.location,
                    'loser_img': record.loser.img.url,
                    'founder_img': record.founder.img.url,
                }
                records.append(temp)
        return Response(records)


class LoserHomeView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request):
        records = []
        for image in request.user.loser.loserimage_set.all():
            for record in image.matchedrecord_set.all():
                temp = {
                    'founder_name': record.founder.founder.user.username,
                    'founder_num': record.founder.founder.user.profile.phone_number,

                    'founder_location': record.founder.location,
                    'loser_img': record.loser.img.url,
                    'founder_img': record.founder.img.url,
                }
                records.append(temp)
        return Response(records)


class TestView(APIView):
    def get(self, request):
        records = []
        user = User.objects.get(pk=2)
        for image in user.founder.founderimage_set.all():
            for record in image.matchedrecord_set.all():
                temp = {
                    'loser_name': record.loser.loser.user.username,
                    'loser_num': record.loser.loser.user.profile.phone_number,
                    'loser_location': record.loser.location,
                    'description': record.loser.description,
                    'loser_img': record.loser.img.url,
                    'founder_img': record.founder.img.url
                }
            records.append(temp)
        return Response(records)
