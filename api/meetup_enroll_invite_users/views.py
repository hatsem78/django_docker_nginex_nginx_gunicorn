import datetime

from rest_framework import status, generics
from rest_framework.authentication import TokenAuthentication, SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.common import Pagination, RegisterNotification
from api.meetup_enroll_invite_users.serializers import MeetupEnrollInviteUsersSerializers
from core.models import MeetupEnrollInviteUsers, User, Notification, Meetup


class MeetupEnrollInviteUsersAdd(APIView):
    """
        ``GET`` lists all  Enroll or Invite Users in the Meetup

        ``POST`` Generates a request to Enroll or Invite a user to a Meetup

         see :doc:`Flexible Security Framework `.

         **Example request**:

        .. code-block:: http

            GET  api/meetup_enroll_invite_users/list/

        **Example response**:

        .. code-block:: json

             [
                {
                    "id": 30,
                    "user": 2,
                    "user_name": "test",
                    "user_email": "test@gmail.com",
                    "meetup": 1,
                    "meetup_name": "hola",
                    "meetup_date": "2020-10-28T06:00:00Z",
                    "user_check_in": false
                }
            ]

        .. code-block:: http

            POST  api/meetup_enroll_invite_users/create/

            **Example response**:

            .. code-block:: json parameter required

                 {
                    "user" : 2,
                    "meetup" : 1

                }
    """

    authentication_classes = [
        SessionAuthentication,
        BasicAuthentication,
        TokenAuthentication,
    ]
    permission_classes = (IsAuthenticated,)

    serializer_class = MeetupEnrollInviteUsersSerializers

    def get(self, request, format=None):
        """"return list all MeetupEnrollInviteUsers """
        user_id = self.request.GET.get('user_id', -1)

        if int(user_id) > -1:
            meetup = MeetupEnrollInviteUsers.objects.filter(
                user__id=user_id,
                user_check_in=False
            )
        else:
            meetup = MeetupEnrollInviteUsers.objects.all()

        serializer = MeetupEnrollInviteUsersSerializers(meetup, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        """List all Meetup Enroll InviteUse, create a new Meetup."""
        serializer = MeetupEnrollInviteUsersSerializers(data=request.data)

        try:
            if serializer.is_valid():
                serializer.save()
                self.__registre_notification(request, serializer.data)
                return Response(serializer.initial_data, status=status.HTTP_201_CREATED)
        except Exception as error:
            errors = error.args[0]
            return Response({'error': errors}, content_type="application/json", status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def __registre_notification(self, request, trans):

        if request.user.is_superuser:
            text = f"Lo han inviatado a la meetup: {trans['meetup_name']}, el cual es en la fecha {trans['meetup_date']} "
            user = User.objects.get(pk=trans['user'])
            notification = RegisterNotification(user, text)
            notification.register_notifiaction()

        else:
            meetup = Meetup.objects.get(pk=trans['meetup'])
            user = User.objects.get(pk=meetup.user.pk)
            text = f"El usuario name: {request.user.name}, email: {request.user.email} se registro en la  meetup {trans['meetup_name']}"

            notification = RegisterNotification(user, text)
            notification.register_notifiaction()


class MeetupEnrollInviteUsersModuleDetail(APIView):

    """
        retrieve:
            Return the given Enroll or Invite User in the Meetup
            GET api/meetup/get_meetup_enroll_invite_users/1

        Update:
            update a Enroll or Invite User in the Meetup if user check in meetup
            PUT api/meetup_enroll_invite_users/update/1
            :parameter
                user is required
                meetup is required
                user_check_in is required
                Exmple json:
                {
                    'user': 1,
                    'meetup': 1,
                    'user_check_in': True
                }

        Delete:
            delete a MeetupEnrollInviteUsersModuleDetail instance.
            DELETE api/meetup_enroll_invite_users/delete/1
    """

    def get_object(self, pk):
        try:
            object = MeetupEnrollInviteUsers.objects.get(pk=pk)
            return object
        except MeetupEnrollInviteUsers.DoesNotExist:
            from django.http import Http404
            raise Http404

    def get(self, request, pk, format=None):
        """Return detail of the MeetupEnrollInviteUsersModuleDetail"""
        file_obj = self.get_object(pk)
        serializer = MeetupEnrollInviteUsersSerializers(file_obj)

        return Response(serializer.data)

    def put(self, request, pk, format=None):
        """Update MeetupEnrollInviteUsersModuleDetail"""
        instance = self.get_object(pk)
        serializer = MeetupEnrollInviteUsersSerializers(instance, data=request.data)
        try:
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            errors = error.args[0]

    def delete(self, request, pk, format=None):
        """Delete MeetupEnrollInviteUsersModuleDetail"""
        meetup = self.get_object(pk)
        meetup.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MeetupEnrollInviteUsersModuleList(generics.ListAPIView):

    """
        retrieve:
            Return list of meetup on pagination
            Example:
                {
                    "prev_page_url": null,
                    "from": 1,
                    "to": 1,
                    "total": 1,
                    "per_page": 1,
                    "current_page": 1,
                    "last_page": 1,
                    "next_page_url": null,
                    "data": [
                        {
                            "id": 30,
                            "user": 2,
                            "user_name": "test",
                            "user_email": "test@gmail.com",
                            "meetup": 1,
                            "meetup_name": "hola",
                            "meetup_date": "2020-10-28T06:00:00Z",
                            "user_check_in": false
                        }
                    ]
                }
    """

    authentication_classes = [
        SessionAuthentication,
        BasicAuthentication,
        TokenAuthentication,
    ]
    permission_classes = (IsAuthenticated,)

    serializer_class = MeetupEnrollInviteUsersSerializers
    pagination_class = Pagination

    def get_queryset(self):
        """ Filter MeetupEnrollInviteUsersModuleList for option date, name and user_check"""
        filter = self.request.GET.get('filter', None)
        sort = self.request.GET.get('sort', None)
        sort_file = 'id'
        if sort is not None:
            sort = self.request.GET['sort'].split('|')
            if sort[1] == 'desc':
                sort_file = f"{sort[0]}"
            else:
                sort_file = f"-{sort[0]}"

        if filter is not None:
            if filter.isnumeric():
                files = MeetupEnrollInviteUsers.objects.filter(
                    id=filter
                )
            elif self.is_date(filter):
                files = MeetupEnrollInviteUsers.objects.filter(
                    date__contains=filter[:10]
                )
            else:
                files = MeetupEnrollInviteUsers.objects.filter(
                    name__contains=filter
                ) | MeetupEnrollInviteUsers.objects.filter(
                    description__contains=filter
                ) | MeetupEnrollInviteUsers.objects.filter(
                    user_check_in_contains=filter
                ).order_by(sort_file)
        else:
            files = MeetupEnrollInviteUsers.objects.get_queryset().order_by(sort_file)
        return files
