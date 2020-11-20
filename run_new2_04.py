import os
#第几个条件,从0开始
condT = 0

#需要修改的参数
homedir = os.getcwd()
dirpath = homedir + '\\'
draco_enc = 'draco_encoder_new2_01.exe'
draco_dec = 'draco_decoder_new2_01.exe'
pce = 'pc_evalue_human_new2_01.exe'
#os.mkdir('log')
logpath = 'log\\'

#human set
stanford_area_2_vox20 = list()
stanford_area_4_vox20 = list()
Church_vox16 = list()
Courthouse_vox16 = list()
Ignatius_vox11 = list()
QQdog_vox15 = list()
Truck_vox15 = list()

num_lst1 = range(1,2,1)

for name4 in num_lst1:
		stanford_area_2_vox20.append( 'stanford_area_2_vox20' )
		stanford_area_4_vox20.append( 'stanford_area_4_vox20' )
		Church_vox16.append( 'Church_vox16' )
		Courthouse_vox16.append( 'Courthouse_vox16' )
		Ignatius_vox11.append( 'Ignatius_vox11' )
		QQdog_vox15.append( 'QQdog_vox15' )
		Truck_vox15.append( 'Truck_vox15' )

stanford_area_2_vox201 = list()
stanford_area_4_vox201 = list()
Church_vox161 = list()
Courthouse_vox161 = list()
Ignatius_vox111 = list()
QQdog_vox151 = list()
Truck_vox151 = list()

num_lst1 = range(1,2,1)

for name5 in num_lst1:
		stanford_area_2_vox201.append( 'C1-limitlossyG-lossyA-ai_r4_stanford_area_2_vox20_dec' )
		stanford_area_4_vox201.append( 'C1-limitlossyG-lossyA-ai_r4_stanford_area_4_vox20_dec' )
		Church_vox161.append( 'C1-limitlossyG-lossyA-ai_r4_Church_vox16_dec' )
		Courthouse_vox161.append( 'C1-limitlossyG-lossyA-ai_r4_Courthouse_vox16_dec' )
		Ignatius_vox111.append( 'C1-limitlossyG-lossyA-ai_r4_Ignatius_vox11_dec' )
		QQdog_vox151.append( 'C1-limitlossyG-lossyA-ai_r4_QQdog_vox15_dec' )
		Truck_vox151.append( 'C1-limitlossyG-lossyA-ai_r4_Truck_vox15_dec' )
		

		
def getPointCount(dec):
	decfile = open(dec,'r',encoding='ISO-8859-1')
	voxelnum=0
	for line in decfile:
		words = line.split()
		if 'element' in words:
			voxelnum = int(words[2])
			return voxelnum
	return voxelnum
	
def readpce(pcelog):
	reader = open( pcelog, 'r')
	D1=0
	D2=0
	C0=0
	C1=0
	C2=0
	R=0
	for line in reader:
		words = line.split()
		if ('D1_PSNR_F' in words):
			D1=float(words[2])
		if ('D1_HausdorffPSNR_F' in words):
			D2=float(words[2])
		if ('c[0]_PSNR_F' in words):
			C0=float(words[2])
		if ('c[1]_PSNR_F' in words) :
			C1=float(words[2])
		if ('c[2]_PSNR_F' in words) :
			C2=float(words[2])
		if ('rel_PSNR_F' in words) :
			R=float(words[2])
	return D1,D2,C0,C1,C2,R
	
def readenc(file_name):
	time1=0
	reader = open( file_name, 'r')
	for line in reader:
		words = line.split()
		if ('ms' in words)and('encode' in words):
			time1+=float(words[6][1:])
		if ('ms' in words)and('decode' in words):
			time1+=float(words[5][1:])
	reader.close()
	return time1

#运行start

#设置数据集
ford_file_lst = list([
stanford_area_2_vox20,
stanford_area_4_vox20,
Church_vox16,
Courthouse_vox16,
Ignatius_vox11,
QQdog_vox15,
Truck_vox15
])

file_lst = list([
stanford_area_2_vox20,
stanford_area_4_vox20,
Church_vox16,
Courthouse_vox16,
Ignatius_vox11,
QQdog_vox15,
Truck_vox15
])

