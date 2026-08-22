list_set={
	'bg':['背景','具体调用function手动列表'],
	'bgm':['BGM','调用function改为直接现场引入'],
	'se':['音效','f_0003FC09'],
	'msg':['对话框位置','f_000349F2，(1,-1)居中，(0,nil)通常'],
	'cha':['角色栏','SPEAK部分，顺便调用语音'],
	'dia':['对话内容','f_00038348'],
	'cg':['CG图','现场引入'],
	'sel_start':['选项基底文字',''],
	'sel':['选项内容','f_00057F2E'],
	'sel_end':['选项结束标志','f_0005802C'],
	'specialeffect':['特殊特效','f_0003DF65'],
}

base_off=0x0008AEC7
new_off=int(base_off)
str_code='gbk'
header_bytes=b'\x01\x00\x00\x0C\x00\x02\x39\x68\x03\x00\x0C\x01\x19\x0E\x03\xA1\xA1\x00\x02\x60\x68\x03\x00\x0E\x03\xA1\xA1\x00\x02\xD2\x8B\x03\x00\x0C\x02\x0C\x04\x0C\x01\x0C\x01\x08\x02\x7A\x67\x03\x00\x0C\x0D\x08\x08\x08\x08\x02\x7A\x67\x03\x00\x0C\x00\x0B\xE8\x03\x08\x08\x08\x08\x08\x08\x08\x02\x5A\x11\x04\x00'
ender_bytes=b'\x0C\x00\x08\x02\xF1\x49\x03\x00\x0B\xE8\x03\x02\x95\x06\x04\x00\x02\x23\x54\x00\x00\x0C\x00\x0B\xE8\x03\x08\x08\x08\x08\x08\x08\x08\x02\x5A\x11\x04\x00\x0B\xDC\x05\x08\x08\x08\x08\x08\x08\x02\x74\x0E\x04\x00\x02\x49\x05\x04\x00\x02\x23\x54\x00\x00\x0C\x01\x08\x08\x02\x63\x0D\x04\x00\x04'
bg_list={
	1:['ゆめのねどこ·奥座敷','00005579'],
	2:['ゆめのねどこ·店先','00005727'],
	3:['ゆめのねどこ·店内','000059E2'],
	4:['ゆめのねどこ·大雅の部屋','00005BA6'],
	5:['ゆめのねどこ·魔法使いの工房','00005EC6'],
	6:['ゆめのねどこ·店先·夜の国','000058F7'],
	11:['桜ヶ丘学園·校門前','0000607C'],
	12:['桜ヶ丘学園·大雅の教室','000063BB'],
	13:['桜ヶ丘学園·時計塔の管理室','000066A3'],
	14:['桜ヶ丘学園·一階廊下','00006A24'],
	15:['桜ヶ丘学園·二階廊下','00006C15'],
	16:['桜ヶ丘学園·一階廊下·夜の国','00006E06'],
	17:['桜ヶ丘学園·二階廊下·夜の国','00006EFF'],
	18:['桜ヶ丘学園·刻の終着駅·夜の国','00006FF8'],
	21:['夜の遊園地·夜の国','00007111'],
	23:['桜ヶ丘学園·校門前·夜の国','00006298'],
	24:['桜ヶ丘学園·大雅の教室·夜の国','000065A8'],
	25:['桜ヶ丘学園·時計塔の管理室·夜の国','000068F9'],
	31:['千和のお店·店先','000071F4'],
	32:['千和のお店·店内','000073C2'],
	33:['千和のお店·千和の部屋','00007584'],
	34:['千和のお店·父親の部屋','00007734'],
	35:['千和のお店·廊下','000078E4'],
	36:['千和のお店·店先·夜の国','00007A69'],
	43:['夜月神社·社務所前','00007B52'],
	44:['夜月神社·社務所前·夜の国','00007CFD'],
	45:['夜月神社·石段','00007DF4'],
	46:['夜月神社·石段·夜の国','00007F9B'],
	51:['通学バスの中','0000808E'],
	61:['参禅町·大通り','00008288'],
	62:['参禅町·大通り·夜の国','0000846D'],
	63:['参禅町·裏路地','00008560'],
	64:['参禅町·裏路地·夜の国','00008707'],
	65:['参禅町·大通り２','000087FA'],
	66:['参禅町·大通り２·夜の国','000089E1'],
	67:['参禅町·展望広場','00008AD6'],
	68:['参禅町·展望広場·夜の国','00008C7F'],
	71:['参禅町·公園','00009071'],
	72:['参禅町·公園·夜の国','00009254'],
	73:['参禅町·坂の道','f_00009345'],
	74:['参禅町·坂の道·夜の国','000094EC'],
	75:['参禅町·通学路','000095DF'],
	76:['参禅町·通学路·夜の国','000097EA'],
	81:['列車内','000098DD'],
	82:['列車·客室車両','000099C1'],
	83:['ナナちゃんの部屋','00009AA1'],
	84:['扇形庫','00009B83'],
	85:['列車·屋根','00009C5B'],
	101:['空','00009D60'],
	1010:['空（雨天）','00009ED7'],
	102:['満月','0000A04E'],
	103:['桜空','0000A124'],
	105:['空·夜の国','0000A2C3'],
	106:['満月·夜の国','0000A393'],
	107:['桜空·夜の国','0000A483'],
	110:['校舎見上げ','0000A555'],
	112:['桜の木','0000A79D'],
	113:['桜の木·夜の国','0000A924'],
	200:['幻想の海','0000AABE'],
	201:['海底','0000AB52'],
	220:['闇','0000ABB8'],
	230:['空·きな穴','0000AC3C'],
	231:['空·きな穴２','0000ACCE'],
	300:['砂漠','0000AA00'],
}
length_now=0
isstart=0
isend=0
select_num=0
op_num=0
sel_target=[]

