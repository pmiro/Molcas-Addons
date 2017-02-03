#Import libraries
import datetime
import os.path
import math
import sys

#Define consants
pi=3.14159265

#User defined variables
if int(len(sys.argv)) < 5:
  print('ERROR 1: Missing one or more of the required arguments (resolution, wide, type and spinorbit).')
  exit()

resolution=float(sys.argv[1])
wide=float(sys.argv[2])
type=str(sys.argv[3])
spinorbit=str(sys.argv[4])

#Define variables
files=[]
RASSI=[]
RASSISO=[]
RASSIindex=[]
RASSISOindex=[]
spectraRASSIenergy=[]
spectraRASSIoscil=[]
spectraRASSISOenergy=[]
spectraRASSISOoscil=[]

#Print program log
logfile = open('logfile.txt', 'w')
logfile.write('**********************************************\n')
logfile.write('*****	           DRAGON               *****\n')
logfile.write('*****                                    *****\n')
logfile.write('*****    Contact: pere.miro@gmail.com    *****\n')
logfile.write('**********************************************\n')
logfile.write('\n')
logfile.write('Date: '+str(datetime.date.today())+'\n')

#Read the paths of the Molcas files
input = open('input.txt', 'r')
for line in input:
    line=line.strip('\n')
    if line != '':
      files.append(line)
input.close()

#Read the Molcas outputs energies
for i in range(0,len(files)):
    check=(os.path.isfile(files[i]))
    if str(check) == 'False':
        print('ERROR 2: File '+str(files[i])+' not found.')
        exit()
    temp = open(str(files[i]),'r')
    for line in temp:
        if 'Dipole transition strengths' not in line:
          line = line.strip('\n')
          if 'RASSI State' in line:
              if 'SO-RASSI' not in line:
                templist = line.split()
                for j in range(0,len(templist)):
                    if templist[j] == 'energy:':
                      RASSI.append(str(templist[j+1]))
              if spinorbit.lower() == 'so':
                if 'SO-RASSI' in line:
                  templist = line.split()
                  for j in range(0,len(templist)):
                      if templist[j] == 'energy:':
                        RASSISO.append(str(templist[j+1]))

    temp.close()
    if i==0:
      RASSIindex.append(len(RASSI))
      preRASSI=len(RASSI)
      if spinorbit.lower() == 'so':
        RASSISOindex.append(len(RASSISO))
        preRASSISO=len(RASSISO)
    if i!=0:
      RASSIindex.append(int(len(RASSI))-int(preRASSI))
      preRASSI=len(RASSI)
      if spinorbit.lower() == 'so':
        RASSISOindex.append(int(len(RASSISO))-int(preRASSISO))
        preRASSISO=len(RASSISO)

#Read the Molcas outputs transitions
for i in range(0,len(files)):
    temp = open(str(files[i]),'r')
    for j in range(0,10000000):
        line = temp.readline()
        line = line.strip('\n')
        if 'RASSI State' in line:
            if 'SO-RASSI' not in line:
              n=0
            if 'SO-RASSI' in line:
              n=1
        if 'To  From     Osc. strength   Einstein coefficients' in line:
            if n==0:
              logfile.write('\n')
              logfile.write('RASSI FILE: '+str(files[i])+'\n')
              logfile.write('\n')
              logfile.write('From To EnergyFrom(a.u.) EnergyTo(a.u.) EnergyFromTo(a.u) EnergyFromTo(eV) Osc.Strength \n')

            if spinorbit.lower() == 'so':
              if n==1:
                logfile.write('\n')
                logfile.write('RASSI-SO FILE: ' + str(files[i])+'\n')
                logfile.write('\n')
                logfile.write('From To EnergyFrom(a.u.) EnergyTo(a.u.) EnergyFromTo(a.u) EnergyFromTo(eV) Osc.Strength \n')

            line = temp.readline()
            for k in range(0, 10000000):
                line = temp.readline()
                line = line.strip('\n')
                if '---------------------------------------' in line:
                  break
                else:
                    templist = line.split()
                    if i == 0:
                        shiftRASSI=0
                        if spinorbit.lower() == 'so':
                          shiftRASSISO=0
                    if i != 0:
                        shiftRASSI = 0
                        if spinorbit.lower() == 'so':
                          shiftRASSISO = 0
                        for h in range(0, i):
                          shiftRASSI=shiftRASSI+RASSIindex[h]
                          if spinorbit.lower() == 'so':
                            shiftRASSISO=shiftRASSISO+RASSISOindex[h]
                    if n == 0:
                      logfile.write(str(int(templist[0]))+' '+str(int(templist[1]))+' '+str(float(RASSI[int(templist[0])-1+int(shiftRASSI)]))+' '+str(float(RASSI[int(templist[0])-1+int(shiftRASSI)]))+' '+str(((float(RASSI[int(templist[1])-1+int(shiftRASSI)])-float(RASSI[int(templist[0])-1+int(shiftRASSI)]))))+' '+str(((float(RASSI[int(templist[1])-1+int(shiftRASSI)])-float(RASSI[int(templist[0])-1+int(shiftRASSI)]))*27.2107))+' '+str(float(templist[2]))+'\n')
                      spectraRASSIenergy.append((float(RASSI[int(templist[1])-1+int(shiftRASSI)])-float(RASSI[int(templist[0])-1+int(shiftRASSI)]))*27.2107)
                      spectraRASSIoscil.append(float(templist[2]))

                    if spinorbit.lower() == 'so':
                      if n == 1:
                        logfile.write(str(int(templist[0]))+' '+str(int(templist[1]))+' '+str(float(RASSISO[int(templist[0])-1+int(shiftRASSISO)]))+' '+str(float(RASSISO[int(templist[0])-1+int(shiftRASSISO)]))+' '+str(((float(RASSISO[int(templist[1])-1+int(shiftRASSISO)])-float(RASSISO[int(templist[0])-1+int(shiftRASSISO)]))))+' '+str(((float(RASSISO[int(templist[1])-1+int(shiftRASSISO)])-float(RASSISO[int(templist[0])-1+int(shiftRASSISO)]))*27.2107))+' '+str(float(templist[2]))+'\n')
                        spectraRASSISOenergy.append((float(RASSISO[int(templist[1]) - 1 + int(shiftRASSISO)]) - float(RASSISO[int(templist[0]) - 1 + int(shiftRASSISO)])) * 27.2107)
                        spectraRASSISOoscil.append(float(templist[2]))

        if 'Happy landing!' in line:
           temp.close()
           break

