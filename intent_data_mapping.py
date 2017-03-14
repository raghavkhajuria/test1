INTENT_DATA_MAPPING = {
    '1A_PromoCodeDidntWork': [
        'promocodeapplied',
        'promocodename',
        'promocodeexpiry',
        'tripdate',
        'triptime',
        'timefrom',
        'timeto',
        'tripcity',
        'promocodelocations'
    ],
    '1B_PromoCodeWasntEntered': [
        'promocodeapplied',
        'promocodename',
        'promocodeexpiry',
        'tripdate',
        'triptime',
        'timefrom',
        'timeto',
        'tripcity',
        'promocodelocations'
    ],
    '2A_IssueWithPickup': [
        'remainingeta',
        'tripacceptedtime',
        'eta',
    ],
    '2C_DriverAskedCashPayment': [
        'paymentmethod',
        'upfrontprice'
    ],
    '3A_DidNotTakeThisTrip': [
        'startaddress',
        'endaddress'
    ],
    '3C_FareDoesntReflectUpfrontPrice': [
        'endlat',
        'endlng',
        'actualendlat',
        'actualendlng',
        'actualduration',
        'calculatedduration',
        'actualcharge',
        'upfrontprice'
    ]
}

INTENT_TICKET_MAPPING = {
    '1B': "Promo code is not working",
    '2A': "I had an issue with pickup",
    '2B': "My Driver Refused my destination",
    '2C': "My driver asked for cash payment",
    '3A': "I did not take this trip",
    '3B': "Why is my fare different for the same route?",
    '3C': "My fare doesn't reflect the upfront price I was shown",
}
