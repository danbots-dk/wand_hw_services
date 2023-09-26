#	Makefile for hw services

VERSION=1.0.0-2
PKG_NAME=danbots-wand-hw-services-$(VERSION)
PKG_FOLDER=tmp/package
DEST_FOLDER=/usr/local/bin/wand-hw

help:
	@echo "make install           Install the services"
	@echo "make uninstall         Uninstall the services"
	@echo "make install-battery   Install the battery services"
	@echo "make uninstall-battery Uninstall the battery services"
	@echo "make install-imu       Install the IMU services"
	@echo "make uninstall-imu     Uninstall the IMU services"
	@echo "make install-io        Install the IO services"
	@echo "make uninstall-io      Uninstall the IO services"

install-battery:
	@echo "Installing the battery service" 
	sudo mkdir /usr/local/bin/wand/ || echo "/usr/local/bin/wand/ already exists"
	pip install -r requirements.txt
	sudo cp batteryService/MAX17048.py /usr/local/bin/wand/
	sudo cp batteryService/batteryService.py /usr/local/bin/wand/
	sudo cp batteryService/batteryService.service /etc/systemd/system/
	sudo service batteryService start

uninstall-battery:
	@echo "Uninstalling the battery service"
	systemctl stop batteryService.service
	sudo rm -f /usr/local/bin/wand/MAX17048.py 
	sudo rm -f /usr/local/bin/wand/batteryService.py 
	sudo rm -f /etc/systemd/system/batteryService.service

install-imu:
	@echo "Installing the IMU service"
	sudo mkdir /usr/local/bin/wand/ || echo "/usr/local/bin/wand/ already exists"
	pip install -r requirements.txt
	sudo cp imuService/imuService.py /usr/local/bin/wand/
	sudo cp imuService/imuService.service /etc/systemd/system/
	sudo service imuService start

uninstall-imu:
	@echo "Uninstalling the IMU service"
	systemctl stop imuService.service
	sudo rm -f /usr/local/bin/wand/imuService.py 
	sudo rm -f /etc/systemd/system/batteryService.service

install-io:
	@echo "Installing the IO service"
	sudo mkdir /usr/local/bin/wand/ || echo "/usr/local/bin/wand/ already exists"
	pip install -r requirements.txt
	sudo cp ioService/ioService.py /usr/local/bin/wand/
	sudo cp io/ioLib.py /usr/lib/python3.9/ioLib.py
	sudo cp io/tmp1075.py /usr/lib/python3.9/tmp1075.py
	sudo cp ioService/ioService.service /etc/systemd/system/
	sudo service ioService start

uninstall-io:
	@echo "Uninstalling the IO service"
	systemctl stop ioService.service
	sudo rm -f /usr/local/bin/wand/ioService.py 
	sudo rm -f /usr/lib/python3.9/ioLib.py
	sudo rm -f /usr/lib/python3.9/tmp1075.py
	sudo rm -f /etc/systemd/system/ioService.service

set_i2c:
	dtparam i2c_arm=on
	modprobe i2c-dev

pkg-copy:
	mkdir -p $(PKG_FOLDER) 
	mkdir -p $(PKG_FOLDER)/usr/local/bin/wand $(PKG_FOLDER)/etc/systemd/system/
	cp requirements.txt $(PKG_FOLDER)/usr/local/bin/wand
	cp batteryService/MAX17048.py batteryService/batteryService.py $(PKG_FOLDER)/usr/local/bin/wand
	cp batteryService/batteryService.service $(PKG_FOLDER)/etc/systemd/system/
	cp io/ioLib.py $(PKG_FOLDER)/usr/local/bin/wand
	cp io/tmp1075.py $(PKG_FOLDER)/usr/local/bin/wand

deb-pkg: pkg-copy
	cp -r -p deb-pkg/DEBIAN $(PKG_FOLDER)
	dpkg-deb --build --root-owner-group -Zxz $(PKG_FOLDER) tmp/$(PKG_NAME).deb

pkg-push:
	rcp tmp/$(PKG_NAME).deb  danbots:/var/www/apt/simple/pool/wand/
	rsh danbots /var/www/apt/simple/scan

clean-pkg:
	rm -rf $(PKG_FOLDER)
	rm -rf tmp

install: install-battery install-imu install-io
	@echo "All services installed"

uninstall: uninstall-battery uninstall-imu uninstall-io
	sudo rm -rf /usr/local/bin/wand/
	@echo "All services uninstalled"




