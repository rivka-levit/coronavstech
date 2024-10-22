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
                'status': 'error',
                'message': '`n` parameter is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                n = int(n)
            except ValueError:
                return Response({
                    'status': 'error',
                    'message': '`n` must be an integer'
                })

        try:
            fib_number = fibonacci_dynamic_v2(n)
        except ValueError as e:
            rp.update({
                'status': 'error',
                'message': str(e)
            })
        except Exception as e:
            rp.update({
                'status': 'error',
                'message': str(e)
            })
        else:
            rp.update({
                'status': 'success',
                'n_requested': n,
                'fibonacci_number': fib_number
            })

        return Response(rp, status=status.HTTP_200_OK)