cha_list={
	'小黑':[0x00000004,'小黑',{}],
	'春':[0x000000DC,'春',{}],
	'千和':[0x000001B4,'千和',{}],
	'姫织':[0x0000028C,'姫织',{}],
	'真白':[0x00000362,'真白',{}],
	'十夜':[0x0000043A,'十夜',{}],
	'朝日':[0x00000512,'朝日',{}],
	'梓咲':[0x000005EA,'梓咲',{}],
	'七七':[0x000006C2,'七七',{}],
	'智仁':[0x0000079A,'智仁',{}],
	'索尔':[0x00000872,'索尔',{'一磨':10,'遠矢':100}],
	'纳哈特':[0x000009D0,'纳哈特',{}],
	'女孩子':[0x00000AB0,'女孩子',{}],
	'大雅':[0x00001784,'大雅',{'奏大雅':10}],
}
def pushstr(inputtext):
	return_bytes=b''
	try:
		str_bytes=inputtext.encode(str_code)
	except Exception as e:
		raise(f'在“inputtext”中含有{str_code}不支持的字符')
		return (return_bytes)
	length=len(str_bytes)+1
	return_bytes+=b'\x0e'
	return_bytes+=length.to_bytes()
	return_bytes+=str_bytes
	return_bytes+=b'\x00'
	return(return_bytes)

def pushint(inputint):
	return_bytes=b''
	m_add=b''
	iint=int(inputint)
	if iint<0:
		iint*=-1
		m_add+=b'\x19'
	if 0<iint<=127:
		return_bytes+=b'\x0c'
		return_bytes+=iint.to_bytes()
	elif 127<iint<=32767:
		return_bytes+=b'\x0b'
		return_bytes+=iint.to_bytes(2,'little')
	elif 32767<iint<=2147483647:
		return_bytes+=b'\x0a'
		return_bytes+=iint.to_bytes(4,'little')
	else:
		print('输入数字过大，请检查')
		return(return_bytes)
	return_bytes+=m_add
	return(return_bytes)

