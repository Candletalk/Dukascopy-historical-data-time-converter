#! /bin/python


# Converts a Dukascopy historical quote file line by line from
# quote time in GMT time zone to quote time in MET/MEST time zone.
#
# usage: Dukascopy_time_converter.py <input.csv> ...
#
# will create output files named <input.converted.csv>
# in same directory as input files.
#
#
# Needs package pytz, which can be installed with the command:
#
# easy_install --upgrade pytz
# or perhaps some similiar as:
# easy_install-2.7 --upgrade pytz


import csv
import datetime
import os.path
import pytz
import sys


class Config:
  """Script configuration data"""
  datetime_format = '%d.%m.%Y %H:%M:%S.%f'
  local_time_zone = pytz.timezone('Europe/Berlin')
  out_file_infix  = '.converted'


def main():
  """top level entry function"""

  # function definitions for details of work

  def convert_file(in_file_name):
    """do conversion for one file"""

    def get_out_file_name(in_file_name):
      """derive output file name from input file name"""
      return Config.out_file_infix.join(os.path.splitext(in_file_name))

    def convert_data_line(line):
      """convert one data line"""
      line[0] = convert_utc_to_local_time_zone(line[0])
      return line

    csv_filter(
        in_file_name
      , get_out_file_name(in_file_name)
      , lambda line : line   # simple copy of header line
      , convert_data_line
      )

  # loop over all files given as arguments

  iterate_argv(convert_file)


# general utility functions

def iterate_argv(function):
  """call a function for each argv item"""
  for in_file_name in sys.argv[1:]:
    function(in_file_name)

def csv_filter(in_file_name, out_file_name, header_function, data_function):
  """apply two functions to a CSV file, creating a new CSV file

     first function transforms the header line
     second function is appliad to every data row (lines 2 until end)
  """
  with   open(in_file_name      ) as in_file :
    with open(out_file_name, 'w') as out_file:
      csv_reader = csv.reader(in_file )
      csv_writer = csv.writer(out_file)

      csv_writer.writerow(header_function(csv_reader.next()))
      for line in csv_reader:   # reader is now on first data line
        csv_writer.writerow(data_function(line))

def convert_utc_to_local_time_zone(string):
  """converts a datetime string in UTC time zone to local time zone"""
  utc   = datetime.datetime.strptime(string, Config.datetime_format)
  utc   = utc.replace(tzinfo = pytz.utc)
  local = utc.astimezone(Config.local_time_zone)
  local = Config.local_time_zone.normalize(local)
  local = local.strftime(Config.datetime_format)
  return local[0:-3]


main()
