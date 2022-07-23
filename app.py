from firedata import FiresData

fd = FiresData()

# fd.get_data_from_csv('global', 'data/MODIS_C6_1_Global_7d.csv')
fd.get_data_from_csv('europe24h', 'data/MODIS_C6_1_Europe_24h.csv')
