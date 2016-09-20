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
            print "\n", demand
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
                dv['satisfied'] = dv['volume'] <= 0
                print "\n", dv

        return super(CalculateView, self).render_to_response(context)

calculate = CalculateView.as_view()
