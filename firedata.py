import csv
from sqlalchemy import DATE, INTEGER, NUMERIC, TIMESTAMP, Column, MetaData, PrimaryKeyConstraint, create_engine, Table, text
from datetime import datetime

class FiresData:
    """
    class for all fires data from https://firms.modaps.eosdis.nasa.gov/active_fire/#firms-txt 
    and all methods
    """

    def __init__(self):
        """initialize metadata object for db"""
        self.engine = create_engine("sqlite+pysqlite:///firedata.db", echo=True, future=True)
        # set metadata object for all data
        self.metadata_obj = MetaData(bind=self.engine)
        # include all existind db's
        self.metadata_obj.reflect()

        # data used for fires charts
        self.firesdatatypes = ['lat', 'lon', 'date', 'frp']

    def get_data_from_csv(self, areaname, filepath):
        """open csv file and create table for firesdat with given name"""
        if areaname in self.metadata_obj.tables:
            print(f"Table '{areaname}' already exsists. Rename or delete'")
            return False
        
        # create table
        self._create_firetable(areaname)

        # read date from csv
        with open(filepath) as f:
                self._reader = csv.reader(f)
                self._header_row = next(self._reader)

                # define column numbers for datatype in csv
                self._define_csv_col_number()

                # prepare to insert rows in db
                with self.engine.connect() as conn:
                    # going through CVS line by line, send data to db table
                    for row in self._reader:
                        self._get_csv_line_for_query(row)

                        # insert row for current date
                        ins = self.metadata_obj.tables[areaname].insert().values(
                            cur_date = self._date,
                            latitude = self._lat,
                            longitude = self._lon,
                            frp = self._frp
                        )
                        conn.execute(ins)
                
                    # commit inserts
                    conn.commit()

    def _create_firetable(self, areaname):
            """create table in db for area with given name"""
            Table(
                areaname,
                self.metadata_obj, 
                Column('id', INTEGER, primary_key=True) ,
                Column('cur_date', DATE),
                Column('latitude', NUMERIC(7.5)),
                Column('longitude', NUMERIC(7.5)),
                Column('frp', NUMERIC(4.2))
            )
            self.metadata_obj.create_all(self.engine)

    def _define_csv_col_number(self):
        """define which column in csv corresponds to fires datatype"""
        # dict to store result - key: datatype, value: column number in csv
        self._data_columns = {
            'lat': '',
            'lon': '',
            'date': '',
            'frp': '',
        }
        # fill in the doct from header in csv
        for col_num in range(len(self._header_row)):
            if self._header_row[col_num] == 'acq_date':
                self._data_columns['date'] = col_num
            elif self._header_row[col_num] == 'latitude':
                self._data_columns['lat'] = col_num
            elif self._header_row[col_num] == 'longitude':
                self._data_columns['lon'] = col_num
            elif self._header_row[col_num] == 'frp':
                self._data_columns['frp'] = col_num

    def _get_csv_line_for_query(self, row):
        """read the csv line and prepare variables for `query`"""
        self._date = datetime.strptime(row[self._data_columns['date']], "%Y-%m-%d")
        self._lat = float(row[self._data_columns['lat']])
        self._lon = float(row[self._data_columns['lon']])
        self._frp = float(row[self._data_columns['frp']])

    def export_frp_data(self, arename):
        """get data from table in db and prepare list with lon, lat, frp"""

        query = f"SELECT latitude, longitude, frp FROM {arename};"
        firedata = {
            'lat': [],
            'lon': [],
            'frp': []
        }
        with self.engine.connect() as conn:
            for row in conn.execute(text(query)):
                firedata['lat'].append(row[0])
                firedata['lon'].append(row[1])
                firedata['frp'].append(row[2])

        return firedata
