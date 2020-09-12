1) Command to create table template_collection in database
create table template_collection(type character varying(500), entity character varying(500), customerId integer, law character varying(500), fields json []);

2) Command to insert template in table template_collection
insert into template_collection (type, entity, customerId, law, fields)	values ('system', 'entity', 1234, 'base',
	array[
	'{
		"field": "name",
		"label": "Name",
		"data_type": "short-text",
		"default": "Type name here..",
		"field_type": "basic_details",
		"field_type_label": "Basic Details",
		"is_removable": false,
		"mandatory": true
	}',
	'{
		"field": "description",
		"label": "Description",
		"data_type": "long-text",
		"default": "Type description here..",
		"field_type": "basic_details",
		"field_type_label": "Basic Details",
		"is_removable": false,
		"mandatory": false
	}',
	'{
		"field": "entity_type",
		"label": "Entity Type",
		"data_type": "options",
		"default": "",
		"field_type": "basic_details",
		"field_type_label": "Basic Details",
		"is_removable": false,
		"mandatory": false,
		"options_list": [
			"Affiliate",
			"Client",
			"Holding Company",
			"Regulatory Body",
			"Subsidiary"
		]
	}',
	'{
		"field": "location",
		"label": "Location",
		"data_type": "options",
		"default": "",
		"field_type": "basic_details",
		"field_type_label": "Basic Details",
		"is_removable": false,
		"mandatory": false,
		"options_url": {
			"url": "dm/geos",
			"request_type": "GET"
		}
	}']::json[]
);	


3) Command to get all record in table template_collection
select * from template_collection;