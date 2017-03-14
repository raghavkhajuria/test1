from datetime import datetime, timedelta
from services.haversine import haversine

__author__ = "akanksha", "raghav"


def promo_code_didnt_work(intent, entities, data):
    if intent == '1A_PromoCodeDidntWork':
        try:
            code = entities['promo_code']
            if not code:
                raise KeyError
        except KeyError:
            return "I can help you with that. Can you tell me what promo code you are trying to use?"

        if data:
            if data['promocodeapplied'] is None or data['promocodeapplied'] == '':
                return "I just checked our system, and unfortunately it seems that you did not apply any promo code to this trip." \
                       "You can use this same promo code again for your next trip."
            else:
                if data['promocodeapplied'] != code:
                    return "It looks like that the promo code you entered was " + data['promocodeapplied'] + ". This" +\
                           " was successfully applied."
                elif data['promocodename'] != data['promocodeapplied']:
                    return "It looks like that the promo code you entered was " + data['promocodeapplied'] + ". This," +\
                           " unfortunately, is not a valid promo code."
                else:
                    if data['promocodeexpiry'] < data['tripdate']:
                        return "Oops! The promo code " + code + " had crossed its expiry date before you took the trip!"
                    if data['triptime'] <= data['timefrom'] or data['timeto'] <= data['triptime']:
                        return "Unfortunately, the promo code " + code + " is only available from " + data['timefrom'] + \
                               " to " + data['timeto']
                    if data['tripcity'] not in data['promocodelocations']:
                        return "Unfortunately, the promo code " + code + " is not available in " + data['tripcity']
        return "Okay! Sorry about the hassle, I have gone ahead and applied the promo code " + code + " to your trip! :)"

    if intent == '1A_PromoCode':
        try:
            code = entities['promo_code']
            if not code:
                raise KeyError
        except KeyError:
            return "I'm really sorry - I could not catch the promo code you are trying to use, can you tell me the" \
                   " code again?"

        if data:
            if data['promocodeapplied'] is None or data['promocodeapplied'] == '':
                return "I just checked our system, and unfortunately it seems that you did not apply any promo code to this trip." \
                       "You can use this same promo code again for your next trip."
            else:
                if data['promocodeapplied'] != code:
                    return "It looks like that the promo code you entered was " + data['promocodeapplied'] + ". This" +\
                           " was successfully applied."
                elif data['promocodename'] != data['promocodeapplied']:
                    return "It looks like that the promo code you entered was " + data['promocodeapplied'] + ". This," +\
                           " unfortunately, is not a valid promo code."
                else:
                    if data['promocodeexpiry'] < data['tripdate']:
                        return "Oops! The promo code " + code + " had crossed its expiry date before you took the trip!"
                    if data['triptime'] <= data['timefrom'] or data['timeto'] <= data['triptime']:
                        return "Unfortunately, the promo code " + code + " is only available from " + data['timefrom'] + \
                               " to " + data['timeto']
                    if data['tripcity'] not in data['promocodelocations']:
                        return "Unfortunately, the promo code " + code + " is not available in " + data['tripcity']
        return "Okay! Sorry about the hassle, I have gone ahead and applied the promo code " + code + " to your trip! :)"


