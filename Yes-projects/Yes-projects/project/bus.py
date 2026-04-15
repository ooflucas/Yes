import requests
import json
from pathlib import Path
from datetime import datetime, timezone, timedelta
station = 'yl556'.upper()
direction = None
route = '76K'
service_type = 1
stop_id = None
target_tz = timezone(timedelta(hours=8))
current_time = datetime.fromisoformat((datetime.now(target_tz)).isoformat(timespec = 'minutes'))
stop_list = ((requests.get('https://data.etabus.gov.hk/v1/transport/kmb/stop')).json()).get('data')
inbound_data = (((requests.get(f'https://data.etabus.gov.hk/v1/transport/kmb/route/{route}/inbound/1')).json()).get('data')).get('route')
outbound_data = (((requests.get(f'https://data.etabus.gov.hk/v1/transport/kmb/route/{route}/outbound/1')).json()).get('data')).get('route')
current_dir = Path(__file__).parent
file_path = current_dir / "stop_data.json"
with open(file_path, 'r', encoding='utf-8') as f:
        stop_data = json.load(f)
def traceback(stop_data: dict, route: str, target_id: str, eta_data: dict, delta: int):
    stop_data = stop_data.get(f'{route}_1')
    for seq in stop_data:
        hex_id = (stop_data.get(f'{seq}').get('hex_id'))
        if hex_id == target_id:
            prev_hex_id = stop_data.get(f'{int(seq) - 1}').get('hex_id')
            print(prev_hex_id)
            print(hex_id)
def calculate_speed(stop_data: dict, route: str, target_id: str, delta: int):
    if delta  <= 0:
        print('bus arriving/departed')
        return
    route_key = f'{route}_1'
    stops = stop_data.get(route_key, {})
    prev_stop = None
    for seq in sorted(stops.keys(), key=int):
        current_stop = stops[seq]
        current_id = current_stop.get('hex_id') 
        if current_id == target_id:
            if prev_stop:
                dist_gap = round(current_stop['dist'] - prev_stop['dist'])
                print(f'distance from last stop: {dist_gap} M')
                dist_gap = dist_gap / 1000
                delta = delta / 60
                speed = dist_gap / delta
                print(f'bus speed: {speed}')
            else:
                print("This is the first stop (no previous stop available).")
            return 
        prev_stop = current_stop
if route in outbound_data:
    direction = 'outbound'
elif route in inbound_data:
    direction = 'inbound'
for stop in stop_list:
    if station in stop.get('name_en'):
        stop = stop
        stop_id = stop.get('stop')
        print(f"station: {stop.get('name_tc')}")
eta = ((requests.get(f'https://data.etabus.gov.hk/v1/transport/kmb/stop-eta/{stop_id}')).json()).get('data')
ran = False
first_ran = False
for bus_eta in eta:
    if route in bus_eta.get('route') and bus_eta.get('service_type') == service_type:
        if not ran:
            print(f"route: {bus_eta.get('route')} {bus_eta.get('dest_tc')}")
            ran = True
        bus_etas = datetime.fromisoformat(bus_eta.get('eta'))
        delta = bus_etas - current_time
        eta_delta = round((delta.total_seconds())/60)
        print(f'\neta: {eta_delta} mintes')
        calculate_speed(stop_data, route, stop_id, eta_delta)
        if eta_delta <= 1:
            print('Arriving\n')
        elif eta_delta < 0:
            print('Departed\n')
traceback(stop_data, route, stop_id, eta, delta)