def chaload(inputlist):
	global cha_list
	#预期输入[chaload,realname,n:showname]
	#首先，固定一个角色编号。这里我们直接按冗余内容试试。50开始
	#如果不行那就老老实实len(cha_list)
	#cha_count=50
	cha_count=len(cha_list)
	return_bytes=b''
	function_hex=int(int(base_off)+length_now)
	now_offset=int(int(base_off)+length_now)
	dict_cha={}
	inputname=inputlist[0].strip()
	if inputname in cha_list:
		print(f'{inputname} is loaded.')
	else:
		#SPEAK的固定开头
		return_bytes+=b'\x01\x03\x00'
		return_bytes+=pushint(cha_count)
		return_bytes+=b'\x15\xE3\x00\x0F\xE3\x00\x02\x6E\x18\x00\x00'
		now_offset+=16
		#接着是具体显示人名的块
		for i in range(len(inputlist)+1):
			tmp_bytes=b''
			if i==0:
				#第二入参是否为-1的判定
				tmp_bytes+=b'\x10\xFD\x0C\x01\x19\x22'
				#跳转到下一处判定
				next_tar=f'speak_cha{cha_count}-{i+1}'
				tmp_bytes+=jmpset(['jz',next_tar])
				#设定显示为？？？
				tmp_bytes+=pushstr('　 ？？？ 　')
				tmp_bytes+=b'\x08\x02\x24\x81\x03\x00\x0F\xE3\x00\x09\x02\xAB\x21\x08\x00'
				#跳转到末尾设定
				tmp_bytes+=jmpset(['jump',f'::speak_end'])
				now_offset+=len(tmp_bytes)
				return_bytes+=tmp_bytes
			elif i<len(inputlist):
				#注册当前偏移
				now_tar=f'speak_cha{cha_count}-{i}'
				label_load(now_tar,now_offset)
				#第二入参判断
				tmp_bytes+=b'\x10\xFD'
				tmp_bytes+=pushint(int(inputlist[i].split(':')[0]))
				tmp_bytes+=b'\x22'
				#若否，跳转下一处判定
				next_tar=f'speak_cha{cha_count}-{i+1}'
				tmp_bytes+=jmpset(['jz',next_tar])
				#设定具体显示内容
				tmp_bytes+=pushstr(str(inputlist[i].split(':')[-1]))
				tmp_bytes+=b'\x08\x02\x24\x81\x03\x00\x0F\xE3\x00\x09\x02\xAB\x21\x08\x00'
				#跳转到末尾设定
				tmp_bytes+=jmpset(['jump',f'::speak_end'])
				now_offset+=len(tmp_bytes)
				return_bytes+=tmp_bytes
				dict_cha[str(inputlist[i].split(':')[-1]).strip()]=int(inputlist[i].split(':')[0])
			else:
				#注册当前偏移
				now_tar=f'speak_cha{cha_count}-{i}'
				label_load(now_tar,now_offset)
				#设定具体显示内容
				tmp_bytes+=pushstr(str(inputlist[0]))
				tmp_bytes+=b'\x08\x02\x24\x81\x03\x00\x0F\xE3\x00\x09\x02\xAB\x21\x08\x00'
				now_offset+=len(tmp_bytes)
				return_bytes+=tmp_bytes
		#注册固定end部分偏移
		end_tar='::speak_end'
		label_load(end_tar,now_offset)
		#末尾固定部分
		return_bytes+=b'\x0C\x01\x15\x1D\x00\x10\xFC\x15\x25\x01\x10\xFE\x15\x26\x01'
		return_bytes+=pushint(51)
		return_bytes+=b'\x02\x7B\x83\x07\x00\x14\x15\x27\x01\x04\x04'
			
		cha_count+=1
		
		cha_list[inputname]=[function_hex,dict_cha]
	return (return_bytes)


