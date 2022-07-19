import decimal
import json
import math
import time

from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.response import Response

from .models import Disk, Statistic, Index, Linked

# Create your views here.
from rest_framework.views import APIView


class initialize(APIView):
    def get(self, request, *args, **kwargs):
        for i in range(0, 100):
            Disk.objects.create()
        Statistic.objects.create(method='contiguous')
        Statistic.objects.create(method='linked')
        Statistic.objects.create(method='index', config=json.dumps({'blockSize': 10}))
        return Response('successful')


class freeDisk(APIView):
    def get(self, request, *args, **kwargs):
        disk = Disk.objects.all()
        for i in disk:
            i.isFull = False
            i.file_name = None
            i.save()
        Index.objects.all().delete()
        Linked.objects.all().delete()
        return Response('successful')


class ContiguousCreate(APIView):
    def post(self, request, *args, **kwargs):
        startT = time.time()
        name = request.data['name']
        size = int(request.data['size'])
        disk = Disk.objects.all()
        start = -1
        freeSpace = 0
        wasteSpace = 0
        created = False
        for i in disk:
            if i.isFull:
                wasteSpace = wasteSpace + freeSpace
                freeSpace = 0
            else:
                freeSpace = freeSpace + 1
                if freeSpace == size and not created:
                    freeSpace = 0
                    if not created:
                        start = i.id - size + 1
                        for j in disk.filter(id__range=(start, start + size - 1)):
                            j.isFull = True
                            j.file_name = name
                            j.save()
                        created = True
        statistic = Statistic.objects.get(method='contiguous')
        statistic.times = statistic.times + 1
        if start > -1:
            data = {'method': 'contiguous', 'message': 'Successful', 'start': start, 'waste space': wasteSpace}
            data['average_waste_space'] = statistic.average_waste_space = (wasteSpace * (
                    statistic.times - 1) + statistic.average_waste_space) / statistic.times
            data['time'] = (time.time() - startT) * 1000
            data['average_time'] = statistic.average_time = (statistic.average_time * (
                    statistic.times - 1) + decimal.Decimal(data["time"])) / statistic.times
            statistic.save()
        else:
            data = {'method': 'contiguous', 'message': 'Unsuccessful, there is not space in memory for this file'}

        return Response(data)


class ContiguousDelete(APIView):
    def post(self, request, *args, **kwargs):
        name = request.data['name']
        disk = Disk.objects.filter(file_name=name)
        for i in disk:
            i.isFull = False
            i.file_name = None
            i.save()
        return Response('successful')


class ChangeBlockSize(APIView):
    def post(self, request, *args, **kwargs):
        disk = Disk.objects.all()
        blockSize = request.data['block_size']
        for i in disk:
            i.isFull = False
            i.file_name = None
            i.save()
        Index.objects.all().delete()
        statistic = Statistic.objects.get(method='index')
        statistic.config = json.dumps({'blockSize': blockSize})
        return Response('successful')


class IndexCreate(APIView):
    def post(self, request, *args, **kwargs):
        startT = time.time()
        name = request.data['name']
        size = int(request.data['size'])
        statistic = Statistic.objects.get(method='index')
        blockSize = int(json.loads(statistic.config)['blockSize'])
        blockCount = math.ceil(float(size / blockSize))
        blockAvailable = 0
        remaining = size
        disk = Disk.objects.all()
        wasteSpace = 0
        indexes = []
        break_out_flag = False
        for i in range(0, disk.count()-blockSize, blockSize):
            if not disk[i].isFull:
                blockAvailable = blockAvailable + 1

        if blockAvailable < blockCount:
            data = {'method': 'index', 'message': 'Unsuccessful, there is not space in memory for this file'}
            return Response(data)

        for i in range(0, disk.count()-blockSize, blockSize):
            if not disk[i].isFull and remaining != 0:
                createdIndex = Index.objects.create(index=i)
                indexes.append(i)
                for j in range(i, i + 10):
                    if remaining == 0:
                        wasteSpace = wasteSpace + 9 + i - j
                        break_out_flag = True
                        break
                    current = disk[j]
                    current.isFull = True
                    current.file_name = name
                    current.save()
                    remaining = remaining - 1
                createdIndex.file_name = name
                createdIndex.block_size = blockSize
                createdIndex.save()
                if break_out_flag:
                    break
            elif disk[i].isFull:
                for j in range(i, i + 10):
                    if not disk[j].isFull:
                        wasteSpace = wasteSpace + 1

        statistic.times = statistic.times + 1
        data = {'method': 'index', 'message': 'Successful', 'block_size': blockSize, 'indexes': indexes,
                'waste space': wasteSpace}
        data['average_waste_space'] = statistic.average_waste_space = (wasteSpace * (
                    statistic.times - 1) + statistic.average_waste_space) / statistic.times
        data['time'] = (time.time() - startT) * 1000
        data['average_time'] = statistic.average_time = (statistic.average_time * (
                    statistic.times - 1) + decimal.Decimal(data['time'])) / statistic.times
        statistic.save()

        return Response(data)


class IndexDelete(APIView):
    def post(self, request, *args, **kwargs):
        name = request.data['name']
        disk = Disk.objects.filter(file_name=name)
        for i in disk:
            i.isFull = False
            i.file_name = None
            i.save()
        Index.objects.filter(file_name=name).delete()
        return Response('successful')


class LinkedCreate(APIView):
    def post(self, request, *args, **kwargs):
        startT = time.time()
        name = request.data['name']
        size = int(request.data['size'])
        remaining = size
        disk = Disk.objects.all()
        wasteSpace = 0
        indexes = []
        length = 0
        previousLink = None

        if disk.filter(isFull=False).count() < size:
            data = {'method': 'linked', 'message': 'Unsuccessful, there is not space in memory for this file'}
            return Response(data)

        for i in disk:
            if remaining <= 0:
                Linked.objects.create(file_name=name, index=i.id - length, length=length)
                indexes.append({'start': i.id - length, 'length': length})
                break
            if not i.isFull:
                if previousLink:
                    previousLink.next = i.id
                    previousLink.save()
                    previousLink = None
                i.isFull = True
                i.file_name = name
                i.save()
                length = length + 1
                remaining = remaining - 1
            else:
                if length != 0:
                    previousLink = Linked.objects.create(file_name=name, index=i.id - length, length=length)
                    indexes.append({'start': i.id - length, 'length': length})
                    length = 0

        statistic = Statistic.objects.get(method='linked')
        statistic.times = statistic.times + 1
        data = {'method': 'index', 'message': 'Successful', 'indexes': indexes}
        data['average_waste_space'] = 'there is not wasted space'
        data['time'] = (time.time() - startT) * 1000
        data['average_time'] = statistic.average_time = (statistic.average_time * (
                    statistic.times - 1) + decimal.Decimal(data['time'])) / statistic.times
        statistic.save()

        return Response(data)


class LinkedDelete(APIView):
    def post(self, request, *args, **kwargs):
        name = request.data['name']
        disk = Disk.objects.filter(file_name=name)
        for i in disk:
            i.isFull = False
            i.file_name = None
            i.save()
        Linked.objects.filter(file_name=name).delete()
        return Response('successful')
