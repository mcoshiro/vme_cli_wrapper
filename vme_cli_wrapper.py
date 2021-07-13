#!/bin/env python
import os
import sys
import multiprocessing
import glob
import subprocess
import argparse
import time
import binascii
#from time import time

#options

#OSU
#odmb_slot = '07'
#cfeb_slot = '02'
#vme_mac_address = '02:00:00:00:00:02'
#eth_name = 'eth1'
#schar_port = '1'

#UCSB
odmb_slot = '19'
ccb_slot = '13'
cfeb_slot = '0040' #1,2,4,8...,40
vme_mac_address = '02:00:00:00:00:4A'
#eth_name = 'p5p2' #higgs
eth_name = 'ens3f1' #wimp
schar_port = '2'
is_verbose_default = True

def run_vme_command(r_w,vme_cmd,vme_data='0000',vme_slot=odmb_slot,verbose=is_verbose_default):
  s = ''
  time.sleep(1.0)
  if (verbose):
    print(r_w+' '+vme_cmd+' '+vme_data)
  if (r_w=='r'):
    s = subprocess.check_output(['./vme_cli/vme_cli','--vcc_mac_address',vme_mac_address,'--schar_port',schar_port,'--eth_name',eth_name,'--vme_write_read',r_w,'--vme_command',vme_cmd,'--vme_slot',vme_slot])
    if (verbose):
      print(s.split('\n')[4].split()[2])
  else:
    s = subprocess.check_output(['./vme_cli/vme_cli','--vcc_mac_address',vme_mac_address,'--schar_port',schar_port,'--eth_name',eth_name,'--vme_write_read',r_w,'--vme_command',vme_cmd,'--vme_slot',vme_slot,'--vme_data',vme_data])
  return s.split('\n')[4].split()[2]

def vme_left_pad(hex_str):
  if (len(hex_str) > 4):
    print('ERROR: string too long to pad')
    Exit()
  while (len(hex_str) < 4):
    hex_str = '0' + hex_str
  return hex_str

