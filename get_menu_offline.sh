#!/bin/bash

mysql -uroot -hlocalhost -p -N -e 'use waimai_spider; select distinct menu from meituan_waimai_shop where menu is not null limit 10000' > meituan_menu.sample
