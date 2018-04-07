#!/bin/bash

mysql -uroot -hlocalhost -p -N -e 'use waimai_spider; select poi, address from meituan_waimai_shop where poi is not null and address is not null' > meituan_poi_address.txt
#mysql -uroot -hlocalhost -p -N -e 'use waimai_spider; select distinct address from eleme_shop where menu is not null' > eleme_address.txt
#mysql -uroot -hlocalhost -p -N -e 'use waimai_spider; select distinct address from baidu_waimai_shop where menu is not null' > baidu_address.txt