if __name__=='__main__':
  parser = argparse.ArgumentParser(description='Wrapper for vme_cli',formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument('-t','--test', default='odmbid', choices=['dmbid','usercmds','discretelogic','odmbid','dcfebid','xdcfebid','xdcfebjtag','prom'],help='Sets VME commands to be run.')
  parser.add_argument('-c','--cfeb', default=cfeb_slot, choices=['0001','0002','0004','0008','0010','0020','0040'],help='Sets cfeb slot.')
  args = vars(parser.parse_args())
  test_name = args['test']
  cfeb_slot = args['cfeb']
  if test_name=='dmbid':
    run_vme_command('w','293C','3C8')
    run_vme_command('w','2F04','0000')
    out1 = run_vme_command('r','2014')
    run_vme_command('w','2F08','0000')
    out2 = run_vme_command('r','2014')
    print(out1)
    print(out2)
    print('Test complete.')
  elif test_name=='odmbid':
    result = run_vme_command('r','4100')
    print(result)
    print('Test complete.')
  elif test_name=='dcfebid':
    result = ''
    run_vme_command('w','1018','0000')
    run_vme_command('w','1020',cfeb_slot)
    run_vme_command('w','191C','03C8')
    run_vme_command('w','1F04','0000')
    result = run_vme_command('r','1014')+result
    run_vme_command('w','1F08','0000')
    result = run_vme_command('r','1014')+result
    print(result)
    print('Test complete.')
  elif test_name=='xdcfebid':
    result = ''
    run_vme_command('w','1018','0000')
    run_vme_command('w','1020',cfeb_slot)
    run_vme_command('w','1934','03C8')
    run_vme_command('w','1F30','FFFF')
    run_vme_command('w','1F30','FFFF')
    run_vme_command('w','1F30','FFFF')
    run_vme_command('w','1338','000F')
    run_vme_command('w','1F04','0000')
    result = run_vme_command('r','1014')+result
    run_vme_command('w','1F08','0000')
    result = run_vme_command('r','1014')+result
    print(result)
    print('Test complete.')
  elif test_name=='xdcfebjtag':
    result=''
    run_vme_command('w','1018','0000')
    run_vme_command('w','1020',cfeb_slot)
    run_vme_command('w','1934','03C2')
    run_vme_command('w','1F30','FFFF')
    run_vme_command('w','1F30','FFFF')
    run_vme_command('w','1F30','FFFF')
    run_vme_command('w','1338','000F')
    run_vme_command('w','1704','000C')
    run_vme_command('w','1308','0000')
    run_vme_command('w','1934','03C3')
    run_vme_command('w','1F30','FFFF')
    run_vme_command('w','1F30','FFFF')
    run_vme_command('w','1F30','FFFF')
    run_vme_command('w','1338','000F')
    run_vme_command('w','1B04','0123')
    run_vme_command('w','1308','0000')
    run_vme_command('w','1B04','0456')
    run_vme_command('w','1308','0000')
    result=result+run_vme_command('r','1014')
    run_vme_command('w','1B04','0789')
    run_vme_command('w','1308','0000')
    result=result+run_vme_command('r','1014')
    run_vme_command('w','1B04','0ABC')
    run_vme_command('w','1308','0000')
    result=result+run_vme_command('r','1014')
    run_vme_command('w','1B04','0DEF')
    run_vme_command('w','1308','0000')
    result=result+run_vme_command('r','1014')
    print(result)
    print('Test complete.')
  elif test_name=='usercmds':
    quit = False
    while not quit:
      user_input = raw_input('')
      if user_input == 'exit':
        quit = True
        break
      split_user_input = user_input.split()
      if len(split_user_input) == 3:
        run_vme_command(split_user_input[0],split_user_input[1],split_user_input[2])
      elif len(split_user_input) == 4:
        run_vme_command(split_user_input[0],split_user_input[1],split_user_input[2],split_user_input[3])
      else:
        print('ERROR: user input wrong length')
    print('Test complete.')
  elif test_name=='discretelogic':
    ##V6 3C8 read user code
    ##dl_pattern = '111110110000020022231010' 
    ##V6 3C9 read ID code
    ##dl_pattern = '111110110020020022231010'
    ##KUS 09 read ID code
    #dl_pattern = '11111011002002011010'
    ##KUS 08 read user code
    ##dl_pattern = '11111011000002011010'
    #for char in dl_pattern:
    #  run_vme_command('w','FFFC','000'+char)
    #result = ''
    #for hex_digit in range(8):
    #  for command in range(8):
    #    if hex_digit==0:
    #      if command%2==1:
    #        result = run_vme_command('r','FFFC')+result
    #      elif command==0:
    #        run_vme_command('w','FFFC','0000')
    #      else:
    #        run_vme_command('w','FFFC','0002')
    #    elif hex_digit==1:
    #      if command%2==1:
    #        result = run_vme_command('r','FFFC')+result
    #      elif command==0:
    #        run_vme_command('w','FFFC','0002')
    #      else:
    #        run_vme_command('w','FFFC','0000')
    #    else:
    #      if command%2==1:
    #        result = run_vme_command('r','FFFC')+result
    #      else:
    #        run_vme_command('w','FFFC','0000')
    #print(result)
    #KUS 09 read ID code
    dl_pattern = '11111011002002011010'
    for char in dl_pattern:
      run_vme_command('w','FFFC','000'+char)
    result = ''
    for hex_digit in range(8):
      for command in range(8):
        if hex_digit==0:
          if command%2==1:
            result = run_vme_command('r','FFFC')+result
          elif command==0:
            run_vme_command('w','FFFC','0000')
          else:
            run_vme_command('w','FFFC','0002')
        elif hex_digit==1:
          if command%2==1:
            result = run_vme_command('r','FFFC')+result
          elif command==0:
            run_vme_command('w','FFFC','0002')
          else:
            run_vme_command('w','FFFC','0000')
        else:
          if command%2==1:
            result = run_vme_command('r','FFFC')+result
          else:
            run_vme_command('w','FFFC','0000')
    print(result)
    print(hex(int(result,2)))
    print('Test complete.')
  elif test_name == 'prom':
    #f = open('prom_write.bin','rb')
    #prom_write_contents = f.read()
    #print(binascii.hexlify(prom_write_contents))
    #f.close()
    f = open('prom_read.bin','wb')
    page_size = 0x80 #words, 0x100 bytes
    num_pages = 0xA
    page_idx = 0
    while page_idx < num_pages:
      addr = page_idx*0x100
      load_addr_command_first = vme_left_pad(hex(((addr >> 16) << 5) | 0x17)[2:])
      load_addr_command_second = vme_left_pad(hex(addr & 0xFFFF)[2:])
      read_page_command = vme_left_pad(hex(((page_size-1) << 5) | 0x04)[2:])
      run_vme_command('w','602c',load_addr_command_first)
      run_vme_command('w','602c',load_addr_command_second)
      run_vme_command('w','602c',read_page_command)
      #now read out readback FIFO
      word_idx = 0
      while word_idx < page_size:
        vme_out = run_vme_command('r','6030')
        f.write(binascii.unhexlify(vme_left_pad(vme_out.strip())))
        word_idx += 1
      page_idx += 1
    f.close()
  