def selset(inputlist):
	#预期输入[sel,start/op/end,seldia,seltar|op]
	#基本选项架构
	global select_num
	global op_num
	global sel_target
	return_bytes=b''
	sel_start=int(0x0003836D).to_bytes(4,'little')
	sel_option=int(0x00057F0D).to_bytes(4,'little')
	sel_end=int(0x0005800B).to_bytes(4,'little')
	if inputlist[0]=='start':
		try:
			str_bytes=inputlist[1].encode(str_code)
		except Exception as e:
			raise(f'在“{inputlist[1]}”中含有{str_code}不支持的字符')
		#标记好选项位置
		sel_offset=int(int(base_off)+length_now)
		select_num+=1
		select_label='::select'+str(select_num)
		label_load(select_label,sel_offset)
		#写入正式内容
		#共4入参，第一入参为字符串，后续均为08即可
		length=len(str_bytes)+1
		return_bytes+=b'\x0E'
		return_bytes+=length.to_bytes()
		return_bytes+=str_bytes
		return_bytes+=b'\x00\x08\x08\x08\x02'
		return_bytes+=sel_start
	elif inputlist[0]=='op':
		try:
			str_bytes=inputlist[1].encode(str_code)
		except Exception as e:
			raise(f'在“{inputlist[1]}”中含有{str_code}不支持的字符')
		op_num+=1
		#3入参，第一入参字符串，后续0x08
		length=len(str_bytes)+1
		return_bytes+=b'\x0E'
		return_bytes+=length.to_bytes()
		return_bytes+=str_bytes
		return_bytes+=b'\x00\x08\x08\x02'
		return_bytes+=sel_option
		#导入选项目标到列表
		sel_target.append(inputlist[-1])
	elif inputlist[0]=='end':
		now_offset=int(int(base_off)+length_now)
		#l_selend=0
		return_bytes+=b'\x02'
		return_bytes+=sel_end
		now_offset+=5
		#选项后续判断
		for i in range(1,op_num+1):
			#记录当前偏移注册
			now_tar=f'::select{str(select_num)}-{str(i)}'
			label_load(now_tar,now_offset)
			#判断G[103]
			return_bytes+=b'\x0f\x67\x00\x0c'
			return_bytes+=i.to_bytes()
			return_bytes+=b'\x22'
			next_tar=f'::select{str(select_num)}-{str(i+1)}' if i<op_num else f'::select{str(select_num)}'
			return_bytes+=jmpset(['jz',next_tar])
			now_offset+=11
			#若选择了第i项则如何，暂时写法是跳转到目标
			jump_seltarget_bytes=jmpset(['jump',sel_target[i-1]])
			return_bytes+=jump_seltarget_bytes
			now_offset+=len(jump_seltarget_bytes)
		#清空选项相关记录
		op_num=0
		sel_target=[]
	return (return_bytes)


jmp_tem={}
jmp_real={}
tem_label=int(0xffffffff)

def jmpset(inputlist):
	global jmp_tem
	global tem_label
	return_bytes=b''
	#预期输入：跳转方式，跳转目标如[jump,::label1]
	#选项内用[jz,::sel_targetn]之类的方式
	if inputlist[0]=='jump':
		return_bytes+=b'\x06'
	else:
		return_bytes+=b'\x07'
	if inputlist[-1] in jmp_tem:
		#使用已有占位字节
		return_bytes+=jmp_tem[inputlist[-1]]
	else:
		#注册临时占位字节
		tmp_off=tem_label.to_bytes(4,'little')
		return_bytes+=tmp_off
		jmp_tem[inputlist[-1]]=tmp_off
		tem_label-=1
	print(return_bytes)
	return (return_bytes)

def label_load(inputlabel,n):
	#预期输入：目标标签如::label1。
	#手动输入标签坐标，一般情况下有预设记录
	global jmp_real
	if inputlabel not in jmp_real:
		jmp_real[inputlabel]=n.to_bytes(4,'little') 
	
	return None

def jmpreplace(inputbytes):
	global return_bytes
	for i in jmp_tem:
		if i not in jmp_real:
			print('有未定义的jump目标')
			break
		else:
			print(jmp_real[i])
			inputbytes=inputbytes.replace(jmp_tem[i],jmp_real[i])
	
	return (inputbytes)

with open('base/cg_loaded.txt') as f:
	lines = [line.strip() for line in f if line.strip()]
cg_loaded = {lines[i+1].strip('"').upper(): int(lines[i],16) for i in range(0, len(lines), 2)}




