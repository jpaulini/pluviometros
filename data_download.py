from ftplib import FTP
from datetime import tzinfo, timedelta, datetime, date
import glob
import gzip

#ftp://disc2.nascom.nasa.gov/data/TRMM/Gridded/3B42_V6/201105/
#3B42.110501.00z.6.precipitation.bin
def download_bin_files(date_tuple):
   yy,mm,dd=date_tuple
   hours = range(0,24,3)
   file_names=[]

   for hh in hours:
       #3B42.110501.00z.6.precipitation.bin
       #3B42.110501.00z.6.relativeError.bin
       name='3B42.%02d%02d%02d.%02dz.6.precipitation.bin' % (yy-2000,mm,dd,hh)
       # NASA file system structure es <year>\<ordinal number of day>\file
       day_of_year=day_number(datetime(yy,mm,dd,hh,0,0,0,tzinfo=TZ() ))
       file_names.append(  name )

   ftp = FTP('disc2.nascom.nasa.gov')   # connect to host, default port
   ftp.login()                                      # user anonymous, passwd anonymous@
   ftp.cwd("data/TRMM/Gridded/3B42_V6/%d%02d" % (yy, mm) )
   #ftp.retrlines('LIST')
   for file_name in file_names:
       print "Trying to retrieve file: " + file_name
       ftp.retrbinary('RETR ' + file_name, open(file_name, 'wb').write)
   ftp.quit()

class TZ(tzinfo):
   def utcoffset(self, dt): return timedelta(hours=-3)

def day_number(d):
       yday = d.toordinal() - date(d.year, 1, 1).toordinal() + 1
       return yday

#ftp://disc2.nascom.nasa.gov/ftp/data/s4pa//TRMM_L3/TRMM_3B42//2011/151/3B42.110531.21.6A.HDF.Z
def download__HDF_files(date_tuple):
   yy,mm,dd=date_tuple
   hours = range(0,24,3)
   file_names=[]

   for hh in hours:
       name='3B42.%02d%02d%02d.%d.6A.HDF.Z' % (yy-2000,mm,dd,hh)
       # NASA file system structure es <year>\<ordinal number of day>\file
       day_of_year=day_number(datetime(yy,mm,dd,hh,0,0,0,tzinfo=TZ() ))

       # I don't know why, but the 0 file seems to be a day before day_of_year
       if hh==0:
           day_of_year-=1
       file_names.append( (day_of_year, name) )

   ftp = FTP('disc2.nascom.nasa.gov')   # connect to host, default port
   ftp.login()                                      # user anonymous, passwd anonymous@
   ftp.cwd("ftp//data//s4pa//TRMM_L3//TRMM_3B42//2011")
   #ftp.retrlines('LIST')

   for dir, file_name in file_names:
       print "Trying to retrieve file: " + str(dir) + "/" + file_name
       ftp.cwd(str(dir))
       ftp.retrbinary('RETR ' + file_name, open(file_name, 'wb').write)
       ftp.cwd("..")
   ftp.quit()

def uncompress_files():
   BLOCK_SIZE = 2**20
   filenames = glob.glob('*.fastq.gz')

   number_of_characters = number_of_lines = number_of_words = 0
##    for filename in filenames:
##        with gzip.open(filename) as f:
##            for block in iter(lambda: f.read(BLOCK_SIZE), ""):
##                number_of_characters += len(block)
##                number_of_lines += block.count('\n')
##                number_of_words += len(block.split())
##            print "%d %d %d %s" % (number_of_lines, number_of_words, number_of_characters, filename)

def getSatelliteInfo(dict_in):

#    base_name = '3B42RT.2011.06.15.00z'
   base_name = 'data\\3B42.110531.21.6A'

   infile = base_name + '.HDF'
   outfile = base_name + '.txt'

   # read the binary file
   try:
       inFile = open(infile, 'rb')
       data_string = inFile.read()
       inFile.close()
   except:
       print "error: File "+ infile +" not found"
       return


   # convert the binary string to a NumPy array
   precip = np.fromstring(data_string, np.float32)
   # byte-swap if you are working on a little-endian machine
   # your computer is almost certainly little-endian
   if sys.byteorder == 'little':
       precip = precip.byteswap()

   t=precip.reshape((480, 1440))
   n=0
   c=Coord.Coord()

   for i in dict_in:
       x,y=dict_in[i]
       print x,y ,c.fromLatLng(x,y),t[c.fromLatLng(x,y)]
       n+=1
       if n>15:
           break
   return 0

def getRainGaugesInfo():
   infile = "estaciones\\estaciones.inta"
   outfile = "estaciones-inta.txt"
   dict_out= {}

   # read the binary file
   try:
       inFile = open(infile,"rb")
       json_string = inFile.read()
       inFile.close()
   except:
       print("I/O Error: " )

   decoder= json.JSONDecoder()
   gauges=decoder.decode(json_string)
   for estacion in gauges["estaciones"]:
       dict_out[estacion["id_estacion"]]=(estacion["Latitud"],estacion["Longitud"])
   return dict_out

def save_numpy_matrix():
   # open the hdf file for reading
   hdf=SD.SD(FILE_NAME)
   # read the sds data
   sds=hdf.select(SDS_NAME)
   data=sds.get()
   print data.shape
   # turn [y,x] (HDF representation) data into [x,y] (numpy one)
   #data=data.reshape(data.shape[1],data.shape[0])
   data=data.reshape((400,1440))
   data.save(yy+mm+dd+SDS_NAME+"matrix")


def convert_to_csv(date_tuple):
   yy,mm,dd=date_tuple
   hours = range(0,24,3)
   file_names=[]

   lon=np.zeros((1440),dtype=float)
   lat=np.zeros((400),dtype=float)
   for i in range(1440):
       lon[i]=-179.875+0.25*i
   for j in range(400):
       lat[j]=-49.875+0.25*j

   outfile=open('3B42.%02d%02d%02d.6.precipitation' % (yy-2000,mm,dd) + ".csv","w+")
   outfile.write("date,lat,lon,precip\n")

   for hh in hours:
       #3B42.110501.00z.6.precipitation.bin
       #3B42.110501.00z.6.relativeError.bin
       base_name='3B42.%02d%02d%02d.%02dz.6.precipitation' % (yy-2000,mm,dd,hh)

       trmm_data = (np.fromfile ( base_name + ".bin", dtype=np.float32,count=400*1440).byteswap()).reshape((400,1440))
       for j in range(400):
           for i in range(1440):
               outfile.write( '%02d%02d%02d%02d,%.3f,%.3f,%f\n' % (yy, mm, dd, hh, lat[j], lon[i], trmm_data[j,i]))
   outfile.close()

if __name__ == '__main__':

   start_date=date(2011,5,2)
   end_date=date(2011,5,2)

# Este código es horrible, debería ser mas limplio con un while... creo..
   for i in range(day_number(start_date)-1, day_number(end_date)):
       d=date.fromordinal(date(start_date.year,1,1).toordinal() + i )
#        download_bin_files((d.year,d.month,d.day))
       convert_to_csv((d.year,d.month,d.day))
