import os
#第几个条件,从0开始
condT = 0

#需要修改的参数
homedir = os.getcwd()
dirpath = homedir + '\\'
draco_enc = 'draco_encoder_old5.exe'
draco_dec = 'draco_decoder_old5.exe'
pce = 'pc_evalue_human_5.exe'
#os.mkdir('log')
logpath = 'log\\'

#human set
basketball_player_file_lst = list()
exercise_file_lst = list()
dancer_file_lst = list()
model_file_lst = list()

basketball_player_file_2st = list()
exercise_file_2st = list()
dancer_file_2st = list()
model_file_2st = list()

num_lst1 = range(1,65,1)

for name4 in num_lst1:
		basketball_player_file_lst.append( 'C1-limitlossyG-lossyA-ai_r5_basketball_player_vox11_dec-' + str(name4).zfill(8))
		exercise_file_lst.append( 'C1-limitlossyG-lossyA-ai_r5_exercise_vox11_dec-' + str(name4).zfill(8))
		dancer_file_lst.append( 'C1-limitlossyG-lossyA-ai_r5_dancer_vox11_dec-' + str(name4).zfill(8))
		model_file_lst.append( 'C1-limitlossyG-lossyA-ai_r5_model_vox11_dec-' + str(name4).zfill(8))   
		
for name5 in num_lst1:
		basketball_player_file_2st.append( 'basketball_player_vox11_' + str(name5).zfill(8))
		exercise_file_2st.append( 'exercise_vox11_' + str(name5).zfill(8))
		dancer_file_2st.append( 'dancer_vox11_' + str(name5).zfill(8))
		model_file_2st.append( 'model_vox11_' + str(name5).zfill(8))   

		
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
basketball_player_file_lst,
exercise_file_lst,
dancer_file_lst,
model_file_lst
])

file_lst = list([
basketball_player_file_lst,
exercise_file_lst,
dancer_file_lst,
model_file_lst
])

file_2st=list([
basketball_player_file_2st,
exercise_file_2st,
dancer_file_2st,
model_file_2st
])

    
#qp_lst=list([0,1,2,3,4,5,6,7,8,9,10,11,12])
qp_lst=list([0])
   
dir_lst=list([
'basketball_player_vox11\\r05\\',
'exercise_vox11\\r05\\',
'dancer_vox11\\r05\\',
'model_vox11\\r05\\',
])


for filenum in range(4):
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
		for name1,name10 in zip(file_lst[filenum],file_2st[filenum]):
			#seq = (datasetpath + dir_lst[filenum] + name1 + '.ply')
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
			os.system(pce + ' -f1 ' + seq2 + ' -f2 ' + seq + ' -cc 1 -pk 2047 >' + pcelog)
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


			

		