def promo_code_wasnt_entered(intent, entities, data, response_msgs):
    if intent in ['1B_PromoCodeWasntEntered', '1B_PromoCode', '1A_PromoCode']:

        reply = ''
        try:
            code = entities['promo_code']
            if not code:
                raise KeyError
        except KeyError:
            return 'Sure, let me assist you with this. Can you tell me the promo code you are trying to use?'

        try:
            friend_gave = entities['friend_gave']
            if not friend_gave:
                raise KeyError
        except KeyError:
            friend_gave = None

        try:
            phone_number = entities['phone-number']
            if not phone_number:
                raise KeyError
        except KeyError:
            phone_number = None

        if data:
            if data['promocodeapplied'] is None or data['promocodeapplied'] == '':
                reply += "I checked our system, and unfortunately, it seems like no promo code was applies to this trip."
            elif data['promocodeapplied'] != code:
                reply += "It looks like that the promo code you entered was " + data['promocodeapplied'] + ". This" +\
                           " was successfully applied."

            if data['promocodename'] != code:
                if friend_gave is None:
                    reply += " Can you tell me if this promo code came from any of your friends?"
                elif friend_gave == "yes":
                    if phone_number is None:
                        reply += " Can you give me your friend's registered phone number?"
                    else:
                        reply += " We would be looking into this promo code associated with your friends phone number " + phone_number
                else:
                    reply += " I am really sorry but this is not a valid promo code. I would suggested that you try UBER4FREE."
            else:
                if data['promocodeexpiry'] < data['tripdate']:
                    reply += "Oops! The promo code " + code + " crossed its expiry date before you took the trip!"
                elif data['triptime'] <= data['timefrom'] or data['timeto'] <= data['triptime']:
                    reply += "Unfortunately, the promo code " + code + " is only available from " + data['timefrom'] + \
                            " to " + data['timeto']
                elif data['tripcity'] not in data['promocodelocations']:
                    reply += "Unfortunately, the promo code " + code + " is not available in " + data['tripcity']
                else:
                    reply += " Sorry about the hassle, I have gone ahead and applied the promo code " + code + " to your trip! :)"
            if reply:
                return reply
        return "Okay! Sorry about the hassle, I have gone ahead and applied the promo code " + code + " to your trip! :)"

    if intent == '1B_PromoCodeCameFromFriend':
        try:
            code = entities['promo_code']
            if not code:
                raise KeyError
        except KeyError:
            return 'Sure, I can help with that. Can you tell me the promo code you are trying to use?'
        return "To assist you better, can you share your friend's phone number?"

    if intent in ['1B_FriendsPhoneNumber', '1B_PromoCodeWasntEnteredFriendPhone']:
        try:
            code = entities['promo_code']
            phone_number = entities['phone-number']
            if not code:
                raise KeyError
        except KeyError:
            return 'I can help you with that. Can you tell me the promo code you are trying to use?'
        return "Thanks, we would be looking into this promo code associated with the phone number " + phone_number

    if intent == '1B_DontHaveFriendsNumber':
        try:
            code = entities['promo_code']
            if not code:
                raise KeyError
        except KeyError:
            return 'Let me assist you with that. Can you tell me the promo code you are trying to use?'
        return "No problem. In that case, I will escalate this to the concerned team with the details you have " \
               "provided. You will surely hear from us within 24 hours."

    if intent == '1B_PromoCodeDidntCameFromFriend':
        try:
            code = entities['promo_code']
            if not code:
                raise KeyError
        except KeyError:
            return 'Let me lend you a hand with that. Can you tell me the promo code you are trying to use?'
        return "In that case, I am really sorry but this promo code is not a valid promo code. I would suggested that you try UBER4FREE."

    if intent == '1B_PromoCodeWasntEnteredFriendGave':
        try:
            code = entities['promo_code']
            if not code:
                raise KeyError
        except KeyError:
            return 'Sure, can you tell me the promo code you are trying to use?'
        return "Can you also share your friend's registered phone number?"


def issue_with_pickup(intent, entities, data, response_msgs):

    if intent == '2A_IssueWithPickup':
        try:
            code = entities['duration']
            if not code:
                raise KeyError
        except KeyError:
            return "I am really sorry to hear that. To assist you better, can you tell me if this was a scheduled ride?"
        return "I am really sorry to hear that your ride is " + str(code['amount']) + ' ' + code['unit'] + "late. " \
                "Was this a scheduled ride?"

    if intent == "2A_ScheduledRide":
        return "Thanks for the information, we are looking into this at highest priority and will get back to you" \
               " soon. We may match you with another driver if required. I understand that your time" \
               " is valuable and that Uber should always be a hassle-free and seamless experience. We will certainly" \
               " ensure that your upcoming ride goes smoothly. Anything else I can help you with?"

    if intent == '2A_NotScheduledRide':
        if data:
            if (datetime.now() + timedelta(minutes=int(data['remainingeta'])) - (datetime.strptime(data['tripacceptedtime'], "%H:%M") + timedelta(minutes=int(data['eta'])))).seconds/60 > 5:
                return "Yes, the driver is more than 5 minutes behind the provided ETA. I understand that would be" \
                       " frustrating. You can cancel the ride request without incurring a cancellation fee. Please " \
                       "book another ride for your trip."
            else:
                return "Looks like driver is not running late and should arrive at your pickup location in " \
                       "" + str(data['remainingeta']) + ' mins'
        return "Unfortunately, we dont seem to have the data available for the expected ETA. I apologise for the" \
               " inconvenience - our systems are facing technical trouble. I request you to cancel this trip " \
               "and book another one."


