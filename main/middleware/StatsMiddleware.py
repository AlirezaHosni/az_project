import time

from main.models import Statistic


class StatsMiddleware(object):
    def process_request(self, request):
        "Start time at request coming in"
        request.start_time = time.time()

    def process_response(self, request, response):
        "End of request, take time"
        total = time.time() - request.start_time

        # Add the header.
        statistic = Statistic.objects.get(response["method"])
        response["time"] = int(total * 1000)
        # response['average_time'] = statistic.average_time = (statistic.average_time + response["time"]) / statistic.times
        # statistic.save()
        return response
