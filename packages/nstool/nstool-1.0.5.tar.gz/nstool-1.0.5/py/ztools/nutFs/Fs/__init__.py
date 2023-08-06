from ztools.Fs.Xci import Xci
from ztools.Fs.pXci import uXci
from ztools.Fs.pXci import nXci
from ztools.Fs.pXci import lXci
from ztools.Fs.Nca import Nca
from ztools.Fs.Nsp import Nsp
from ztools.Fs.Rom import Rom
from ztools.Fs.Nacp import Nacp
from ztools.Fs.Pfs0 import Pfs0
from ztools.Fs.Hfs0 import Hfs0
from ztools.Fs.Ticket import Ticket
from ztools.Fs.File import File
from ztools.Fs.ChromeNsp import ChromeNsp
from ztools.Fs.ChromeXci import ChromeXci
from ztools.Fs.ChromeNacp import ChromeNacp

def factory(name):
	if name.endswith('.xci'):
		f = Xci()
	elif name.endswith('.xcz'):
		f = Xci()		
	elif name.endswith('.nsp'):
		f = Nsp()
	elif name.endswith('.nsz'):
		f = Nsp()		
	elif name.endswith('.nsx'):
		f = Nsp()
	elif name.endswith('.nca'):
		f =  Nca()
	elif name.endswith('.ncz'):
		f =  File()		
	elif name.endswith('.nacp'):
		f =  Nacp()
	elif name.endswith('.tik'):
		f =  Ticket()
	elif name.endswith('.hfs0'):
		f =  Hfs0()		
	else:
		f = File()
	return f