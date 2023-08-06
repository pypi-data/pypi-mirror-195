import ztools.nutFs.Nsp
import ztools.nutFs.Xci
import ztools.nutFs.Nca
import ztools.nutFs.Nacp
import ztools.nutFs.Ticket
import ztools.nutFs.Cnmt
import ztools.nutFs.File

def factory(name):
	if name.endswith('.xci'):
		f = nutFs.Xci.Xci()
	elif name.endswith('.xcz'):
		f = nutFs.Xci.Xci()
	elif name.endswith('.nsp'):
		f = nutFs.Nsp.Nsp()
	elif name.endswith('.nsz'):
		f = nutFs.Nsp.Nsp()
	elif name.endswith('.nsx'):
		f = nutFs.Nsp.Nsp()
	elif name.endswith('.nca'):
		f =  nutFs.Nca.Nca()
	elif name.endswith('.nacp'):
		f =  nutFs.Nacp.Nacp()
	elif name.endswith('.tik'):
		f =  nutFs.Ticket.Ticket()
	elif name.endswith('.cnmt'):
		f =  nutFs.Cnmt.Cnmt()
	else:
		f = nutFs.File.File()

	return f