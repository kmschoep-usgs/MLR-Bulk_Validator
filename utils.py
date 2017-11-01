
import requests


#'http://localhost:8090/monitoringLocations/'
#'http://127.0.0.1:5000/validators/add'
#33721

def run_validate(cru_url, validator_url, last_record, counts_only):
    passed_count = 0
    failed_count = 0
    warning_count = 0
    for i in range(1, last_record):
        response = requests.get(cru_url + str(i))
        data = response.json()
        payload = {'ddotLocation': data, 'existingLocation': {}}
        validator_response = requests.post(validator_url, json=payload)
        messages = str(validator_response.content)
        if 'validation_passed_message' in messages:
            passed_count = passed_count + 1
        if 'warning' in messages:
            warning_count = warning_count + 1
            if not counts_only:
                print('legacy_location_id ' + str(i) + ': ' + messages)
        if 'fatal' in messages:
            failed_count = failed_count + 1
            if not counts_only:
                print('legacy_location_id ' + str(i) + ': ' + messages)
        recs_validated = passed_count +  warning_count + failed_count

    print('Number of records validated: ' + str(recs_validated))
    print('Number of records with fatal errors: ' + str(failed_count))
    print('Number of records with warnings: ' + str(warning_count))
    print('Number of records passed validation: ' + str(passed_count))
