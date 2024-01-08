from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received

from django.dispatch import receiver

from . models import Transaction, Donation

from django.conf import settings


@receiver(valid_ipn_received)
def paypal_payment_received(sender, **kwargs):
   
    ipn_obj = sender
   
    if ipn_obj.payment_status == ST_PP_COMPLETED:
       
        # Check 1: 
        # Ensure that the receiver email is the same as the business email 
       
        if ipn_obj.receiver_email != settings.PAYPAL_RECEIVER_EMAIL:
       
            # Return nothing if the payment is invalid 
       
            return


        # Check 2: 
        # Ensure that the amount paid and the currency is what is expected

        '''

        PLEASE keep in mind that there are many ways to do this check. This is just 
        a simple example of how you can do it.

        '''

        try:


            myDonation = Donation.objects.get(id=1) # Get the donation amount

            assert ipn_obj.mc_gross == myDonation.amount and ipn_obj.mc_currency == 'CZK'
       


        except Exception:
       
            print('Paypal ipn object data is invalid!')


       
        else:
            
            # Create a Transaction object if the payment was successful

            Transaction.objects.create(invoice=ipn_obj.invoice, title=ipn_obj.item_name, amount=ipn_obj.mc_gross, paid=True)


    else:

        # Return a message that the payment was not completed 

        print('Paypal payment status not completed: %s' % ipn_obj.payment_status)