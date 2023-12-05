from django.shortcuts import render,redirect
from rest_framework.views import APIView , View
from .serializers import UserSerializer, ChallengesSerializer, BlogSerializer
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
import jwt,datetime
import random
from django.http import JsonResponse
from .helpers import send_otp_email, send_forgot_email
import uuid
import pyotp
from rest_framework import generics, status
from .models import Challenges, BlogPost, User



# Create your views here.

class RegisterView(APIView):
    def post(self,request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
"""class LoginView(APIView):
    def post(self,request):
        email=request.data['email']
        password=request.data['password']
        
        user=User.objects.filter(email=email).first()
        if user is None:
            raise AuthenticationFailed('user not found')
        
        if not user.check_password(password):
            raise AuthenticationFailed("Incorrect password")
        
        payload = {
            'id':user.id,
            'exp':datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat':datetime.datetime.utcnow()
            }
        
        token = jwt.encode(payload, 'secret', algorithm='HS256').encode('utf-8')
        response = Response()
        
        response.set_cookie(key='jwt', value=token, httponly=True)
        
        response.data = {
            'jwt':token
        }
        return response"""
        
        
class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']
        
        user = User.objects.filter(email=email).first()
        if user is None:
            raise AuthenticationFailed('User not found')
        
        if not user.check_password(password):
            raise AuthenticationFailed("Incorrect password")
        
        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30),
            'iat': datetime.datetime.utcnow()
        }
        
        token = jwt.encode(payload, 'secret', algorithm='HS256')
        response = Response()
        
        response.set_cookie(key='jwt', value=token, httponly=True)
        
        response.data = {
            'jwt': token
        }
        return response

    
"""class UserView(APIView):
    def get(self,request):
        token = request.COOKIES.get('jwt')
        
        if not token:
            raise AuthenticationFailed("Incorrect password")
        
        try:
            payload = jwt.decode(token,'secret',algorithms=['HS256']).decode("ut")
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Incorrect password")
        
        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)
        return Response(serializer.data)"""
    

class UserView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')
        
        if not token:
            raise AuthenticationFailed("Token not provided")
        
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Token expired")
        except jwt.DecodeError:
            raise AuthenticationFailed("Invalid token")
        
        user = User.objects.filter(id=payload['id']).first()
        
        if not user:
            raise AuthenticationFailed("User not found")
        
        serializer = UserSerializer(user)
        return Response(serializer.data)    
    
    
class RandomView(APIView):
    def get(self,request):
        otp = ''.join(random.choice('0123456789') for _ in range(4))
        return JsonResponse({'otp': otp})
    
    
    
    
class ForgotPass(APIView):
    def post(self,request):
        try:
            email=request.data['email']
                    
            if not User.objects.filter(email=email).first():
                return JsonResponse({"message":"user not found"})
                    
            user_obj= User.objects.get(email=email)
            print(user_obj)
            token=str(uuid.uuid4())
            send_forgot_email(user_obj,token)
            return JsonResponse({"message":"email is sent"})
                
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Incorrect password")
        
        
class Otp_sent(APIView):
    def get(self, request):
        try:
            # Generate a random OTP
            totp = pyotp.TOTP(pyotp.random_base32(), interval=300)
            otp = totp.now()
            
            # Store OTP in the session
            request.session['otp'] = otp
            print(otp)
            
            email = request.data.get('email') 
                    
            if not User.objects.filter(email=email).exists():
                return JsonResponse({"message": "User not found with this email"})
                    
            user_obj = User.objects.get(email=email)
            print(user_obj)
            send_otp_email(user_obj, otp)  
            
            return JsonResponse({"message": "OTP has been sent via message"})
                
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Incorrect password")

            
            
class Otp_varify(APIView):
    def post(self,request):
        try:
            user_otp = request.data['ottp']
            stored_otp = request.session.get('otp')

            if user_otp == stored_otp:
                    # OTP is correct, perform further authentication or redirect as needed
                return JsonResponse({"message":'authenticated_page'})
            else:
                return JsonResponse({'message': 'Invalid OTP'}, status=400)
        except Exception as e:
            print(e)


from rest_framework.response import Response
from rest_framework.views import APIView
from twilio.rest import Client
import random

class whatsapp(APIView):
    def post(self, request):
        mobile = request.data.get("mobile")
        if not mobile:
            return Response({"error": "Please provide a mobile number"}, status=400)

        account_sid = 'AC496909bfd3cc0785577c3d3d7f6fb1b1'
        auth_token = 'f09cb0317bcd69f196b93d1177bea11b'
        twilio_number = '+14155238886'  

        client = Client(account_sid, auth_token)
        otp_code = ''.join(random.choices('0123456789', k=6))  

        message = client.messages.create(
            body=f"Your OTP is: {otp_code}",
            from_= "whatsapp:" + twilio_number,
            to= "whatsapp:" + mobile,
        )
        
        """message = client.messages.create(
            body=f"Your OTP is: {otp_code}",
            from_=  twilio_number,
            to=  mobile,
        )"""
        print(otp_code)
        return Response({"message_sid": message.sid})
        
        
        
class sms(APIView):
    def post(self, request):
        mobile = request.data.get("mobile")
        if not mobile:
            return Response({"error": "Please provide a mobile number"}, status=400)

        account_sid = 'AC496909bfd3cc0785577c3d3d7f6fb1b1'
        auth_token = 'be798b50dfa267884c5a38805f47bbf2'
        twilio_number = '+12056070858'  

        client = Client(account_sid, auth_token)
        otp_code = ''.join(random.choices('0123456789', k=6))  

        message = client.messages.create(
            body=f"Your OTP is: {otp_code}",
            from_=  twilio_number,
            to=  mobile,
        )
        print(otp_code)
        return Response({"message_sid": message.sid})
        


class ChallengesCreateAPIView(generics.CreateAPIView):
    queryset = Challenges.objects.all()
    serializer_class = ChallengesSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()
    
    
    def get(self, request):
        challenges = self.get_queryset()
        serializer = ChallengesSerializer(challenges, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)




class BlogPostAPI(APIView):
    queryset = Challenges.objects.all()
    serializer_class = BlogSerializer
    def post(self, request):
        serializer = BlogSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def get(self, request):
        blog_posts = BlogPost.objects.all()
        serializer = BlogSerializer(blog_posts, many=True)
        return Response(serializer.data)

    