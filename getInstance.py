from burp import IBurpExtender
from burp import IContextMenuFactory
from java.util import ArrayList
from javax.swing import JMenuItem
import socket
from java.awt.datatransfer import StringSelection
from java.awt import Toolkit



class BurpExtender(IBurpExtender, IContextMenuFactory):

	def registerExtenderCallbacks( self, callbacks):
		self._callback = callbacks

		self._helpers = callbacks.getHelpers()

		callbacks.setExtensionName("Depth Instance Info")

		callbacks.registerContextMenuFactory(self)

		return

	def createMenuItems(self, invocation):
		self.context = invocation
		inv_context = invocation.getInvocationContext()


		if inv_context == 7:
			#not a valid menu
		    return
		menuList = ArrayList()
		menuItem = JMenuItem("Get Depth Instance", actionPerformed=self.getDepthInstance)
		menuList.add(menuItem)
		return menuList

	def getDepthInstance(self, event):
		message = []
		message = self.context.getSelectedMessages()

		try:
			httpService = message[0].getHttpService()
			host = httpService.getHost()
			try:
				ip = socket.gethostbyname(host)
			except socket.error:
				ip = 'Did Not Resolve'
				print 'host not resolved'
			protocol = httpService.getProtocol()
			port = httpService.getPort()
		except:
			print 'Could not get service details'
		instance = ip + ' / ' + ' ' + host + ' : ' + 'tcp/udp' + '/' + str(port) + '/' + protocol
		s = StringSelection(instance)
		Toolkit.getDefaultToolkit().getSystemClipboard().setContents(s, s)
		print instance