bs_current=[]
def bsfade():
	global bs_current
	return_bytes=b''
	inputlist=bs_current 
	#function_offset=0x00043F97
	if inputlist!=[]:
		print(inputlist)
		
		#return_bytes+=b'\x0c\x00\x0c\x00\x0b\x5e\x01\x0b\x26\x02\x08\x08\x08\x08\x08\x08\x08\x08\x02\xa3\x26\x05\x00'
		return_bytes+=b'\x08\x08\x02\xa9\xba\x00\x00'
		#return_bytes+=b'\x0c'
		#return_bytes+=int(inputlist[0]).to_bytes()
		#return_bytes+=b'\x0c'
		#return_bytes+=int(inputlist[1]).to_bytes()
		#return_bytes+=b'\x0c'
		#return_bytes+=int(inputlist[2]).to_bytes()
		#return_bytes+=b'\x0c'
		#return_bytes+=int(inputlist[3]).to_bytes()
		#return_bytes+=b'\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08'
		#return_bytes+=b'\x02'
		#return_bytes+=int(function_offset).to_bytes(4,'little')
		bs_current=[]
		print(bs_current)
		return(return_bytes)
	else:
		print('当前无立绘，无法消除')
		return (b'')

def bsset(inputlist):
	global bs_current
	return_bytes=b''
	function_offset=0x00043F97
	#立绘设定。虽然入参还有很多不理解的内容
	#预期输入，[cha,pose,cloth,face,l,'l/m/r',z,x,y,lyr,alpha(?)]
	#已知，前4个入参对应角色、姿势、服装、表情
	bs_current=inputlist[:4]
	return_bytes+=b'\x0c'
	return_bytes+=int(inputlist[0]).to_bytes()
	return_bytes+=b'\x0c'
	return_bytes+=int(inputlist[1]).to_bytes()
	return_bytes+=b'\x0c'
	return_bytes+=int(inputlist[2]).to_bytes()
	return_bytes+=b'\x0c'
	return_bytes+=int(inputlist[3]).to_bytes()
	#接下来是自由入参，一共10个
	#第一个是l，虽然不清楚具体含义，为0居多。
	#为-10则，清除当前立绘，为 `0 / -1 / 1 / 2` = 四种不同构图状态
	#似乎具体调用默认、L、U、S的文件名。0是L，1是U，2是S，-1默认
	return_bytes+=b'\x0c'
	if int(inputlist[4])>=0:
		l_num = int(inputlist[4])
		return_bytes+=l_num.to_bytes()
	else:
		l_num = int(inputlist[4])*(-1)
		return_bytes+=l_num.to_bytes()
		return_bytes+=b'\x19'
	#第二个自由入参为预设站位，0右1中2左
	bslocation={'l':2,'m':1,'r':0}
	loc_num=bslocation[inputlist[5]] #if inputlist[5] in bslocation else 1
	return_bytes+=b'\x0c'
	return_bytes+=loc_num.to_bytes()
	#第三个自由入参，未知
	return_bytes+=b'\x08'
	#第四个入参，z，虽然我想取巧用默认值算了）
	return_bytes+=b'\x0b'
	return_bytes+=int(inputlist[6]).to_bytes(2,'little')
	#第五第六个入参是x,y
	x_num=int(inputlist[7])
	return_bytes+=b'\x0b'
	if x_num>=0:
		return_bytes+=x_num.to_bytes(2,'little')
	else:
		x_num*=-1
		return_bytes+=x_num.to_bytes(2,'little')
		return_bytes+=b'\x19'
	y_num=int(inputlist[8])
	return_bytes+=b'\x0b'
	if y_num>=0:
		return_bytes+=y_num.to_bytes(2,'little')
	else:
		y_num*=-1
		return_bytes+=y_num.to_bytes(2,'little')
		return_bytes+=b'\x19'
	#第七个入参，不明确
	return_bytes+=b'\x08'
	#第八个，控制层次
	lyr_num=int(inputlist[9])
	return_bytes+=b'\x0c'
	return_bytes+=lyr_num.to_bytes()
	#第九个，透明度。但我不想设置了
	#第十个好像是第二层alpha，不管
	return_bytes+=b'\x08\x08'
	
	return_bytes+=b'\x02'
	return_bytes+=int(function_offset).to_bytes(4,'little')
	print(bs_current)
	return(return_bytes)


