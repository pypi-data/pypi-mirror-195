from abc import abstractmethod
from dataclasses import dataclass
from .models import CustomerExtension, CustomerExtensionExtended, ValidatedTemplate
from .models import Departure
from .models import Route
from .models import Selection
from typing import List, Iterator, Optional
from datetime import datetime
from .methods import calc_departures, calc_route_departure, recalculate_lead_time


def MakeRoute(data: ValidatedTemplate) -> Iterator[Route]:
    data = data.copy()

    tostr = lambda x: str(x) if x != None else ''

    yield Route.construct(
        ROUT=data.ROUT,
        RUTP=6,
        TX40=tostr(data.EDEL)\
            + '_' + tostr(data.EDEU)\
            + '_' + tostr(data.MODL),
        TX15=tostr(data.EDEL)\
            + '_' + tostr(data.EDEU)\
            + '_' + tostr(data.MODL),
        RESP=data.RRSP,
        SDES=data.EDEL,
        DLMC=1,
        DLAC=1,
        TSID=data.TSID
    )



def MakeDeparture(data: ValidatedTemplate) -> Iterator[Departure]:
    data = data.copy()

    list_of_departure_days = [data.DDOW]\
        if not data.ADOW\
        else calc_departures(data.DDOW, data.ARDY)
     
    for DDOW in list_of_departure_days:
        RODN = calc_route_departure(DDOW, data.ARDY) if not data.RODN else data.RODN
        ARDY = recalculate_lead_time(DDOW, data.ARDY) if data.ADOW else data.ARDY
        ARDY = int(data.ARDX) if data.ARDX else ARDY
    
        yield Departure.construct(
            WWROUT = data.ROUT,
            WWRODN = RODN,
            WRRESP = data.DRSP,
            WRFWNO = data.FWNO,
            WRTRCA = data.TRCA,
            WRMODL = data.MODL,
            WRLILD = data.LILD,
            WRSILD = data.SILD,
            WRLILH = data.LILH,
            WRLILM = data.LILM,
            WRSILH = data.SILH,
            WRSILM = data.SILM,
            WEFWLD = data.FWLD,
            WEFWLH = data.FWLH,
            WEFWLM = data.FWLM,
            WRDDOW = DDOW,
            WRDETH = data.DETH,
            WRDETM = data.DETM,
            WRVFDT = datetime.now().strftime('%y%m%d'),
            WRARDY = ARDY,
            WRARHH = data.ARHH,
            WRARMM = data.ARMM
        )


def MakeSelection(data: ValidatedTemplate) -> Iterator[Selection]:
    data = data.copy()
    yield Selection.construct(
        EDES = data.EDEL,
        PREX = ' 6',  # with preceding space
        OBV1 = data.EDEU,
        OBV2 = data.MODL,
        OBV3 = '',
        OBV4 = '',
        ROUT = data.ROUT,
        RODN = data.RODN,
        SEFB = '4',
        DDOW = data.DDOW,
        LOLD = data.ARDY\
            if data.ARDX\
            else None
    )



def MakeCustomerExtension(data: ValidatedTemplate) -> Iterator[CustomerExtension]:
    data = data.copy()

    list_of_departure_days = [data.DDOW]\
    if not data.ADOW\
    else calc_departures(data.DDOW, data.ARDY)

    for DDOW in list_of_departure_days:
        RODN = calc_route_departure(DDOW, data.ARDY) if not data.RODN else data.RODN

    yield CustomerExtension.construct(
        FILE='DROUDI',
        PK01=data.ROUT,
        PK02=RODN,
        A030=data.EDEU,
        N096=data.PCUD if data.PCUD else None,
        N196=data.PCUH if data.PCUH else None,
        N296=data.PCUM if data.PCUM else None
    )

    if data.CUSD:
        yield CustomerExtension.construct(
                FILE='DROUTE',
                PK01=data.ROUT
            )


def MakeCustomerExtensionExtended(data: ValidatedTemplate) -> Iterator[CustomerExtensionExtended]:
    data = data.copy()

    if data.CUSD:
        yield CustomerExtensionExtended.construct(
                FILE='DROUTE',
                PK01=data.ROUT,
                CHB1=data.CUSD
            )
        
        
def MakeTemplate(
    route: Route,
    departures: List[Departure],
    selection: Selection,
    cugex: Optional[CustomerExtension] = None,
    cugexex: Optional[CustomerExtensionExtended] = None
    ):

    return ValidatedTemplate(
        ROUT=route.ROUT,
        EDEL=route.SDES,
        EDEU=selection.EDES if selection else '',
        TSID=route.TSID,
        MODL=departures[0].WRMODL if departures else '',
        RODN='',
        DDOW=selection.DDOW,
        FWNO=departures[0].WRFWNO if departures else '',
        ARDY=min([d.WRARDY for d in departures if d.WRARDY]) if departures else 0,
        ARDX=selection.LOLD,
        TRCA=selection.TRCA,
        LILD=departures[0].WRLILD,
        LILH=departures[0].WRLILH,
        LILM=departures[0].WRLILM,
        SILD=departures[0].WRSILD,
        SILH=departures[0].WRSILH,
        SILM=departures[0].WRSILM,
        FWLD=departures[0].WEFWLD,
        FWLH=departures[0].WEFWLH,
        FWLM=departures[0].WEFWLM,
        PCUD=cugex.N096 if cugex else None,
        PCUH=cugex.N196 if cugex else None,
        PCUM=cugex.N296 if cugex else None,
        DETH=departures[0].WRDETH,
        DETM=departures[0].WRDETM,
        ARHH=departures[0].WRARHH,
        ARMM=departures[0].WRARMM,
        RRSP=route.RESP,
        DRSP=departures[0].WRRESP,
        CUSD=cugexex.CHB1 if cugexex else 0,
        ADOW=all([int(d.WWRODN) in [1, 2, 3, 4] for d in departures])
    )