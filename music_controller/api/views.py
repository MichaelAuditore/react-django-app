"""Views Module"""
from django.http import JsonResponse

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Room
from .serializers import CreateRoomSerializer, RoomSerializer, UpdateRoomSerializer

# Create your views here.


class RoomView(generics.ListAPIView):
    """
        Class Inherits from a generic API view and
        returns all Room objects from database
    """
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class GetRoom(APIView):
    """ Get Room Model by Code Room """
    serializer_class = RoomSerializer
    lookup_url_kwarg = 'code'

    def get(self, request, format=None):
        """Get the code in Request URL """
        code = request.GET.get(self.lookup_url_kwarg)
        if code is not None:
            room = Room.objects.filter(code=code)
            if room.exists():
                data = RoomSerializer(room[0]).data
                _is_host = self.request.session.session_key == room[0].host
                data['is_host'] = _is_host
                return Response(data, status=status.HTTP_200_OK)

            return Response({'Room Not Found': 'Invalid Room Code.'},
                            status=status.HTTP_404_NOT_FOUND)
        return Response(
            {'Bad Request': 'Code parameter not found in request.'},
            status=status.HTTP_400_BAD_REQUEST
        )


class JoinRoom(APIView):
    """ Class to check if it is possible to join to an existing room """
    lookup_url_kwarg = 'code'

    def post(self, request):
        """Post method to receive a POST request to JOIN in a Room"""
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()

        code = request.data.get(self.lookup_url_kwarg)
        if code is not None:
            room_result = Room.objects.filter(code=code)
            if room_result.exists():
                room = room_result[0]
                self.request.session['room_code'] = room.code
                return Response(
                    {'message': 'Room Joined!'},
                    status=status.HTTP_200_OK
                )

            return Response(
                {'Bad Request': 'Invalid Room COde'},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {'Bad Request': 'Invalid post data, did not find a code key'},
            status=status.HTTP_400_BAD_REQUEST
        )


class UserInRoom(APIView):
    """
        Class to check if a user is active in a
        Room using inherits from APIView
    """

    def get(self, request):
        """
            Get data about an user to know he's active in a Room
            self: Room Model
            request: request sended via Client
            format: define it's a request format is required
        """
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()

        data = {
            'code': self.request.session.get('room_code')
        }

        return JsonResponse(data, status=status.HTTP_200_OK)


class CreateRoomView(APIView):
    """ Class to create a RoomView using a APIView """

    serializer_class = CreateRoomSerializer

    def post(self, request):
        """Create or update an existing Room"""
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            guest_can_pause = serializer.data.get('guest_can_pause')
            votes_to_skip = serializer.data.get('votes_to_skip')
            host = self.request.session.session_key
            queryset = Room.objects.filter(host=host)
            if queryset.exists():
                room = queryset[0]
                room.guest_can_pause = guest_can_pause
                room.votes_to_skip = votes_to_skip
                room.save(update_fields=[
                    'guest_can_pause', 'votes_to_skip'])
                self.request.session['room_code'] = room.code
                return Response(
                    RoomSerializer(room).data,
                    status=status.HTTP_201_CREATED
                )
            else:
                room = Room(
                    host=host,
                    guest_can_pause=guest_can_pause,
                    votes_to_skip=votes_to_skip
                )
                room.save()
                self.request.session['room_code'] = room.code
                return Response(
                    RoomSerializer(room).data,
                    status=status.HTTP_201_CREATED
                )

        return Response(
            {'Bad Request': 'Invalid data...'},
            status=status.HTTP_400_BAD_REQUEST
        )


class LeaveRoom(APIView):
    """ Class to Remove an Active Home from a Room """

    def post(self, request):
        """Post request to remove a Host from a Room"""
        if 'room_code' in self.request.session:
            self.request.session.pop('room_code')
            host_id = self.request.session.session_key
            room_results = Room.objects.filter(host=host_id)
            if room_results.exists():
                room = room_results[0]
                room.delete()

        return Response(
            {'Message': 'Success'},
            status=status.HTTP_200_OK
        )


class UpdateRoom(APIView):
    """Class to update a model inherits from APIView"""
    serializer_class = UpdateRoomSerializer

    def patch(self, request, format=None):
        """Update a Room Model"""

        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            guest_can_pause = serializer.data.get('guest_can_pause')
            votes_to_skip = serializer.data.get('votes_to_skip')
            code = serializer.data.get('code')

            queryset = Room.objects.filter(code=code)
            if not queryset.exists():
                return Response({'msg': 'Room not found.'}, status=status.HTTP_404_NOT_FOUND)

            room = queryset[0]
            user_id = self.request.session.session_key
            if room.host != user_id:
                return Response({'msg': 'You are not the host of this room.'}, status=status.HTTP_403_FORBIDDEN)

            room.guest_can_pause = guest_can_pause
            room.votes_to_skip = votes_to_skip
            room.save(update_fields=['guest_can_pause', 'votes_to_skip'])

            return Response(RoomSerializer(room).data, status=status.HTTP_200_OK)

        return Response({'Bad Request': "Invalid Data..."}, status=status.HTTP_400_BAD_REQUEST)
