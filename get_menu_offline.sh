#!/bin/bash

mysql -uroot -hlocalhost -p -N -e 'use waimai_spider; select distinct name from meituan_waimai_shop where name is not null' > meituan_shop_name.txt
mysql -uroot -hlocalhost -p -N -e 'use waimai_spider; select distinct name from eleme_shop where name is not null' > eleme_shop_name.txt
mysql -uroot -hlocalhost -p -N -e 'use waimai_spider; select distinct name from baidu_waimai_shop where name is not null' > baidu_shop_name.txt