file_2st = list([
stanford_area_2_vox201,
stanford_area_4_vox201,
Church_vox161,
Courthouse_vox161,
Ignatius_vox111,
QQdog_vox151,
Truck_vox151
])

    
#qp_lst=list([0,1,2,3,4,5,6,7,8,9,10,11,12])
qp_lst=list([0])
peak_lst=list([1048575,1048575,65535,65535,2047,32767,32767])
   
dir_lst=list([
'stanford_area_2_vox20\\r04\\',
'stanford_area_4_vox20\\r04\\',
'Church_vox16\\r04\\',
'Courthouse_vox16\\r04\\',
'Ignatius_vox11\\r04\\',
'QQdog_vox15\\r04\\',
'Truck_vox15\\r04\\',
])


for filenum in range(7):
	datasetpath = 'D:\\draco\\scripts_pcem0.5\\log\\'
	datasetpath1='D:\\AVS\dataset\\'
	pointcountlog = (dirpath + 'total_log\\' + dir_lst[filenum] + 'total.txt')
	total_log=open(pointcountlog,'w')
	for qp in qp_lst:
		totalPointcount = 0
		totalPointcountin=0
		totalBinsize = 0
		enctime=0
		dectime=0
		totalD1=0
		totalD2=0
		totalC0=0
		totalC1=0
		totalC2=0
		totalR=0
		datasetlen=0
		peakk=peak_lst[filenum]
		for name1,name10 in zip(file_2st[filenum],file_lst[filenum]):
			seq = (datasetpath +name1+ '.ply')
			seq2 = (datasetpath1 + name10 + '.ply')
			#print(seq)
			dec = (dirpath + 'dec\\' + dir_lst[filenum] + name1 + '_dec.ply')
			bin = (dirpath + 'bin\\' + dir_lst[filenum] + name1 + '.bin')
			#print(dec)
			#print(bin)
			enclog = (logpath + dir_lst[filenum] + name1 +str(qp) + '_enc.log')
			declog = (logpath + dir_lst[filenum] + name1+str(qp)  + '_dec.log')
			pcelog = (logpath + dir_lst[filenum] + name1 +str(qp) + '_pce.log')
			os.system(draco_enc + ' -point_cloud -i ' + seq + ' -o ' + bin + ' -qp '+str(qp) +' -qt 0 -qn 0 -qg 0 -nc 1 -cl 10 -geo 0 >' + enclog)
			
			os.system(draco_dec + ' -i ' + bin + ' -o ' + dec +' -nc 1 >' + declog) 		
			os.system(pce + ' -f1 ' + seq2 + ' -f2 ' + seq + ' -cc 1 '+'-pk'+str(peakk) +'>' + pcelog)
			#os.system(pce + ' -f1 ' + seq2 + ' -f2 ' + seq + ' -cc 1 -pk 30000 >' + pcelog)
			totalPointcount += getPointCount(dec)
			totalPointcountin+=getPointCount(seq)
			D1,D2,C0,C1,C2,R=readpce(pcelog)
			totalD1+=float(D1)
			totalD2+=float(D2)
			totalC0+=float(C0)
			totalC1+=float(C1)
			totalC2+=float(C2)
			totalR+=float(R)
			siez_bin = os.path.getsize(bin)
			totalBinsize += int(siez_bin)*8
			enctime += readenc(enclog)
			dectime += readenc(declog)
			os.remove(bin)
			os.remove(dec)
			print(name1)
			datasetlen=len(file_lst[filenum])
		#print(name+ ' ' +str(totalPointcount) + ' ' + str(totalBinsize) + ' '+ str(enctime) + ' '+ str(dectime))
		total_log.write(name1 + ' '+str(qp)+ ' '+ str(totalPointcount) + ' ' + str(totalPointcountin) + ' ' + str(totalBinsize) + ' '+ str(enctime) + ' '+ str(dectime)+ ' '+str(totalD1/datasetlen)+ ' '+str(totalD2/datasetlen)+ ' '+str(totalC0/datasetlen)+ ' '+str(totalC1/datasetlen)+ ' '+str(totalC2/datasetlen)+ ' ' +str(totalR/datasetlen)+ ' '+ '\n')
	total_log.close()
#运行end


			

		
