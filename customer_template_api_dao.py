import psycopg2
from psycopg2 import extras
from db_confuguration import *
import traceback
from api_constants import *
import status
import json
import logging
logging.basicConfig()

log = logging.getLogger()
log.setLevel(logging.INFO)


class CustomerTemplateApiDao:

    def get_customer_template(self, request_config):
        cursor = None
        myConnection = None
        request_params = request_config[REQUEST_PARAMS]
        is_invalid = self.validate_request(request_params)
        if is_invalid:
            response = {
                'success': False,
                'message': "Invalid customer id passed in request: {0}. Customer id should be integer".format(
                    request_params[CUSTOMER_ID])
            }
            return json.dumps(response), status.HTTP_400_BAD_REQUEST, RESPONSE_HEADER
        try:
            myConnection = psycopg2.connect(host=DB_HOST, user=DB_USERNAME, password=DB_PASSWORD, dbname=DB_NAME)
            cursor = myConnection.cursor(cursor_factory=extras.DictCursor)
            query = "select *from template_collection where customerId = {0};".format(request_params[CUSTOMER_ID])
            log.info("Executing query to get specific customer template: {0}".format(query))
            cursor.execute(query)
            customer_template = cursor.fetchall()
            if len(customer_template) == 0:
                return "No Content", status.HTTP_204_NO_CONTENT, RESPONSE_HEADER
            response_headers = RESPONSE_HEADER
            final_response = self.format_response(customer_template[0])
            return json.dumps(final_response), status.HTTP_200_OK, response_headers
        except Exception:
            error_msg = "Error while fetching books info from db : %s" % traceback.format_exc()
            log.info(error_msg)
            raise Exception(error_msg)
        finally:
            if cursor:
                cursor.close()
            if myConnection:
                myConnection.close()

    def generate_customer_template(self, request_config):
        cursor = None
        myConnection = None
        request_params = request_config[REQUEST_PARAMS]
        is_invalid = self.validate_request(request_params)
        if is_invalid:
            response = {
                'success': False,
                'message': "Invalid customer id passed in request: {0}. Customer id should be integer".format(
                    request_params[CUSTOMER_ID])
            }
            return json.dumps(response), status.HTTP_400_BAD_REQUEST, RESPONSE_HEADER
        try:
            myConnection = psycopg2.connect(host=DB_HOST, user=DB_USERNAME, password=DB_PASSWORD, dbname=DB_NAME)
            cursor = myConnection.cursor(cursor_factory=extras.DictCursor)
            count_query = "select count(customerId) from template_collection where type = '{0}';".format(SYSTEM)
            cursor.execute(count_query)
            result_count = cursor.fetchall()
            if result_count[0][0] == 0:
                return "No Content", status.HTTP_204_NO_CONTENT, RESPONSE_HEADER
            else:
                log.info("Total no. of records present in database:{0}".format(result_count[0][0]))
                no_of_batches = int(result_count[0][0]/MAX_LIMIT) + 1
                log.info("Total no. of batches: {0}".format(no_of_batches))
                offset = INITIAL_OFFSET
                fields = []
                for batch in range(0, no_of_batches):
                    log.info("Batch: {0}".format(batch + 1))
                    log.info("Getting all templates")
                    query = "select *from template_collection where type = '{0}' LIMIT {1} OFFSET {2};".format(SYSTEM,
                                                                                                           MAX_LIMIT,
                                                                                                           offset)
                    log.info("Executing query to get all templates:%s" % query)
                    cursor.execute(query)
                    query_result = cursor.fetchall()
                    if query_result:
                        log.info("No. of records fetched: {0}".format(len(query_result)))
                        for record in query_result:
                            for field in record[4]:
                                fields.append(field)
                        offset += MAX_LIMIT
                    else:
                        log.info("No record found")
                response_headers = RESPONSE_HEADER
                db_record = [CUSTOMER, ENTITY, request_params.get(CUSTOMER_ID), BASE, fields]
                final_response = self.format_response(db_record)
                insert_query = self.get_insert_query(db_record)
                cursor.execute(insert_query)
                myConnection.commit()
                return json.dumps(final_response), status.HTTP_200_OK, response_headers
        except Exception:
            error_msg = "Error while fetching books info from db : %s" % traceback.format_exc()
            log.info(error_msg)
            raise Exception(error_msg)
        finally:
            if cursor:
                cursor.close()
            if myConnection:
                myConnection.close()

    def validate_request(self, request_params):
        customer_id = request_params.get(CUSTOMER_ID)
        try:
            id = int(customer_id)
            return False
        except Exception as e:
            log.info("Invalid customer id passed in request: {0}".format(customer_id))
            return True

    def format_response(self, db_record):
        final_response = {}
        final_response[TYPE] = db_record[0]
        final_response[ENTITY] = db_record[1]
        final_response[CUSTOMER_ID] = db_record[2]
        final_response[LAW] = db_record[3]
        final_response[FIELDS] = db_record[4]
        return final_response

    def get_insert_query(self, db_record):
        fields = []
        for field in db_record[4]:
            fields.append(json.dumps(field))
        insert_query = "insert into template_collection values ('{0}', '{1}', {2}, '{3}', array{4}::json[]);".format(
            db_record[0], db_record[1], db_record[2], db_record[3], fields)
        log.info("Executing insert query: {0}".format(insert_query))
        return insert_query
