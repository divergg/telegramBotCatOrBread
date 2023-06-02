from rest_framework import status
from rest_framework.response import Response


def handle_errors(data: list, allowed_fields: list):
    # Check that all fields are in request
    for field in allowed_fields:
        if field not in data:
            return Response({'error': f'Missing {field} field'}, status=status.HTTP_400_BAD_REQUEST)

    # Look for unexpected fields
    unexpected_fields = [field for field in data if field not in allowed_fields]
    if unexpected_fields:
        return Response({'error': f'Unexpected fields: {unexpected_fields}'}, status=status.HTTP_400_BAD_REQUEST)