def chaset(inputlist):
	return_bytes=b''
	#预期输入格式['角色名/实际用名','语音编号']
	#首先第一入参设置语音调用
	if len(inputlist)==2:
		return_bytes+=b'\x0a'
		return_bytes+=int(inputlist[1]).to_bytes(4,'little')
	else:
		return_bytes+=b'\x08'
	#然后是第二入参，使用名义判断
	cha_realname=inputlist[0].split('/')[0]
	if cha_realname in cha_list:
		function_offset=int(cha_list[cha_realname][0])
		#使用其他名义
		if '/' in inputlist[0]:
			#
			cha_showname=inputlist[0].split('/')[-1].strip()
			if cha_showname in cha_list[cha_realname][-1]:
				nameshowint=cha_list[cha_realname][-1][cha_showname]
				return_bytes+=b'\x0c'
				return_bytes+=nameshowint.to_bytes()
			
			elif cha_showname == '？？？':
				return_bytes+=b'\x0c\x01\x19'
			#使用了未预设名义，当作使用本名处理
			else:
				return_bytes+=b'\x08'
		#本名，第二入参为nil
		else :
			return_bytes+=b'\x08'
	else:
		print('无预设人名，请手修hcb')
		return(b'')
	#后续入参，大雅3个，普通角色1个。
	if cha_realname=='大雅':
		return_bytes+=b'\x08\x08\x08'
	else:
		return_bytes+=b'\x08'
	#调用最终function
	return_bytes+=b'\x02'
	return_bytes+=function_offset.to_bytes(4,'little')
	return (return_bytes)



def bgset(inputlist):
	if int(inputlist[0]) in bg_list:
		function_offset=bg_list[int(inputlist[0])][-1]
		if len(inputlist)>1:
			bg_num=int(inputlist[-1])
			#第七个入参控制具体细分
			return_bytes=b'\x08\x08\x08\x08\x08\x08'+b'\x0c'+bg_num.to_bytes()+b'\x08\x08\x08\x02'+bytes.fromhex(function_offset)[::-1]
		else:
			#第八个入参为-1
			return_bytes=b'\x08\x08\x08\x08\x08\x08\x08\x0c\x01\x19\x08\x08\x02'+bytes.fromhex(function_offset)[::-1]
		return_bytes+=b'\x0C\x00\x0B\x20\x03\x08\x08\x08\x08\x08\x08\x08\x02\x5A\x11\x04\x00'
	return(return_bytes)

def cgload(cgname):
	return_bytes=b''
	realcgname=cgname.upper()
	if realcgname in cg_loaded:
		print(f'{cgname} is loaded.')
	else:
		try:
			cgname_bytes=realcgname.encode(str_code)
		except Exception as e:
			raise(f'在“{cgname}”中含有{str_code}不支持的字符')
		length=len(cgname_bytes)+1
		return_bytes+=b'\x01\x06\x00\x02\xAC\x51\x00\x00\x0E'
		return_bytes+=length.to_bytes()
		return_bytes+=cgname_bytes
		return_bytes+=b'\x00\x10\xF9\x0C\x01\x08\x10\xFA\x10\xFB\x10\xFC\x10\xFD\x08\x08\x02\x6A\xC8\x03\x00\x08\x08\x10\xFE\x02\xD3\x51\x00\x00\x04'
		
	return (return_bytes)

		
def cgset(inputlist):
	#预设传入内容[cg名,x,y,z,time]或[cg名,time]
	return_bytes=b''
	cgname=inputlist[0].upper()
	if cgname not in cg_loaded:
		print(f'{cgname} is not loaded.')
		return b''
	else:
		#function_offset为十进制数的偏移
		function_offset=cg_loaded[cgname]
	if len(inputlist)==5:
		#不使用现有设定
		return_bytes+=b'\x0c\x00'

		xpos=int(inputlist[1])
		#入参x
		if xpos>=0:
			return_bytes+=b'\x0b'
			return_bytes+=xpos.to_bytes(2,'little')
		else:
			xpos_in=xpos*(-1)
			return_bytes+=b'\x0b'
			return_bytes+=xpos_in.to_bytes(2,'little')
			return_bytes+=b'\x19'

		ypos=int(inputlist[2])
		#入参y
		if ypos>=0:
			return_bytes+=b'\x0b'
			return_bytes+=ypos.to_bytes(2,'little')
		else:
			ypos_in=ypos*(-1)
			return_bytes+=b'\x0b'
			return_bytes+=ypos_in.to_bytes(2,'little')
			return_bytes+=b'\x19'

		zoom=3000-int(float(inputlist[3])*1000)
		#入参z
		return_bytes+=b'\x0b'
		return_bytes+=zoom.to_bytes(2,'little')
		#入参rotate，我们不设置这一项
		return_bytes+=b'\x08'
	else:
		#使用现有设定，于是xyz和rotate都raise nil
		return_bytes+=b'\x08\x08\x08\x08\x08'
	timeset=int(inputlist[-1])
	return_bytes+=b'\x0b'
	return_bytes+=timeset.to_bytes(2,'little')
	
	return_bytes+=b'\x02'
	return_bytes+=int(function_offset).to_bytes(4,'little')
	return(return_bytes)

