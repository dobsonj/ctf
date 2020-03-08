#!/bin/bash
# root@teamvm:/opt/ictf/services# ls
# 1after909      docker-compose.yml                lucy_in_the_sky_with_diamonds            strawberry_fields_forever
# come-together  everybodys_got_something_to_hide  she_came_in_through_the_bathroom_window  yellow_submarine

cd /opt/ictf/services

for i in `seq 1 20`; do
	for service in lucy_in_the_sky_with_diamonds everybodys_got_something_to_hide 1after909 come-together she_came_in_through_the_bathroom_window strawberry_fields_forever yellow_submarine; do
		rw_dir="/opt/ictf/services/${service}/rw"
		docker-compose stop ${service};
		rm ${rw_dir}/*
		docker-compose start ${service};
	done
	echo "sleeping 120 sec..."
	sleep 120
done

# This was quick and ugly. Should use swpag_client to automatically restart the services that get marked as down.

