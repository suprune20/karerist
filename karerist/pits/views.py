# -*- coding: utf-8 -*-

import datetime

from django.db.models import Min, Max
from django.db.models.aggregates import Count
from django.views.generic import TemplateView

from pits.models import Pit, PitMaterial, Demand, PitLoad, PitRemain, \
                        Truck, TruckLoad, TruckRemain

class CalculateView(TemplateView):
    template_name = 'calculate.html'

    def post(self, request, *args, **kwargs):
        PitRemain.objects.all().delete()
        PitLoad.objects.all().delete()

        TruckRemain.objects.all().delete()
        TruckLoad.objects.all().delete()

        # Диапазон дат по всем потребностям
        start_date = Demand.objects.aggregate(min_=Min('start_date'))['min_']
        end_date = Demand.objects.aggregate(max_=Max('end_date'))['max_']
        for truck in Truck.objects.all():
            date = start_date
            while date < end_date:
                TruckRemain.objects.create(
                    truck=truck,
                    date=date,
                    trips=truck.trips,
                )
                date += datetime.timedelta(days=1)

        for demand in Demand.objects.all().order_by('dt_created'):
            date_volumes = demand.date_volumes()
            pits = demand.pits_available_all()
            for dv in date_volumes:
                # dict(date=..., volume=...)
                for pit in pits:
                    # dict(pit=pit, pitmaterial=pitmaterial, distance=distance)
                    if dv['volume'] > 0:
                        remain, created = PitRemain.objects.get_or_create(
                            pitmaterial=pit['pitmaterial'],
                            date=dv['date'],
                            defaults=dict(
                                volume=pit['pitmaterial'].capacity,
                        ))
                        this_volume = min(dv['volume'], remain.volume)
                        dv['volume'] -= this_volume
                        remain.volume -= this_volume
                        remain.save()
                        if this_volume > 0:
                            PitLoad.objects.create(
                                demand=demand,
                                date=dv['date'],
                                pitmaterial=pit['pitmaterial'],
                                volume=this_volume,
                                remains=this_volume,
                            )

        # сформированы pitLoads
        # Найти грузовик(и) для перевозки объема this_volume
        # из этого карьера
        # - выбрать по мин цене тонно-км
        # - чтоб в TruckRemain стался не ноль рейсов для грузовика
        # - чтоб грузоподъемность грузовика была <= остатка
        for pitload in PitLoad.objects.all().order_by('pk'):
            while True:
                try:
                    truckremain = TruckRemain.objects.filter(
                        date=pitload.date,
                        trips__gt=0,
                        truck__capacity__lte=pitload.remains,
                        ).select_related('truck'). \
                        order_by('truck__price_tcbm')[0]
                    truck = truckremain.truck
                    trips = min(truckremain.trips, pitload.remains // truck.capacity)
                    truckremain.trips -= trips
                    truckremain.save()
                    truck_volume = trips * truck.capacity
                    truckload, created =TruckLoad.objects.get_or_create(
                        date=pitload.date,
                        truck=truck,
                        pitload=pitload,
                        defaults=dict(
                            trips=trips,
                            volume=truck_volume,
                    ))
                    if not created:
                        truckload.trips += trips
                        truckload.volume += truck_volume
                        truckload.save()
                    # Сколько осталось в питлоаде. Если осталось, надо привлекать еще машины
                    pitload.remains -= truck_volume
                    pitload.save()
                    if pitload.remains == 0:
                        break
                    
                except IndexError:
                    # Не осталось грузовиков для выполнения потребности на день
                    break

        outc = []
        # Вывод для заказчика
        # По каждой demand
        # pits:     [ dict(pit=pit, pitmaterial=pitmaterial, distance=distance)
        # ]
        # dates:[ date: дата,
        #         volumes: [vol_pit1, vol_pit2 ...]
        #         total: сумма в карьерах
        #         need: потребность на дату
        #         not_satisfied: total - need
        # [
        for demand in Demand.objects.all().order_by('dt_created'):
            demandc = dict(demand=demand, pk=demand.pk)
            pits = demand.pits_available_all()
            demandc['pits'] = pits
            demandc['dates'] = []
            date_volumes = demand.date_volumes()
            for dv in date_volumes:
                date = dict(
                    date=dv['date'],
                    total=0,
                    need=dv['volume']
                )
                volumes = []
                for pit in pits:
                    try:
                        vol_in_pit = PitLoad.objects.get(
                            demand=demand,
                            date=dv['date'],
                            pitmaterial=pit['pitmaterial'],
                        ).volume
                    except PitLoad.DoesNotExist:
                        vol_in_pit = 0
                    date['total'] += vol_in_pit
                    volumes.append(vol_in_pit)
                date['volumes'] = volumes
                date['not_satisfied'] = date['need'] - date['total']
                demandc['dates'].append(date)
            outc.append(demandc)


        outp = []
        # Вывод для карьеров: таблицы Карьер/Материал
        # Находим в PitLoad все уникальные pitmaterial's
        # Находим в PitLoad даты, когда были ненулевые загрузки
        # Результат: список pitmaterials, в каждом из них:
        # pitmaterial: ... (отсюда беру price и др.)
        # demands: [] те потребности, которые были по этому pitmaterial
        # dates: [
        #   date:
        #   taken: (взято по всем потребностям)
        #   remain: остаток
        #   volumes: [ по demands ]
        # ]
        #
        pitmaterials = [ PitMaterial.objects.get(pk=pm) \
                         for pm in PitLoad.objects.order_by(
                             'pitmaterial__pit__name', 'pitmaterial__material__name',
                             'pitmaterial__fraction', 'pitmaterial__solidity').values_list(
                                 'pitmaterial', flat=True
                                 ).distinct()
        ]
        for pitmaterial in pitmaterials:
            pitmaterial_c = dict(
                pitmaterial=pitmaterial,
                dates=[]
            )
            dates = [ date for date in PitLoad.objects.filter(
                        pitmaterial=pitmaterial,volume__gt=0).order_by('date'). \
                        values_list('date', flat=True).distinct()
            ]
            demands = [ Demand.objects.get(pk=demand) for demand in PitLoad.objects.filter(
                        pitmaterial=pitmaterial,volume__gt=0).order_by('demand'). \
                        values_list('demand', flat=True).distinct()
            ]
            pitmaterial_c['demands'] = demands
            for date in dates:
                datec = dict(date=date, taken=0, remain=pitmaterial.capacity, volumes=[])
                for demand in demands:
                    try:
                        vol_in_demand = PitLoad.objects.get(
                            pitmaterial=pitmaterial,
                            date=date,
                            demand=demand,
                        ).volume
                    except PitLoad.DoesNotExist:
                        vol_in_demand = 0
                    datec['taken'] += vol_in_demand
                    datec['remain'] -= vol_in_demand
                    datec['volumes'].append(vol_in_demand)
                pitmaterial_c['dates'].append(datec)
            outp.append(pitmaterial_c)

        # Вывод загрузки грузовиков, по датам, рейсам и карьерам
        #   м1  
        #                   (п1)-альянс (п1)-сигма  (п2)-сигма
        #   30.09.16        3           2           1
        #
        # out_truck_pitload [
        #   truck:
        #   demand_pits: [
        #       demand:
        #       pit
        #   ]
        #   dates: [
        #       date:
        #       loads:
        #           [
        #               trips: (рейсы для 1-й из demand-pit:)
        #               volume: (объем для 1-й из demand-pit:)
        #               ....
        #           ]
        #   ]
        #
        # ]

        demand_pits =[
            dict(
                demand=Demand.objects.get(pk=item['demand']),
                pit=Pit.objects.get(pk=item['pitmaterial__pit']),
            )
            for item in PitLoad.objects. \
                        values('demand', 'pitmaterial__pit'). \
                        order_by('demand__pk', 'pitmaterial__pit__name'). \
                            annotate(count=Count('pk'))
        ]
        demand_pits_dict = dict()
        for i, demand_pit in enumerate(demand_pits):
            demand_pits_dict[(demand_pit['demand'], demand_pit['pit'])] = i
        
        out_truck_pitload = []
        for truck in Truck.objects.all().order_by('org__name', 'name'):
            truck_out = dict(truck=truck)
            truck_out['dates'] = []
            cur_date = None
            for tl in TruckLoad.objects.filter(truck=truck).order_by('date'):
                if tl.date != cur_date:
                    cur_date = tl.date
                    date = dict(
                        date=cur_date,
                        loads=[None] * len(demand_pits)
                    )
                    truck_out['dates'].append(date)
                i = demand_pits_dict[(tl.pitload.demand, tl.pitload.pitmaterial.pit)]
                date['loads'][i] = dict(trips=tl.trips, volume=tl.volume)

            out_truck_pitload.append(truck_out)

        # Таблица потребности-карьеры : грузовики
        # п1-альянс   м1  м2
        # 30.09.16    3   5
        #
        # п1-сигма    м1  м3
        # 30.09.16    2   1
        #
        # out_demand_trucs :[
        #   demand_pit: demand_pit
        #   dates: [
        #       date:
        #       trucks: [
        #           trips:
        #           volume:
        #       ]
        #       volume
        #   ]
        # ]
        
        trucks = [truck for truck in Truck.objects.all().order_by('org__name', 'name')]
        trucks_dict = dict()
        for i, truck in enumerate(trucks):
            trucks_dict[truck] = i

        out_demand_trucks = []
        for demand_pit in demand_pits:
            out_demand_pit = dict(demand_pit=demand_pit)
            out_demand_pit['dates'] = []
            cur_date = None
            for tl in TruckLoad.objects.filter(
                    pitload__demand=demand_pit['demand'],
                    pitload__pitmaterial__pit=demand_pit['pit'],
                ).order_by('date'):
                if tl.date != cur_date:
                    cur_date = tl.date
                    date = dict(
                        date=cur_date,
                        trucks=[None] * len(trucks),
                        volume=0
                    )
                    out_demand_pit['dates'].append(date)
                i = trucks_dict[tl.truck]
                date['trucks'][i] = dict(trips=tl.trips, volume=tl.volume)
                date['volume'] += tl.volume
            out_demand_trucks.append(out_demand_pit)

        context = dict(
            demand_pits=demand_pits,
            trucks=trucks,
            outc=outc,
            outp=outp,
            out_truck_pitload=out_truck_pitload,
            out_demand_trucks=out_demand_trucks,
        )
        return super(CalculateView, self).render_to_response(context)

calculate = CalculateView.as_view()
