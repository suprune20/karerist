# -*- coding: utf-8 -*-

from django.views.generic import TemplateView

from pits.models import Demand, DemandResult, DemandRemain

class CalculateView(TemplateView):
    template_name = 'calculate.html'

    def post(self, request, *args, **kwargs):
        context = dict(f='123')
        DemandRemain.objects.all().delete()
        DemandResult.objects.all().delete()
        for demand in Demand.objects.all().order_by('dt_created'):
            date_volumes = demand.date_volumes()
            pits = demand.pits_available_all()
            for dv in date_volumes:
                # dict(date=..., volume=...)
                for pit in pits:
                    # dict(pit=pit, pitmaterial=pitmaterial, distance=distance)
                    if dv['volume'] > 0:
                        remain, created = DemandRemain.objects.get_or_create(
                            pitmaterial=pit['pitmaterial'],
                            date=dv['date'],
                            defaults=dict(
                                volume=pit['pitmaterial'].capacity,
                        ))
                        this_volume = min(dv['volume'], remain.volume)
                        dv['volume'] -= this_volume
                        remain.volume -= this_volume
                        remain.save()
                        DemandResult.objects.create(
                            demand=demand,
                            date=dv['date'],
                            pitmaterial=pit['pitmaterial'],
                            volume=this_volume,
                        )

        outc = []
        # Вывод для заказчика
        # По каждой demand
        # pits:     [ dict(pit=pit, pitmaterial=pitmaterial, distance=distance)
        # ]
        # dates:[ date: дата,
        #         volumes: [vol_pit1, vol_pit2 ...]
        #         total: сумма в карьерах
        #         need: потребность на дату
        #         satisfied: total == need
        # [
        for demand in Demand.objects.all().order_by('dt_created'):
            demandc = dict(demand=demand)
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
                        vol_in_pit = DemandResult.objects.get(
                            demand=demand,
                            date=dv['date'],
                            pitmaterial=pit['pitmaterial'],
                        ).volume
                    except DemandResult.DoesNotExist:
                        vol_in_pit = 0
                    date['total'] += vol_in_pit
                    volumes.append(vol_in_pit)
                date['volumes'] = volumes
                date['satisfied'] = date['total'] >= date['need']
                demandc['dates'].append(date)
            outc.append(demandc)

        return super(CalculateView, self).render_to_response(context)

calculate = CalculateView.as_view()
