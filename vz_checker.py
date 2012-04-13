#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
@author: snooda
@website: www.snooda.com
@License: GNU GPL v3
A script to show OpenVZ resource message friendly
'''

import sys


class beanAttr:
	held = 0
	maxheld = 0
	barrier = 0
	limit = 0 
	failcnt = 0
	def getNum(self, num, type):
		if type == 'k':
			return num/1024.0
		elif type == 'm':
			return num/(1024.0 * 1024.0)
		elif type == 'g':
			return num/(1024.0 * 1024.0 * 1024.0)
		elif type == 'w':
			return num/10000.0
		elif type == 'e':
			return num/(10000.0 * 10000.0)
		elif type == 'n':
			return num
		else:
			raise Exception("type not support")
			return None
	def getHeld(self, type):
		return self.getNum(self.held, type)
	def getMaxHeld(self, type):
		return self.getNum(self.maxheld, type)
	def getBarrier(self, type):
		return self.getNum(self.barrier, type)
	def getLimit(self, type):
		return self.getNum(self.limit, type)
	def getFailcnt(self, type):
		return self.getNum(self.failcnt, type)

class beanPageAttr(beanAttr):
	def getNum(self, num, type):
		return beanAttr.getNum(self, num * 4096, type)




class Kmemsize(beanAttr):
	pass
class Lockedpages(beanPageAttr):
	pass
class Privvmpages(beanPageAttr):
	pass
class Shmpages(beanPageAttr):
	pass
class Numproc(beanAttr):
	pass
class Physpages(beanPageAttr):
	pass
class Vmguarpages(beanPageAttr):
	pass
class Oomguarpages(beanPageAttr):
	pass
class Numtcpsock(beanAttr):
	pass
class Numflock(beanAttr):
	pass
class Numpty(beanAttr):
	pass
class Numsiginfo(beanAttr):
	pass
class Tcpsndbuf(beanAttr):
	pass
class Tcprcvbuf(beanAttr):
	pass
class Othersockbuf(beanAttr):
	pass
class Dgramrcvbuf(beanAttr):
	pass
class Numothersock(beanAttr):
	pass
class Dcachesize(beanAttr):
	pass
class Numfile(beanAttr):
	pass
class Numiptent(beanAttr):
	pass



class beanData:
	_uid = None
	_cur = None
	kmemsize = Kmemsize()
	lockedpages = Lockedpages()
	privvmpages = Privvmpages()
	shmpages = Shmpages()
	numproc = Numproc()
	physpages = Physpages()
	vmguarpages = Vmguarpages()
	oomguarpages = Oomguarpages()
	numtcpsock = Numtcpsock()
	numflock = Numflock()
	numpty = Numpty()
	numsiginfo = Numsiginfo()
	tcpsndbuf = Tcpsndbuf()
	tcprcvbuf = Tcprcvbuf()
	othersockbuf = Othersockbuf()
	dgramrcvbuf = Dgramrcvbuf()
	numothersock = Numothersock()
	dcachesize = Dcachesize()
	numfile = Numfile()
	numiptent = Numiptent()
	
class Line:
	msgPos = 0
	ptr = 0
	inMsg = 0
	def __init__(self, line):
		self.msgPos = 0
		self.ptr = 0
		self.inMsg = 0
		self.line = line
	def getOutMsgTry(self):
		if self.inMsg != 1:
			return None
		tmp_ptr = self.ptr
		while self.line[tmp_ptr] != ' ':
			if self.line[tmp_ptr] == '\n':
				break
			tmp_ptr += 1
		return tmp_ptr
	def getOutMsg(self):
		resu_ptr = self.getOutMsgTry()
		if resu_ptr != None:
			self.ptr = resu_ptr
			self.inMsg = 0
			return 1
		else:
			return 0
	def getInMsg(self):
		if self.inMsg != 0:
			return
		while self.line[self.ptr] == ' ':
			self.ptr += 1
		self.inMsg = 1
		self.msgPos +=1
	def getAttrNum(self):
		param_end_ptr = self.getOutMsgTry()
		assert param_end_ptr != None
		param = int(self.line[self.ptr:param_end_ptr])
		return param




def splitLine(bd, line_obj):
	resu = {}
	while line_obj.line[line_obj.ptr] != '\n':
		line_obj.getOutMsg()
		line_obj.getInMsg()

		if line_obj.msgPos == 1:
			if line_obj.line[line_obj.ptr].isdigit():
				j = line_obj.ptr + 1
				while line_obj.line[j].isdigit():
					j += 1
				bd._uid = int(line_obj.line[line_obj.ptr:j])
				line_obj.msgPos = 0
			else:
		  		param_end_ptr = line_obj.getOutMsgTry()
	      			assert param_end_ptr != None
				param = line_obj.line[line_obj.ptr:param_end_ptr]
				if hasattr(bd, param):
					bd._cur = getattr(bd, param)
				else:
					break
		if line_obj.msgPos == 2:
		   	bd._cur.held = line_obj.getAttrNum()
		if line_obj.msgPos == 3:
		   	bd._cur.maxheld = line_obj.getAttrNum()
		if line_obj.msgPos == 4:
		   	bd._cur.barrier = line_obj.getAttrNum()
		if line_obj.msgPos == 5:
		   	bd._cur.limit = line_obj.getAttrNum()
		if line_obj.msgPos == 6:
		   	bd._cur.failcnt = line_obj.getAttrNum()
		   		


if len(sys.argv) < 2:
	print 'Useage: \npython vz_checker.py filename'
	exit()
bd = beanData()
filename = sys.argv[1]
print 'filename is:[%s]'%(filename)
fd = open(filename)

i = 0
for line in fd:
	line_obj = Line(line)	
	splitLine(bd, line_obj)

fd.close()

print ''
print '%-50s used:[%0.3fM] max_used:[%0.3fM] limit:[%0.3fM] fail_count:[%d]'\
	%(u'Kernel Mem Info(内核态内存，不可被swap):',
	bd.kmemsize.getNum(bd.kmemsize.held, 'm'), \
	bd.kmemsize.getNum(bd.kmemsize.maxheld, 'm'), \
	bd.kmemsize.getNum(bd.kmemsize.barrier, 'm'), \
	bd.kmemsize.getNum(bd.kmemsize.failcnt, 'n'), )
print '%-50s used:[%0.3fM] max_used:[%0.3fM] limit:[%0.3fM] fail_count:[%d]'\
	%(u'Mem already allocated Info(突发内存):',
	bd.privvmpages.getNum(bd.privvmpages.held, 'm'), \
	bd.privvmpages.getNum(bd.privvmpages.maxheld, 'm'), \
	bd.privvmpages.getNum(bd.privvmpages.barrier, 'm'), \
	bd.privvmpages.getNum(bd.privvmpages.failcnt, 'n'), )
print '%-50s used:[%0.3fM] max_used:[%0.3fM] limit:[%0.3fM] fail_count:[%d]'\
	%(u'Ram actually used(实际使用的母鸡内存):',
	bd.physpages.getNum(bd.physpages.held, 'm'), \
	bd.physpages.getNum(bd.physpages.maxheld, 'm'), \
	bd.physpages.getNum(bd.physpages.limit, 'm'), \
	bd.physpages.getNum(bd.physpages.failcnt, 'n'), )
print '%-50s used:[%0.3fM] max_used:[%0.3fM] limit:[%0.3fM] fail_count:[%d]'\
	%(u'Mem (Ram + swap) used(使用的母鸡内存+swap):',
	bd.oomguarpages.getNum(bd.oomguarpages.held, 'm'), \
	bd.oomguarpages.getNum(bd.oomguarpages.maxheld, 'm'), \
	bd.oomguarpages.getNum(bd.oomguarpages.barrier, 'm'), \
	bd.oomguarpages.getNum(bd.oomguarpages.failcnt, 'n'), )
print '%-50s used:[%d] max_used:[%d] limit:[%d] fail_count:[%d]'\
	%(u'Proc Num(进程数):',
	bd.numproc.getNum(bd.numproc.held, 'n'), \
	bd.numproc.getNum(bd.numproc.maxheld, 'n'), \
	bd.numproc.getNum(bd.numproc.limit, 'n'), \
	bd.numproc.getNum(bd.numproc.failcnt, 'n'), )
print '%-50s used:[%d] max_used:[%d] limit:[%d] fail_count:[%d]'\
	%(u'TCP Socket Num(Tcp连接数):',
	bd.numtcpsock.getNum(bd.numtcpsock.held, 'n'), \
	bd.numtcpsock.getNum(bd.numtcpsock.maxheld, 'n'), \
	bd.numtcpsock.getNum(bd.numtcpsock.limit, 'n'), \
	bd.numtcpsock.getNum(bd.numtcpsock.failcnt, 'n'), )
print '%-50s used:[%d] max_used:[%d] limit:[%d] fail_count:[%d]'\
	%(u'Max SSH login Num(SSH登陆用户数):',
	bd.numpty.getNum(bd.numpty.held, 'n'), \
	bd.numpty.getNum(bd.numpty.maxheld, 'n'), \
	bd.numpty.getNum(bd.numpty.limit, 'n'), \
	bd.numpty.getNum(bd.numpty.failcnt, 'n'), )
print '%-50s used:[%0.3fM] max_used:[%0.3fM] limit:[%0.3fM] fail_count:[%d]'\
	%(u'TCP Send Buff(Tcp发送缓冲区):',
	bd.tcpsndbuf.getNum(bd.tcpsndbuf.held, 'm'), \
	bd.tcpsndbuf.getNum(bd.tcpsndbuf.maxheld, 'm'), \
	bd.tcpsndbuf.getNum(bd.tcpsndbuf.barrier, 'm'), \
	bd.tcpsndbuf.getNum(bd.tcpsndbuf.failcnt, 'n'), )
print '%-50s used:[%0.3fM] max_used:[%0.3fM] limit:[%0.3fM] fail_count:[%d]'\
	%(u'TCP Receive Buff(Tcp接收缓冲区):',
	bd.tcprcvbuf.getNum(bd.tcprcvbuf.held, 'm'), \
	bd.tcprcvbuf.getNum(bd.tcprcvbuf.maxheld, 'm'), \
	bd.tcprcvbuf.getNum(bd.tcprcvbuf.barrier, 'm'), \
	bd.tcprcvbuf.getNum(bd.tcprcvbuf.failcnt, 'n'), )
print ''
print '%-50s used:[%0.3fM] percent:[%0.3f%%]'\
	%(u'Swap(使用的Swap，越大超售越严重):',
	bd.oomguarpages.getNum(bd.oomguarpages.held - bd.physpages.held, 'm'), \
	bd.numpty.getNum(1.0 * (bd.oomguarpages.held - bd.physpages.held) / bd.oomguarpages.held * 100, 'n'))
print '%-50s used:[%0.3fM] limit:[%0.3fM]'\
	%(u'Guarantee Mem(保证内存):',
	bd.numpty.getNum(bd.oomguarpages.held * 4096 + \
						bd.kmemsize.held + \
						bd.tcpsndbuf.held + \
						bd.tcprcvbuf.held + \
						bd.othersockbuf.held + \
						bd.dgramrcvbuf.held , 'm'), \
	bd.oomguarpages.getNum(bd.oomguarpages.barrier, 'm'))
print ''








