"""app to run and display fires fata on the map"""

from drow_map import draw_fire_map
from firedata import FiresData

fd = FiresData()

fd.get_data_from_csv('europe7', 'data/MODIS_C6_1_Europe_7d.csv')

euro_fires = fd.export_frp_data('europe7')

draw_fire_map('Europe fires last 7 days', euro_fires['dates'], euro_fires['lon'], euro_fires['lat'], euro_fires['frp'])