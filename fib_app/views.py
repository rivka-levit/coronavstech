from rest_framework import status

from rest_framework.views import APIView
from rest_framework.response import Response

from fibonacci.dynamic import fibonacci_dynamic_v2


class FibonacciView(APIView):
    def get(self, request):
        n = request.GET.get('n')
        rp = dict()

        if not n:
            return Response({
                'error_code': status.HTTP_400_BAD_REQUEST,
                'error_message': '`n` parameter is required'
            })
        else:
            try:
                n = int(n)
            except ValueError:
                return Response({
                    'error_code': status.HTTP_400_BAD_REQUEST,
                    'error_message': '`n` must be an integer'
                })

        try:
            fib_number = fibonacci_dynamic_v2(int(n))
        except ValueError as e:
            rp.update({
                'error_code': status.HTTP_400_BAD_REQUEST,
                'error_message': str(e)
            })
        except Exception as e:
            rp.update({
                'error_code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'error_message': str(e)
            })
        else:
            rp.update({
                'status': status.HTTP_200_OK,
                'n_requested': int(n),
                'fibonacci_number': fib_number
            })

        return Response(rp)
