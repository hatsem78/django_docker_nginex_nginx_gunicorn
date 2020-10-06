from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from datetime import datetime
from core.models import Meetup, User, Notification


class Pagination(PageNumberPagination):
    """List all object for pagination"""
    page_size = 15

    def get_paginated_response(self, data):

        if 'page' in self.request.query_params:
            return Response({
                "prev_page_url": self.get_previous_link(),
                "from": self.page.paginator.page_range.start,
                "to": self.page.paginator.num_pages,
                "total": self.page.paginator.num_pages,
                "per_page": self.request.query_params['per_page'],
                "current_page": self.page.number,
                "last_page": (self.page.paginator.page_range.stop-1),
                "next_page_url": self.get_next_link(),
                'data': data,
            })
        else:
            return Response({
                "prev_page_url": self.get_previous_link(),
                "from": 1,
                "to": self.page.paginator.num_pages,
                "total": self.page.paginator.num_pages,
                "per_page": 1,
                "current_page": self.page.number,
                "last_page": 1,
                "next_page_url": self.get_next_link(),
                'data': data,
            })


class CalculateBeer:
    """
        A class used to represent an Calculate

        ...

        Attributes
        ----------
        __meetup_id : str: required
            represents the code of the represents the code of the meetup beer to which it belongs
        Properties created with the ``@property`` decorator should be documented
        in the property's getter method.
    """

    __meetup_id = 0

    def __init__(self, meetup_id=None):
        """
            The constructor for CalculateBeer class.

            Parameters:
                portfolio_id(str): required
                    represents the code of the portfolio to which it belongs
                 description(str):
                    Calculate count beer for the meetup beer
        """
        self.meetup_id = meetup_id

    @property
    def meetup_id(self):
        return self.__meetup_id

    @meetup_id.setter
    def meetup_id(self, value):
        if value is None:
            raise ValueError
        elif not isinstance(value, (int,)):
            raise TypeError("meetup_id must be integer")
        self.__meetup_id = value

    def calculate_count_beer(self):

        meetup = Meetup.objects.get(id=self.meetup_id)

        count_beer_person = 0
        count_participants = (meetup.count_participants + 1)

        if meetup.maximum_temperature < 20:
            count_beer_person = 0.75
        elif 20 <= meetup.maximum_temperature <= 24:
            count_beer_person = 1
        elif meetup.maximum_temperature > 24:
            count_beer_person = 3

        count_beer = count_beer_person * count_participants

        if round(count_beer / 6) > 1:
            count_box_beer = round(count_beer / 6)
        else:
            count_box_beer = 1

        count_beer = count_box_beer * 6 if count_box_beer > 1 else 6

        meetup.count_beer = count_beer
        meetup.count_box_beer = count_box_beer
        meetup.count_participants = count_participants
        meetup.save()

        return meetup


class RegisterNotification:
    """
            A class used to represent an Register Notification

            ...

            Attributes
            ----------
            __user : str: required
                represents the code of the code of the user to which it belongs
            __text : str: required
                represents the message of the send to user
            Properties created with the ``@property`` decorator should be documented
            in the property's getter method.
        """

    __user = None
    __text = None

    def __init__(self, user=User, text=None):
        """
            The constructor for RegisterNotification class.

            Parameters:
                user(str): required
                    represents the code of the user to which it belongs
                text(str): required
                    represents the message of the send to user
                 description(str):
                    Send notification for one user
        """
        self.user = user
        self.text = text

    @property
    def user(self):
        return self.__user

    @user.setter
    def user(self, value):
        if value is None:
            raise ValueError
        elif not isinstance(value, (User,)):
            raise TypeError("user  must be Object User")
        self.__user = value

    @property
    def text(self):
        return self.__text

    @text.setter
    def text(self, value):
        if value is None:
            raise ValueError
        elif not isinstance(value, (str,)):
            raise TypeError("text  must be str")
        self.__text = value

    def register_notifiaction(self):

        Notification.objects.create(
            user=self.user,
            date=datetime.now(),
            text=self.text,
            is_seen=False,
            is_read=False
        )


