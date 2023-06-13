#	Makefile for hw services

help:
	@echo "make install 	Install the services"
	@echo "make uninstall	Uninstall the services"
	@echo "make install-battery 	Install the battery services"
	@echo "make uninstall-battery	Uninstall the battery services"

install-battery:
	@echo "installing the battery service"
	pip install -r requirements.txt
	sudo cp batteryService/MAX17048.py /usr/local/bin/
	sudo cp batteryService/batteryService.py /usr/local/bin/
	sudo cp batteryService/batteryService.service /etc/systemd/system/

	sudo service batteryService start

uninstall-battery:
	@echo "uninstalling the battery service"
	systemctl stop batteryService.service
	sudo rm -f /usr/local/bin/MAX17048.py 
	sudo rm -f /usr/local/bin/batteryService.py 
	sudo rm -f /etc/systemd/system/batteryService/batteryService.service


install:	install-battery
	@echo "all services installed"


uninstall:	uninstall-battery
	@echo "all services installed"


