from rest_framework import status, generics
from rest_framework.authentication import TokenAuthentication, SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.common import RegisterNotification
from api.meetup_enroll_invite_users.serializers import MeetupEnrollInviteUsersSerializers
from core.models import User, Meetup, MeetupEnrollInviteUsers


class RegistrationCheckInUserView(APIView):
    """
        Check_in:
            update a Check_in
            PUT api/registration_check_in_user/registration/1
            :parameter
                {
                    "user": [
                        "This field is required."
                    ],
                    "text": [
                        "This field is required."
                    ]
                }
                Exmple json:
                {
                    'user': 1,
                    'meetup': 1,
                    'user_check_in': True
                }
         Registration:
            create a registration
            post api/registration_check_in_user/registration/1
            :parameter
                {
                    "user": [
                        "This field is required."
                    ],
                    "text": [
                        "This field is required."
                    ]
                }
                Exmple json:
                {
                    'user': 1,
                    'meetup': 1,
                    'user_check_in': True
                }

    """

    authentication_classes = [
        SessionAuthentication,
        BasicAuthentication,
        TokenAuthentication,
    ]
    permission_classes = (IsAuthenticated,)

    serializer_class = MeetupEnrollInviteUsersSerializers

    def get_object(self, pk):
        try:
            object = MeetupEnrollInviteUsers.objects.get(pk=pk)
            return object
        except MeetupEnrollInviteUsers.DoesNotExist:
            from django.http import Http404
            raise Http404

    def post(self, request, format=None):
        """List all Meetup Enroll InviteUse, create a new Meetup."""

        serializer = MeetupEnrollInviteUsersSerializers(data=request.data)

        if 'user' not in request.data or int(request.data['user']) <= 0:
            return Response({
                    "user": [
                        "This field is required."
                    ],
                }, status=status.HTTP_201_CREATED)
        if 'meetup' not in request.data or int(request.data['meetup']) <= 0:
            return Response({
                    "meetup": [
                        "This field is required."
                    ],
                }, status=status.HTTP_201_CREATED)

        try:
            if serializer.is_valid():
                serializer.save()
                self.__registre_notification(request, serializer.data)
                return Response(serializer.initial_data, status=status.HTTP_201_CREATED)
        except Exception as error:
            errors = error.args[0]
            return Response({'error': errors}, content_type="application/json", status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, format=None):
        """update check in meetup"""
        if 'user' not in request.data or int(request.data['user']) <= 0:
            return Response({
                    "user": [
                        "This field is required."
                    ],
                }, status=status.HTTP_201_CREATED)
        if 'meetup' not in request.data or int(request.data['meetup']) <= 0:
            return Response({
                    "meetup": [
                        "This field is required."
                    ],
                }, status=status.HTTP_201_CREATED)
        instance = self.get_object(int(pk))

        if 'user' in request.data and 'user_check_in' in request.data:
            try:
                instance.user_check_in = request.data['user_check_in']
                instance.save()
                serializer = MeetupEnrollInviteUsersSerializers(instance)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Exception as error:
                errors = error.args[0]
                return Response({'error': errors}, content_type="application/json", status=status.HTTP_400_BAD_REQUEST)

    def __registre_notification(self, request, trans):

        if request.user.is_superuser:
            text = f"Se a registrado en la meetup: {trans['meetup_name']}, el cual es en la fecha {trans['meetup_date']} "
            user = User.objects.get(pk=trans['user'])
            notification = RegisterNotification(user, text)
            notification.register_notifiaction()

        else:
            meetup = Meetup.objects.get(pk=trans['meetup'])
            user = User.objects.get(pk=meetup.user.pk)
            text = f"El usuario name: {request.user.name}, email: {request.user.email} se registro en la  meetup {trans['meetup_name']}"

            notification = RegisterNotification(user, text)
            notification.register_notifiaction()

    def __check_in_notification(self, request, trans):

        meetup = Meetup.objects.get(pk=trans['meetup'])
        user = User.objects.get(pk=meetup.user.pk)
        text = f"El usuario name: {request.user.name}, email: {request.user.email} ha asistido  en la  meetup {trans['meetup_name']}"

        notification = RegisterNotification(user, text)
        notification.register_notifiaction()