def diaset(inputstr):
	function_offset='00038347'
	try:
		str_bytes=inputstr.encode(str_code)
	except Exception as e:
		raise(f'在“{inputstr}”中含有{str_code}不支持的字符')
	length=len(str_bytes)+1
	return_bytes=b'\x0E'+length.to_bytes()+str_bytes+b'\x00\x08\x08\x08\x08\x02'+bytes.fromhex(function_offset)[::-1]
	return (return_bytes)

def msgset(inputtype):
	return_bytes=b''
	function_offset='000349f1'
	if inputtype=='middle':
		return_bytes=b'\x0c\x01\x0c\x01\x19\x02'+bytes.fromhex(function_offset)[::-1]
	elif inputtype=='normal':
		#return_bytes+=b'\x0c\x00\x08\x02\xf4\x64\x08\x00'
		return_bytes+=b'\x0c\x00\x08\x02'+bytes.fromhex(function_offset)[::-1]
		#0003b797，强制恢复对话栏的显示
		return_bytes+=b'\x0c\x00\x02\x97\xb7\x03\x00'
	elif inputtype=='boxin':
		#000864F4，此处大概是恢复对话框的入参(0,nil)
		return_bytes+=b'\x0c\x00\x08\x02\xf4\x64\x08\x00'
	elif inputtype=='boxout':
		#000864F4，此处是隐藏对话框的入参(1,-2)
		return_bytes+=b'\x0c\x01\x0c\x02\x19\x02\xf4\x64\x08\x00'
		#return_bytes+=b'\x0c\x00\x08\x02'+bytes.fromhex(function_offset)[::-1]
	else:
		print('未定义对话栏位置或特殊操作')
		#return None
		return_bytes=b''
	return (return_bytes)
	
def bgmset(inputint):
	function_offset='00040552'
	try:
		bgmnum=int(inputint)
	except Exception as e:
		raise(f'不合规的入参，预期输入1-255之间的整数')
	return_bytes=b'\x0c'+bgmnum.to_bytes()+b'\x08\x08\x08\x08\x02'+bytes.fromhex(function_offset)[::-1]
	#print(return_bytes)
	return(return_bytes)

def seset(inputlist):
	#预期输入[音效编号,(loop/end)或空,time]
	return_bytes=b''
	function_offset='0003FC08'
	senum=int(inputlist[0])
	return_bytes+=b'\x0b'
	return_bytes+=senum.to_bytes(2,'little')
	if len(inputlist)>1:
		if inputlist[1]=='loop':
			return_bytes+=b'\x0c\x01\x08\x08'
			return_bytes+=b'\x0b'
			return_bytes+=int(inputlist[-1]).to_bytes(2,'little')
			return_bytes+=b'\x02'
		elif inputlist[1]=='end':
			return_bytes+=b'\x0b'
			return_bytes+=int(inputlist[-1]).to_bytes(2,'little')
			return_bytes+=b'\x0c\x00\x08\x08\x02'
		else :
			print('与预期输入不符，请检查')
			return (b'')
	else:
		return_bytes+=b'\x08\x08\x08\x08\x02'
	return_bytes+=bytes.fromhex(function_offset)[::-1]
	return (return_bytes)