def driver_refused_destination(intent, entities, data, response_msgs):
    if intent == '2B_DriverRefusedDestination':
        return "Hey, sorry to hear about that. We'd suggest you to book another ride while I try to solve this" \
               " problem for you. We understand your time is important and we'll revert the cancellation charges" \
               " if any :). To assist you with the issue, can you please share what destination you had requested?"

    if intent in ["2B_RequestedDestination", '2B_DriverRefusedDestinationGiven', '2B_DriverRefusedReasonDestinationGiven']:
        try:
            code = entities['address']
            if not code:
                raise KeyError
        except KeyError:
            return "Sorry, I could not catch the address, can you give me the detailed address of the destination" \
                   " you had requested?"

        try:
            code = entities['any']
            if not code:
                raise KeyError
        except KeyError:
            return "This kind of behavior is not tolerated. We have a certain set of quality and safety standards" \
                   " that we expect all of our driver-partners to meet, so it's important that we know of a concern" \
                   " like this so we can address it appropriately. Could you tell me what reason did the driver give" \
                   " for refusing your destination?"

        return "Thanks for the information, we will be taking immediate appropriate action. I have raised the" \
               " issue with the concerned team with the information - Address: " + entities['address'] + ", reason: " \
               + entities['any']

    if intent == "2B_Reason":
        return "Thanks for the information, we will be taking immediate appropriate action. I have raised the" \
               " issue with the concerned team with the information - Address: " + entities['address'] + ", reason: " \
               + entities['any']

    if intent == '2B_DriverRefusedReasonGiven':
        try:
            code = entities['any']
            if not code:
                raise KeyError
        except KeyError:
            return "I could not catch that, can you repeat that?"
        return "Can you tell me what was your destination for this trip ?"


def driver_asked_cash_payment(intent, entities, data, response_msgs):
    if intent == '2C_DriverAskedCashPayment':
        if data:
            if data['paymentmethod'] == 'Cash':
                return "I have just checked and it appears that the payment method selected for this trip was cash. Can you tell me how much cash driver took"
            else:
                return "Can you tell me how much did the driver took in cash ?"
        return "I am facing some difficulty in finding out the payment method selected for this trip, I have noted down the issue and out team would be looking into this"

    if intent == '2C_CashDriverTook':
        try:
            code = entities['unit-currency']
            if not code:
                raise KeyError
        except KeyError:
            return "I could not catch the amount driver took in cash, can you repeat that?"

        if data['paymentmethod'] == 'Cash' and int(code) == int(data['actualcharge']):
            return "The mode of payment was cash and driver partner has take then right amount in cash"
        elif data['paymentmethod'] == 'Cash' and int(code) != int(data['actualcharge']):
            return "It looks like driver took " + str(int(code) - int(data['actualcharge'])) + " extra. I have initiated refind for the same amount"
        else:
            return "I have initiated the refund process and your account would be credited with " + str(float(entities['unit-currency']))


def did_not_take_this_trip(intent, entities, data, response_msgs):
    if intent == '3A_DidNotTakeThisTrip':
        return "Hey, we get a lot of queries like this and most of the time its either a family member, co-worker or a friend who has access to your uber account taking the trip. I would request you to check once. Thanks :)"

    if intent == "3A_CustomerChecking":
        return "Sure, no problem, take your time"

    if intent == "3A_FamilyMemberTookTrip":
        return "No problem, happens all the time :)"

    if intent == "3A_FamilyMemberDidNotTrip":
        return "This trip was from " + data['startaddress'] + " to " + data['endaddress'] + " .If this trip's pickup location or destination is familiar, it's possible someone used your account or your phone to ride with Uber."

    if intent == "3A_LocationsLooksFamiliar":
        return "No problem, such confusions are inevitable"

    if intent in ["3A_LocationsDontLookFamiliar", '3A_DidNotTakeThisTripCustomerSure']:
        return "No problem, I have initiated the refund proccess. It's also a good idea to regularly update your Uber account password. Visit t.uber.com/forgotpassword to update your password anytime."


def fare_different_for_same_route(intent, entities, data, response_msgs):
    if intent == '3B_FareDifferentSameRoute':
        return "When you enter your pickup and drop off locations for your trip, we use dynamic pricing to calculate the fare you see in-app before you request. This fare takes into account the higher rates that go into effect when there's unusually high demand on the Uber platform. If you're seeing a different fare for a trip that you took previously, it's due to this dynamic pricing that changes along with current supply and demand.\n\nOur goal is to provide certainty when presenting your fare to you before you confirm your trip request, so you can feel comfortable making your travel choices."


