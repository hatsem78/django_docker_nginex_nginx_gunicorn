from datetime import datetime

from rest_framework import status, generics
from rest_framework.authentication import TokenAuthentication, SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.common import Pagination
from core.models import Meetup

from api.meetup.serializers import MeetupSerializers


class MeetupAdd(APIView):

    """
        ``GET`` lists all  Meetups


         see :doc:`Flexible Security Framework `.

         **Example request**:

        .. code-block:: http

            GET  api/meetup/list/

        **Example response**:

        .. code-block:: json

             [
                {
                    "id": 1,
                    "name": "hola",
                    "date": "2020-10-28T06:00:00Z",
                    "description": "",
                    "count_beer": 0,
                    "maximum_temperature": 0.0,
                    "count_participants": 0,
                    "direction": "fasdasdf"
                }
            ]

        .. code-block:: http

            POST  api/meetup/create/
            :parameter
            {
                "name": [
                    "This field may not be blank."
                ],
                "date": [
                    "Datetime has wrong format. Use one of these formats instead: YYYY-MM-DDThh:mm[:ss[.uuuuuu]][+HH:MM|-HH:MM|Z]."
                ],
                "direction": [
                    "This field may not be blank."
                ]
            }

            **Example response**:

            .. code-block:: json parameter required

                 {
                    'user': self.user.pk,
                    'date': '2020-01-02 00:00:00',
                    'name': 'Meetup Beer2',
                    'description': 'Description Meetup2',
                    'count_beer': 36,
                    'maximum_temperature': 30.0,
                    'count_participants': 10,
                    'direction': "Avenida siempre viva 225"
                }

    """

    authentication_classes = [
        SessionAuthentication,
        BasicAuthentication,
        TokenAuthentication,
    ]
    permission_classes = (IsAuthenticated,)

    serializer_class = MeetupSerializers

    def get(self, request, format=None):
        """List all Meetup"""
        user_id = self.request.GET.get('user_id', -1)
        meetup = Meetup.objects.all()

        serializer = MeetupSerializers(meetup, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        """List create a new Meetup."""
        serializer = MeetupSerializers(data=request.data)

        try:
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.initial_data, status=status.HTTP_201_CREATED)
        except Exception as error:
            errors = error.args[0]
            return Response({'error': errors}, content_type="application/json", status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MeetupModuleDetail(APIView):
    """
        retrieve:
            Return the given the Meetup
            GET api/meetup/get_meetup/1

        Update:
            update a Meetup
            PUT api/meetup/update/1
            :parameter
                {
                    "name": [
                        "This field is required."
                    ],
                    "date": [
                        "This field is required."
                    ],
                    "direction": [
                        "This field is required."
                    ]
                }
                Exmple json:
                {
                    'user': 1,
                    'meetup': 1,
                    'user_check_in': True
                }

        Delete:
            delete a Meetup instance.
            DELETE api/meetup/delete/1
    """

    def get_object(self, pk):
        try:
            object = Meetup.objects.get(pk=pk)
            return object
        except Meetup.DoesNotExist:
            from django.http import Http404
            raise Http404

    def get(self, request, pk, format=None):
        """Return detail of the meetup"""
        file_obj = self.get_object(pk)
        serializer = MeetupSerializers(file_obj)

        return Response(serializer.data)

    def put(self, request, pk, format=None):
        """Update meetup"""
        instance = self.get_object(pk)
        serializer = MeetupSerializers(instance, data=request.data)
        try:
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            errors = error.args[0]

    def delete(self, request, pk, format=None):
        """Delete meetup"""
        meetup = self.get_object(pk)
        meetup.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MeetupModuleList(generics.ListAPIView):
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
                            "id": 1,
                            "name": "hola",
                            "date": "2020-10-28T06:00:00Z",
                            "description": "",
                            "count_beer": 0,
                            "maximum_temperature": 0.0,
                            "count_participants": 0,
                            "direction": "fasdasdf"
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

    serializer_class = MeetupSerializers
    pagination_class = Pagination

    def get_queryset(self):
        """Return list of meetup on pagination"""
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
                files = Meetup.objects.filter(
                    id=filter
                )
            else:
                files = Meetup.objects.filter(
                    name__contains=filter
                ) | Meetup.objects.filter(
                    direction__contains=filter
                ).order_by(sort_file)
        else:
            files = Meetup.objects.get_queryset().order_by(sort_file)
        return files

    def is_date(self, date_text):
        try:
            if len(date_text[:10]) == 10 and date_text[:10] != datetime.strptime(date_text[:10], "%Y-%m-%d").strftime('%Y-%m-%d'):
                raise ValueError
            return True
        except ValueError:
            return False


