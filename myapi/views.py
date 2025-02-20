# from rest_framework import viewsets
# from .models import User, Movie, Actor, Comment
# from .serializers import UserSerializer, MovieSerializer, ActorSerializer, CommentSerializer
# from rest_framework.permissions import IsAuthenticated, AllowAny
#
#
# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     permission_classes = [IsAuthenticated]
#
#
# class MovieViewSet(viewsets.ModelViewSet):
#     queryset = Movie.objects.all()
#     serializer_class = MovieSerializer
#     permission_classes = [AllowAny]
#
#
# class ActorViewSet(viewsets.ModelViewSet):
#     queryset = Actor.objects.all()
#     serializer_class = ActorSerializer
#     permission_classes = [AllowAny]
#
#
# class CommentViewSet(viewsets.ModelViewSet):
#     queryset = Comment.objects.all()
#     serializer_class = CommentSerializer
#     permission_classes = [IsAuthenticated]

from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Movie, Actor, Comment
from .permissions import IsAdminOrReadOnly
from .serializers import MovieSerializer, ActorSerializer, CommentSerializer
from random import randint

from django.core.cache import cache
from    drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import User
from .serializers import VerifyOTPSerializer, RegisterSerializer, PhoneSerializer


class MovieList(generics.ListCreateAPIView):
    permission_classes = [IsAdminOrReadOnly]
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


    @action(detail=True, methods=['post'])
    def add_actor(self, request, pk=None):
        """
        Aktyorni mavjud kinoga qo'shish
        """
        movie = self.get_object()
        actor_id = request.data.get('actor_id')

        if not actor_id:
            return Response({"error": "actor_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            actor = Actor.objects.get(id=actor_id)
        except Actor.DoesNotExist:
            return Response({"error": "Actor not found"}, status=status.HTTP_404_NOT_FOUND)

        movie.actors.add(actor)
        return Response({"message": f"Actor {actor.name} added to movie {movie.title}"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def create_and_add_actor(self, request, pk=None):
        """
        Yangi aktyor yaratib, kinoga qo'shish
        """
        movie = self.get_object()
        actor_serializer = ActorSerializer(data=request.data)

        if actor_serializer.is_valid():
            actor = actor_serializer.save()
            movie.actors.add(actor)
            return Response({
                "message": f"Actor {actor.name} created and added to movie {movie.title}",
                "actor": actor_serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response(actor_serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class MovieDetail(generics.RetrieveUpdateDestroyAPIView):
     permission_classes = [IsAdminOrReadOnly]
     queryset = Movie.objects.all()
     serializer_class = MovieSerializer

class ActorList(generics.ListCreateAPIView):
    permission_classes = [IsAdminOrReadOnly]
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer

class ActorDetail(generics.RetrieveUpdateDestroyAPIView):
     permission_classes = [IsAdminOrReadOnly]
     queryset = Actor.objects.all()
     serializer_class = ActorSerializer


class CommentListApiView(APIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, movie_id):
        comments = Comment.objects.filter(movie__id=movie_id)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=CommentSerializer)
    def post(self, request, movie_id):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            movie = Movie.objects.get(id=movie_id)
            serializer.save(user=request.user, movie=movie)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
     permission_classes = [IsAdminOrReadOnly,IsAuthenticated]
     serializer_class = CommentSerializer

     def get_queryset(self):
         comment_id = self.kwargs.get('pk')
         return Comment.objects.filter(id=comment_id)





class PhoneAPIView(APIView):
    @swagger_auto_schema(request_body=PhoneSerializer)
    def post(self, request):
        serializer = PhoneSerializer(data=request.data)
        if serializer.is_valid():
            phone = serializer.validated_data['phone']

            otp_code = str(randint(1000, 9999))
            print("Yaratilgan OTP:", otp_code)

            cache.set(phone, {"otp": otp_code, "phone_number": phone}, timeout=900)

            return Response(
                {"success":True,"detail":"Sizga kod yuborildi!"},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyOTPAPIView(APIView):
        @swagger_auto_schema(request_body=VerifyOTPSerializer)
        def post(self, request):
            serializer = VerifyOTPSerializer(data=request.data)
            if serializer.is_valid():
                phone = serializer.validated_data['phone']
                verification_code = serializer.validated_data['verification_code']
                cached_otp = cache.get(phone)

                if str(cached_otp.get("otp")) == str(verification_code):

                    return Response(
                        {"success":True,"detail":"OTP tasdiqlandi. Endi ro'yxatdan o'tishingiz mumkin."},
                        status=status.HTTP_200_OK
                    )

                return Response(
                    {"success":False,"detail":"Noto‘g‘ri raqam yoki eskirgan OTP kod."},
                     status=status.HTTP_400_BAD_REQUEST
                )

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegisterAPIView(APIView):
    @swagger_auto_schema(request_body=RegisterSerializer)
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():

            phone = serializer.validated_data['phone']
            cached_data = cache.get(phone)

            if not cached_data:
                return Response(
                    {"success": False, "detail": "Telefon raqamingiz tasdiqlangan raqamga moskelmadi emas!"}
                )

            phone_number = cached_data.get("phone_number")

            if str(phone_number) == str(phone):
                serializer.save()
                return Response(
                    {"success": True, "detail": "Ro'yxatdan o'tish muvaffaqiyatli amalga oshdi"},
                    status=status.HTTP_201_CREATED
                )


        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        serializer = RegisterSerializer(request.user)

        return Response(
            {"success":True,"data":serializer.data},
            status=status.HTTP_200_OK
        )

    def patch(self, request):
        serializer = RegisterSerializer(request.user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"success":True,"data":serializer.data},
                status=status.HTTP_201_CREATEDOK
            )

