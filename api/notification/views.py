from datetime import datetime

from django.db.models import Count
from rest_framework import status, generics
from rest_framework.authentication import TokenAuthentication, SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.common import Pagination
from api.notification.serializers import NotificationSerializers
from core.models import Notification


class NotificationAdd(APIView):
    """
        ``GET`` lists all  notification

        ``POST`` Generates a request to notification user

         see :doc:`Flexible Security Framework `.

         **Example request**:

        .. code-block:: http

            GET  api/notification/list/

        **Example response**:

        .. code-block:: json

             [
                {
                    "id": 10,
                    "user": 2,
                    "user_name": "test",
                    "text": "Lo han inviatado a la meetup: hola, el cual es en la fecha 2020-10-28 06:00:00+00:00 ",
                    "date": "2020-10-02T12:55:54.318194Z",
                    "is_seen": false,
                    "is_read": false
                },
                {
                    "id": 11,
                    "user": 1,
                    "user_name": "",
                    "text": "El usuario name: test, email: test@gmail.com se registro en la  meetup hola",
                    "date": "2020-10-02T12:59:28.705128Z",
                    "is_seen": false,
                    "is_read": false
                }
            ]

        .. code-block:: http

            POST  api/notification/create/

            **Example response**:

            .. code-block:: json parameter required
                {
                    "text": [
                        "This field may not be blank."
                    ],
                    "user": [
                        "This field may not be blank."
                    ]
                }

                 {
                    'user': 1,
                    'text': 'llllllllllllllllllllllll',
                    'is_seen': false,
                    'is_read': false
                }

    """

    authentication_classes = [
        SessionAuthentication,
        BasicAuthentication,
        TokenAuthentication,
    ]
    permission_classes = (IsAuthenticated,)

    serializer_class = NotificationSerializers

    def get(self, request, format=None):
        """List all notification user"""
        """"return list all MeetupEnrollInviteUsers """
        user_id = self.request.GET.get('user_id', -1)
        count_is_seen = ''
        count_is_read = ''
        if int(user_id) > -1:
            meetup = Notification.objects.filter(
                user__id=user_id,
            )

            count_is_read = Notification.objects.filter(
                user__id=user_id,
                is_read=False
            ).values('is_read') \
                .order_by('is_read') \
                .annotate(count=Count('is_read'))

            count_is_seen = Notification.objects.filter(
                user__id=user_id,
                is_read=False
            ).values('is_seen') \
                .order_by('is_seen') \
                .annotate(count=Count('is_read'))

        else:
            meetup = Notification.objects.all()

        serializer = NotificationSerializers(meetup, many=True)

        result = [
            {
                'data': serializer.data,
                'count_is_seen': (count_is_seen[0]['count'] if 'count' in count_is_seen else 0),
                'count_is_read': (count_is_read[0]['count'] if 'count' in count_is_read else 0)
            }

        ]
        return Response(result)

    def post(self, request, format=None):
        """Create a new Notification"""
        serializer = NotificationSerializers(data=request.data)

        try:
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.initial_data, status=status.HTTP_201_CREATED)
        except Exception as error:
            errors = error.args[0]
            return Response({'error': errors}, content_type="application/json", status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NotificationModuleDetail(APIView):

    """
        retrieve:
            Return the given Notification
            GET api/meetup/get_notification/1

        Update:
            update a notification
            PUT api/notification/update/1
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
                    'user': user.pk,
                    'meetup': meetup.pk,
                    'user_check_in': True
                }

        Delete:
            delete a notification instance.
            DELETE api/notification/delete/1
    """

    def get_object(self, pk):
        try:
            object = Notification.objects.get(pk=pk)
            return object
        except Notification.DoesNotExist:
            from django.http import Http404
            raise Http404

    def get(self, request, pk, format=None):
        """Return detail of the meetup"""
        file_obj = self.get_object(pk)
        serializer = NotificationSerializers(file_obj)

        return Response(serializer.data)

    def put(self, request, pk, format=None):
        """Update meetup"""
        instance = self.get_object(pk)

        serializer = NotificationSerializers(instance, data=request.data)
        try:
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            errors = error.args[0]
            return Response({'error': errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        meetup = self.get_object(pk)
        meetup.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class NotificationSeenReadDetail(APIView):

    """
        Update:
            update a notification is seen or is read
            PUT api/notification/update/1
            :parameter
                {
                    "is_see": [
                        "This field is required."
                    ],
                    "is_read": [
                        "This field is required."
                    ]
                }
                Exmple is_read json:
                {
                    'is_read': true,

                }
                Exmple is_seen json:
                {
                    'is_seen': true,

                }

        Delete:
            delete a notification instance.
            DELETE api/notification/delete/1
    """

    def get_object(self, pk):
        try:
            object = Notification.objects.get(pk=pk)
            return object
        except Notification.DoesNotExist:
            from django.http import Http404
            raise Http404

    def put(self, request, pk, format=None):
        """update check in Notification"""

        if 'is_read' not in request.data and 'is_seen' not in request.data:
            return Response({
                    "is_seen": [
                        "This field is required."
                    ],
                    "is_read": [
                        "This field is required."
                    ]
                }, status=status.HTTP_201_CREATED
        )

        instance = self.get_object(int(pk))

        try:
            if 'is_read' in request.data:
                instance.is_read = request.data['is_read']
                instance.save()

            if 'is_seen' in request.data:
                instance.is_seen = request.data['is_seen']
                instance.save()

            serializer = NotificationSerializers(instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as error:
            errors = error.args[0]
            return Response({'error': errors}, content_type="application/json", status=status.HTTP_400_BAD_REQUEST)


class NotificationModuleList(generics.ListAPIView):
    """Return list of Notification on pagination"""
    authentication_classes = [
        SessionAuthentication,
        BasicAuthentication,
        TokenAuthentication,
    ]
    permission_classes = (IsAuthenticated,)

    serializer_class = NotificationSerializers
    pagination_class = Pagination

    def get_queryset(self):

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
                files = Notification.objects.filter(
                    id=filter
                )
            else:
                files = Notification.objects.filter(
                    user__name__contains=filter
                ) | Notification.objects.filter(
                    text__contains=filter
                ).order_by(sort_file)
        else:
            files = Notification.objects.get_queryset().order_by(sort_file)
        return files

    def is_date(self, date_text):
        try:
            if len(date_text[:10]) == 10 and date_text[:10] != datetime.strptime(date_text[:10], "%Y-%m-%d").strftime('%Y-%m-%d'):
                raise ValueError
            return True
        except ValueError:
            return False


