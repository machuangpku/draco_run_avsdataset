import os
#第几个条件,从0开始
condT = 0

#需要修改的参数
homedir = os.getcwd()
dirpath = homedir + '\\'
draco_enc = 'draco_encoder_livox1.exe'
draco_dec = 'draco_decoder_livox1.exe'
pce = 'pc_evalue_livox1.exe'
#os.mkdir('log')
logpath = 'log\\'

#Livox set		
Livox_01_all_file_lst = list()
Livox_02_all_file_lst = list()		
num_lst1 = range(0,387,1)
for name4 in num_lst1:
        Livox_01_all_file_lst.append( 'C1-limitlossyG-lossyA-ai_r5_Livox_01_all_1mm_dec-' + str(name4).zfill(4))
        Livox_02_all_file_lst.append( 'C1-limitlossyG-lossyA-ai_r5_Livox_02_all_1mm_dec-' + str(name4).zfill(4))	

Livox_01_all_file_2st = list()
Livox_02_all_file_2st = list()		
num_lst1 = range(0,387,1)
for name4 in num_lst1:
        Livox_01_all_file_2st.append( 'Livox_01_all_1mm-' + str(name4).zfill(4))
        Livox_02_all_file_2st.append( 'Livox_02_all_1mm-' + str(name4).zfill(4))	


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

#设置数据集
ford_file_lst = list([
Livox_01_all_file_lst,
Livox_02_all_file_lst,
])
ford_file_2st = list([
Livox_01_all_file_2st,
Livox_02_all_file_2st,
])
qp_lst=list([0])
    
dir_lst=list([
'Livox_01_all_in_one_1mm\\r05\\',
'Livox_02_all_in_one_1mm\\r05\\',
])

for filenum in range(2):
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
		for name1,name10 in zip(ford_file_lst[filenum],ford_file_2st[filenum]):
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
			os.system(draco_enc + ' -point_cloud -i ' + seq + ' -o ' + bin + ' -qp '+str(qp) +' -qt 0 -qn 0 -qg 0 -nc 1 -geo 0 -cl 10>' + enclog)
			
			os.system(draco_dec + ' -i ' + bin + ' -o ' + dec +' -nc 1 >' + declog) 		
			os.system(pce + ' -f1 ' + seq2 + ' -f2 ' + seq + ' -cr 1 -pk 30000 >' + pcelog)
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
			datasetlen=len(ford_file_lst[filenum])
		#print(name+ ' ' +str(totalPointcount) + ' ' + str(totalBinsize) + ' '+ str(enctime) + ' '+ str(dectime))
		total_log.write(name1 + ' '+str(qp)+ ' '+ str(totalPointcount) + ' ' + str(totalPointcountin) + ' ' + str(totalBinsize) + ' '+ str(enctime) + ' '+ str(dectime)+ ' '+str(totalD1/datasetlen)+ ' '+str(totalD2/datasetlen)+ ' '+str(totalC0/datasetlen)+ ' '+str(totalC1/datasetlen)+ ' '+str(totalC2/datasetlen)+ ' ' +str(totalR/datasetlen)+ ' '+ '\n')
	total_log.close()
#运行end