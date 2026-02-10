import requests
import json
from datetime import datetime, timezone, timedelta

station = 'yl242'.upper()
direction = None
route = '68F'
service_type = 1

target_tz = timezone(timedelta(hours=8))
current_time = datetime.fromisoformat((datetime.now(target_tz)).isoformat(timespec = 'minutes'))

stop_list = ((requests.get('https://data.etabus.gov.hk/v1/transport/kmb/stop')).json()).get('data')

inbound_data = (((requests.get(f'https://data.etabus.gov.hk/v1/transport/kmb/route/{route}/inbound/1')).json()).get('data')).get('route')
outbound_data = (((requests.get(f'https://data.etabus.gov.hk/v1/transport/kmb/route/{route}/outbound/1')).json()).get('data')).get('route')

if route in outbound_data:
    direction = 'outbound'
elif route in inbound_data:
    direction = 'inbound'

for stop in stop_list:
    if station in stop.get('name_en'):
        stop = stop
        stop_id = stop.get('stop')
        print(f'station: {stop.get('name_tc')}')

eta = ((requests.get(f'https://data.etabus.gov.hk/v1/transport/kmb/stop-eta/{stop_id}')).json()).get('data')

ran = False
for bus_eta in eta:
    if route in bus_eta.get('route') and bus_eta.get('service_type') == service_type:
        if not ran:
            print(f'route: {bus_eta.get('route')} {bus_eta.get('dest_tc')}')
            ran = True
        bus_etas = datetime.fromisoformat(bus_eta.get('eta'))
        delta = bus_etas - current_time
        eta_delta = round((delta.total_seconds())/60)
        print(f'eta: {eta_delta} mintes')
        if eta_delta <= 1:
            print('Arriving\n')
        elif eta_delta < 0:
            print('Departed\n')