def fare_not_reflect_upfront_price(intent, entities, data, response_msgs):
    if intent == '3C_FareDoesntReflectUpfrontPrice':
        if haversine(float(data['endlat']),float(data['endlng']),float(data['actualendlat']),float(data['actualendlng'])) > 3:
            return "It seems that the original destination has been changed from " + data['endaddress'] + ". The upfront fares are based on the exact pickup and drop off locations that you input, so when that trip is changed, our system switches to charging based on the time and distance of the actual trip instead, using the rates that apply to the vehicle option you selected. "
        elif float(data['actualduration']) - float(data['calculatedduration']) > 10:
            return "Did you make any extra stops on your trip?"
        elif float(data['actualcharge']) != float(data['upfrontprice']):
            return "Seems like there was some technical glitch with the system. We have to face it from time to time. I have initiated the refund process and " + str(float(data['actualcharge']) - float(data['upfrontprice'])) + " would be refunded to your account. Sorry for the inconvenience"

    if intent == '3C_ExtraStopsMade':
        return "Extra stops can result in changing the fare to be charged based on time and distance of the trip taken. This helps ensure that your driver is fairly compensated for the trip taken."

    if intent == '3C_ExtraStopsNotMade':
        return "Seems like there was some technical glitch with the system. We have to face it from time to time. I have initiated the refund process and " + str(float(data['actualcharge']) - float(data['upfrontprice'])) + " would be refunded to your account. Sorry for the inconvenience"

    if intent == '3C_DoesntReflectUpfrontPriceNoExtraStops':
        if haversine(float(data['endlat']), float(data['endlng']), float(data['actualendlat']),float(data['actualendlng'])) > 3:
            return "It seems that the original destination has been changed from " + data['endaddress'] + ". The upfront fares are based on the exact pickup and drop off locations that you input, so when that trip is changed, our system switches to charging based on the time and distance of the actual trip instead, using the rates that apply to the vehicle option you selected. "
        elif float(data['actualcharge']) != float(data['upfrontprice']):
            return "Seems like there was some technical glitch with the system. We have to face it from time to time. I have initiated the refund process and " + str(float(data['actualcharge']) - float(data['upfrontprice'])) + " would be refunded to your account. Sorry for the inconvenience"


def business_logic(intent, entities, data, response_msgs):
    if intent in ['1A_PromoCodeDidntWork']:
        return promo_code_didnt_work(intent, entities, data)
    if intent in ['1B_PromoCodeWasntEntered', '1B_PromoCodeCameFromFriend', '1B_FriendsPhoneNumber',
                  '1B_DontHaveFriendsNumber', '1B_PromoCodeDidntCameFromFriend', '1B_PromoCodeWasntEnteredFriendGave'
                  , '1B_PromoCodeWasntEnteredFriendPhone', '1B_PromoCode', '1A_PromoCode']:
        return promo_code_wasnt_entered(intent, entities, data, response_msgs)
    if intent in ['2A_IssueWithPickup', ' 2A_ScheduledRide', '2A_NotScheduledRide']:
        return issue_with_pickup(intent, entities, data, response_msgs)
    if intent in ['2B_DriverRefusedDestination', '2B_RequestedDestination', '2B_Reason', '2B_DriverRefusedDestinationGiven'
                  , '2B_DriverRefusedReasonGiven', '2B_DriverRefusedReasonDestinationGiven']:
        return driver_refused_destination(intent, entities, data, response_msgs)
    if intent in ['2C_DriverAskedCashPayment', '2C_CashDriverTook']:
        return driver_asked_cash_payment(intent, entities, data, response_msgs)
    if intent in ['3A_DidNotTakeThisTrip', '3A_CustomerChecking', '3A_FamilyMemberTookTrip',
                  '3A_FamilyMemberDidNotTrip', '3A_LocationsLooksFamiliar', '3A_LocationsDontLookFamiliar',
                  '3A_DidNotTakeThisTripCustomerSure']:
        return did_not_take_this_trip(intent, entities, data, response_msgs)
    if intent in ['3B_FareDifferentSameRoute']:
        return fare_different_for_same_route(intent, entities, data, response_msgs)
    if intent in ['3C_FareDoesntReflectUpfrontPrice', '3C_ExtraStopsMade', '3C_ExtraStopsNotMade'
                  , '3C_DoesntReflectUpfrontPriceNoExtraStops']:
        return fare_not_reflect_upfront_price(intent, entities, data, response_msgs)