#Create the spectra grid
gridRASSI= int(round(float(int(round(float(max(spectraRASSIenergy)+3.0))))/resolution)) +1
spectraRASSI = [0] * gridRASSI
if spinorbit.lower() == 'so':
  gridRASSISO= int(round(float(int(round(float(max(spectraRASSISOenergy)+3.0))))/resolution)) +1
  spectraRASSISO = [0] * gridRASSISO

logfile.write(' \n')
logfile.write('RASSI SPECTRA \n')
logfile.write('MIN= 0.00 eV \n')
logfile.write('MAX= '+str(int(round(float(int(round(float(max(spectraRASSIenergy)+3.0)))))))+'.00 eV \n')
logfile.write('RESOLUTION= '+str(resolution)+' eV \n')
logfile.write(' \n')
if spinorbit.lower() == 'so':
  logfile.write('RASSI-SO SPECTRA \n')
  logfile.write('MIN= 0.00 eV \n')
  logfile.write('MAX= '+str(int(round(float(int(round(float(max(spectraRASSISOenergy)+3.0)))))))+'.00 eV \n')
  logfile.write('RESOLUTION= '+str(resolution)+' eV \n')
  logfile.write(' \n')


if type.lower() == 'gaussian':
  for i in range(0,len(spectraRASSI)):
      for j in range(0,len(spectraRASSIenergy)):
        spectraRASSI[i] = float(spectraRASSI[i]) + float(spectraRASSIoscil[j])*math.exp(-((((float(i)*resolution))-(float(spectraRASSIenergy[j])))**2)/(wide))
  if spinorbit.lower() == 'so':
    for i in range(0,len(spectraRASSISO)):
        for j in range(0,len(spectraRASSISOenergy)):
          spectraRASSISO[i] = float(spectraRASSISO[i]) + float(spectraRASSISOoscil[j])*math.exp(-((((float(i)*resolution))-(float(spectraRASSISOenergy[j])))**2)/(wide))

if type.lower() == 'lorentzian':
  print('not implemented yet')

if type.lower() != 'gaussian':
    if type.lower() != 'lorentzian':
      print('ERROR 3: Requested plot is not Gaussian or Lorentzian.')
      exit()

temp = open('spectraRASSI.dat','w')
for i in range(0,len(spectraRASSI)):
    temp.write(str((float(i)*resolution))+' '+str(spectraRASSI[i])+'\n')

if spinorbit.lower() == 'so':
  temp = open('spectraRASSI-SO.dat', 'w')
  for i in range(0, len(spectraRASSISO)):
      temp.write(str((float(i)*resolution))+' '+str(spectraRASSISO[i])+'\n')

logfile.write('Normal Termination \n')
logfile.write(' \n')
logfile.write(' 		    |\___/| 	    \n')
logfile.write(' 	       (,\  /,)\ \n')
logfile.write(' 	       /     /  \ \n')
logfile.write(' 	      (@_^_@)/   \	    \n')
logfile.write(' 	       W//W_/	  \ \n')
logfile.write(' 	     (//) |	       \ \n')
logfile.write(' 	   (/ /) _|_ /   )  \	    \n')
logfile.write(' 	 (// /) "/,_ _ _/  (~^-. \n')
logfile.write('    (( // )) ,-{       _   `.   \n')
logfile.write('   (( /// ))  "/\	  /	     |	 \n')
logfile.write('  (( ///))     `.	{	     } \n')
logfile.write('   ((/ ))	 .----~-.\    \-"     \n')
logfile.write('             ///.----..>    \ \n')
logfile.write('               ///-._ _  _ _} \n')
logfile.write(' 				\n')
logfile.write(' BESS THE DRAGON SALUTES YOU \n')
logfile.write('\n')

logfile.close()
