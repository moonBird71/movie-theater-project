from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView

from django.views.generic import TemplateView
from django.urls import reverse_lazy, reverse
from ticketingApps.models import *
from ticketingApps.forms import *
from datetime import datetime
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
import json
from django.conf import settings
from django.utils import timezone
import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY 
class TicketTypeSelectionPage(FormView):
    form_class=TicketTypeForm
    template_name='ticketingApps/pick_ticket_type.html' 
    def get_success_url(self):
        return reverse('ticketingApps:order', kwargs={"numberTix":self.numberTix,"orderId":self.orderId})
    def calculate_price(self, form, showing):
        priceGroup = showing.pricing
        priceList = PricePoint.objects.filter(group=priceGroup)
        totalCost = 0
        for price in priceList:
            number=int(form.cleaned_data[price.name])
            totalCost = totalCost+number*int(price.price)
        promo=Promocode.objects.filter(code=form.cleaned_data['promocode'], theater=showing.room.theater).first()
        if promo is None:
            percentoff=0
        else:
            percentoff=promo.percent
        return totalCost*(1-percentoff/100)
    def get_form_kwargs(self):
        kwargs=super(TicketTypeSelectionPage,self).get_form_kwargs()
        showing = Movieshowing.objects.get(id=self.request.GET['showingId'])
        showingGroup = showing.pricing
        kwargs['pricingList']=PricePoint.objects.filter(group=showingGroup)
        toBuyArray = json.loads(self.request.GET['toBuy'])
        kwargs['numberTix']=len(toBuyArray)
        return kwargs
    def get_context_data(self, *args, **kwargs):
        context = super(TicketTypeSelectionPage, self).get_context_data(*args,**kwargs)
        toBuyArray = json.loads(self.request.GET['toBuy'])
        showing = Movieshowing.objects.get(id=self.request.GET['showingId'])
        showingGroup = showing.pricing
        context['pGroup']=PricePoint.objects.filter(group=showingGroup)
        context['numberTix']=len(toBuyArray)
        context['toBuy']=self.request.GET['toBuy']
        context['showingId']=self.request.GET['showingId']
        return context
    def form_valid(self,form):
        validSeats = True
        print(self.request.POST)
        showingP = Movieshowing.objects.get(id=self.request.GET['showingId'])
        toBuyArray = json.loads(self.request.GET['toBuy'])
        ticketsList = []
        orderObj = None
        for key in toBuyArray:
            if(Seatsbought.objects.filter(showing=showingP,seatrow=toBuyArray[key][0], seatcol=toBuyArray[key][1]).count()>0):
                validSeats = False
        if validSeats:
            if self.request.user.is_authenticated:
                profileU = Profile.objects.get(user=self.request.user)
                orderObj=Order.objects.create(profile=profileU)
            else:
                orderObj=Order.objects.create()
            for key in toBuyArray:
                Seatsbought.objects.create(seatrow=toBuyArray[key][0], seatcol=toBuyArray[key][1], showing=showingP,order=orderObj,expirationTime=timezone.now()+timedelta(minutes=10))
            orderObj.cost = float(self.calculate_price(form,showingP))
            orderObj.save()
            numberTix=len(toBuyArray)
            orderId=orderObj.orderid
        else:
            numberTix = 0
            orderId = -1
        self.numberTix=numberTix
        self.orderId=orderId
        return super(TicketTypeSelectionPage,self).form_valid(form)

class SeatSelectionPage(TemplateView):
    template_name='ticketingApps/seat_selection.html'
    def get_context_data(self, *args, **kwargs):
        context=super(SeatSelectionPage, self).get_context_data(*args,**kwargs)
        showingP = Movieshowing.objects.get(id=kwargs['showing'])
        context['showing']= showingP
        context['numberRows']= showingP.room.rows
        context['numberCols']= showingP.room.columns
        allSeatsBought=Seatsbought.objects.filter(showing=showingP)
        seatsBoughtList=[]
        seatsPicked=dict()
        for i in range(showingP.room.rows):
            seatsPicked[i+1]=dict()
            for j in range(showingP.room.columns):
                seatsPicked[i+1][j+1]="#0544F0"
        for seat in allSeatsBought:
            seatsBoughtList.append([seat.seatrow,seat.seatcol])
            seatsPicked[int(seat.seatrow)][int(seat.seatcol)]="#666666"
        context['seatsBought']=json.dumps(seatsBoughtList)
        context['seatsPicked']=json.dumps(seatsPicked)
        return context
class SimpleOrderPage(TemplateView):
    template_name='ticketingApps/order.html'
    def get_context_data(self,*args,**kwargs):
        context=super(SimpleOrderPage, self).get_context_data(*args,**kwargs)
        validSeats=False
        if int(self.kwargs["numberTix"])>0:
            validSeats=True
        context['valid']=validSeats
        if validSeats:
            orderId=int(self.kwargs['orderId'])
            orderObj = Order.objects.get(orderid=orderId)
            context['showingP'] = Seatsbought.objects.filter(order=orderObj).first().showing
            context['order'] = orderObj
            allSeats=Seatsbought.objects.filter(order=orderObj)
            context['numberTix']=allSeats.count()
            context['key']=settings.STRIPE_PUBLISHABLE_KEY
            context['cost']=orderObj.cost
            context['cost100']=orderObj.cost*100
        return context

def charge(request):
    if request.method =='POST':
        error=False
        errorMessage =""
        orderIdH = request.POST['orderId']
        seatsBoughtNow = Seatsbought.objects.filter(order=request.POST['orderId'])
        if(seatsBoughtNow[0].expirationTime<timezone.now()):
            for seat in seatsBoughtNow:
                seat.delete()
            print("Seats are no longer valid")
            try:
                ord1 =Order.objects.get(orderid=orderIdH)
                ord1.delete()
            except Exception as e:
                pass
            return render(request,"ticketingApps/chargeError.html")
        try:
            charge = stripe.Charge.create(
                amount=int(float(request.POST['cost100'])),
                currency = 'usd',
                description = 'A movie ticket purchase',
                source=request.POST['stripeToken']
            )            
            for seat in seatsBoughtNow:
                seat.final = True
                seat.save()
            Order.objects.get(orderid=orderIdH).save()
        except stripe.error.CardError as e:
            # Since it's a decline, stripe.error.CardError will be caught
            body = e.json_body
            err  = body.get('error', {})
            error = True
            errorMessage = err.get('message')
            print("card error")
        except stripe.error.RateLimitError as e:
        # Too many requests made to the API too quickly
            error=True
            print("rate limit")
            pass
        except stripe.error.InvalidRequestError as e:
        # Invalid parameters were supplied to Stripe's API
            error=True
            print("invalid request")
            pass
        except stripe.error.AuthenticationError as e:
        # Authentication with Stripe's API failed
        # (maybe you changed API keys recently)
            error=True
            print("authenticate error")
            pass
        except stripe.error.APIConnectionError as e:
        # Network communication with Stripe failed
            error=True
            print("api error")
            pass
        except stripe.error.StripeError as e:
        # Display a very generic error to the user, and maybe send
        # yourself an email
            error=True
            print("stripe error")
            pass
        except Exception as e:
        # Something else happened, completely unrelated to Stripe
            print("other exception")
            print(e)
            error=True
            pass
        if error:
            for seat in seatsBoughtNow:
                seat.delete()
            ord1 =Order.objects.get(orderid=orderIdH)
            ord1.delete()
            return render(request,"ticketingApps/chargeError.html")
        return render(request, 'ticketingApps/charge.html', {'orderIdH':orderIdH})