def line_to_hcb(script):
	global isstart
	global return_bytes
	global length_now
	global isend
	global new_off
	with open(script,'r',encoding='gbk') as f:
		lst=f.readlines()
		#return_bytes+=header_bytes
	for i,line in enumerate(lst):
		print(i)
		#print(line_to_hcb(line))
		#return_bytes+=line_to_hcb(line)
	
		if line.startswith('[') and line[0]!='#':
			inputlist=line[1:len(line)-2].split(',')
			if inputlist[0]=='cg':
				return_bytes+=cgset(inputlist[1:])
				length_now+=len(cgset(inputlist[1:]))
			elif inputlist[0]=='dia':
				return_bytes+=diaset(inputlist[-1])
				length_now+=len(diaset(inputlist[-1]))
			elif inputlist[0]=='bgm':
				return_bytes+=bgmset(inputlist[-1])
				length_now+=len(bgmset(inputlist[-1]))
			elif inputlist[0]=='msg':
				return_bytes+=msgset(inputlist[-1])
				length_now+=len(msgset(inputlist[-1]))
			elif inputlist[0]=='bg':
				return_bytes+=bgset(inputlist[1:])
				length_now+=len(bgset(inputlist[1:]))
			elif inputlist[0]=='se':
				return_bytes+=seset(inputlist[1:])
				length_now+=len(seset(inputlist[1:]))
			elif inputlist[0]=='cha':
				return_bytes+=chaset(inputlist[1:])
				length_now+=len(chaset(inputlist[1:]))
			elif inputlist[0]=='bs':
				return_bytes+=bsset(inputlist[1:])
				length_now+=len(bsset(inputlist[1:]))
			elif inputlist[0]=='bsfade':
				bsfade_result=bsfade()
				return_bytes+=bsfade_result
				length_now+=len(bsfade_result)
			elif inputlist[0]=='jump':
				return_bytes+=jmpset(inputlist)
				length_now+=len(jmpset(inputlist))
			elif inputlist[0]=='sel':
				result=selset(inputlist[1:])
				return_bytes+=result
				length_now+=len(result)
			elif inputlist[0]=='white':
				#背景调白
				return_bytes+=b'\x02\x67\x54\x00\x00\x0c\x00\x0b\xe8\x03\x08\x08\x08\x08\x08\x08\x08\x02\x5a\x11\x04\x00'
				length_now+=22
			elif inputlist[0]=='bgmstop':
				return_bytes+=b'\x08\x02\x95\x06\x04\x00'
				length_now+=6
			elif inputlist[0]=='eyecatch':
				return_bytes+=b'\x08\x08\x08\x08\x08\x02\x7B\x6E\x03\x00'
				length_now+=10
			elif inputlist[0]=='cgload':
				if isstart==0:
					result=cgload(inputlist[-1])
					return_bytes+=result
					cg_offset=int(int(base_off)+length_now)
					cg_loaded[inputlist[-1].upper()]=cg_offset
					length_now+=len(result)
					new_off+=len(result)
					print(cg_loaded[inputlist[-1].upper()])
					print(inputlist[-1].upper())
			elif inputlist[0]=='chaload':
				if isstart==0:
					result=chaload(inputlist[1:])
					return_bytes+=result
					
					length_now+=len(result)
					new_off+=len(result)
					print(cha_list)
			elif inputlist[0]=='start':
				isstart+=1
				return_bytes+=header_bytes
				length_now+=len(header_bytes)
			elif inputlist[0]=='end':
				isend+=1
				return_bytes+=ender_bytes
				length_now+=len(ender_bytes)
			else:
				continue
		elif line.startswith('::') and line[0]!='#':
			inputlabel=line.strip()
			label_offset_num=int(int(base_off)+length_now)
			label_load(inputlabel,label_offset_num)
		else:
			continue
	#return_bytes+=ender_bytes

length_now=0
if __name__ == '__main__':
	return_bytes=b''
	#isstart=0
	#isend=0
	#script=input('输入待处理剧本文件名：')
	script='base/Script.txt'
	line_to_hcb(script)
	return_bytes=jmpreplace(return_bytes)
	with open('base/base.chb','rb') as g,open('.test.chb','wb') as h:
		oribytes=g.read()
		mainender=oribytes[int.from_bytes(oribytes[:4],'little'):]
		offset=int(base_off)+length_now
		h.write(offset.to_bytes(4,'little'))
		h.write(oribytes[4:int(base_off)].replace(int(base_off).to_bytes(4,'little'),int(new_off).to_bytes(4,'little')))
		h.write(return_bytes)
		h.write(mainender)
	#a=input('回车退出')