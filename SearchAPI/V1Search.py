# for more up to date documentation go to https://automation.trendmicro.com/xdr/home
# Tested with XDR V2.0 API, Trend Micro XDR Product Manager Team, November 2020
# Programmer:  D. Girard, Trend Micro XDR Product Manager Team, March 22nd 2021

import argparse  # for the script arguments
# import pandas as pd   # mainly for CSV flatening and export. TBD
import json      #
import tmconfig  # tmconfig.py with your api keys / token
import TMVisionOne  #Trend Micro Vision One/XDR API wrapper class
import time # for timing our script execution
from datetime import datetime, timedelta, timezone  # to calculate date and time range of the search


def optionparse():
    """Argument Parser."""
    opts = argparse.ArgumentParser(description='V1 Search Script',
                                   formatter_class=argparse.RawTextHelpFormatter)
    opts.add_argument('-d', '--days', help='Days of logs')
    opts.add_argument('-H', '--hours', help='Hours of logs')
    opts.add_argument('-m', '--minutes', help='minutes of logs')
    opts.add_argument('-l', '--datalake', help='Data Lake to query: edr, msg, net, det', default='edr')
    opts.add_argument('-q', '--query', help='XDR search query')
    opts.add_argument('-t', '--output_type', default='json', help='output to json or csv')
    opts.add_argument('-f', '--filename', help='file name for the output')
    parsed_args = opts.parse_args()
    return parsed_args

# used to validate our exported data file
def validate_json(filepath):
    try:
        with open(filepath, 'r', encoding="utf-8") as f:
            json_obj = json.load(f)
            f.close()
        print(f"{filepath} is a valid JSON file")
    except ValueError as e:
        print(f"{filepath} Not a valid JSON file.  {e}")

    finally:
        f.close()


def main(args):
    MAXEVENTS = 500 # Maximum events a search API can return
    try:
        if args.query:
            qry = args.query
            # qry = """pname:"Deep Discovery Inspector" AND NOT eventName:("PRODUCT_UPDATE" OR "PRODUCT_SUMMARY")"""
            #qry ="eventName:INTRUSION_DETECTION"
            begin = time.time()
            #change your region
            x = TMVisionOne.XDR("us", tmconfig.xdr_token, "Trend Micro Vision One Search Script Sample")
            my_date = datetime.now() - timedelta(days=int(args.days))
            istart = x.convert_DateToEpoc(str(my_date.replace(microsecond=0)))
            iEnd = x.convert_DateToEpoc(str(datetime.today().replace(microsecond=0) + timedelta(days=1)))
            ret = x.search(istart, iEnd, args.datalake, qry)
            js =json.loads(ret)
            print("*********STARTING*******************")
            total_cnt = len(js['data']['logs'])
            total_cnt = js['data']['total_count']
            print(f"Data Source : {x.dlake[args.datalake]}")
            print(f"Period from : {my_date} to {datetime.now()}")
            print(f"Query       : {qry}")
            print(f"Found       : {total_cnt}  hits")
            if total_cnt > 0:
                result = list()
                if args.filename:
                    filename = args.filename
                else:
                    filename = "query_results_" + datetime.now().strftime("%Y-%m-%dT%H-%M") + ".json"
                print(f"Records saved to : {filename}")
                js1 = js['data']['logs']
                result.append(js1)
                page_cnt = round(int(total_cnt)/MAXEVENTS)
                pages = str(page_cnt)
                for i in range(page_cnt):
                    p = i + 1
                    print(f"Page {p} of {pages}")
                    offset = (p*MAXEVENTS)
                    if offset > total_cnt:
                        break

                    ret = x.search(istart, iEnd, args.datalake, qry, offset)
                    js2 = json.loads(ret)
                    js3=js2['data']['logs']
                    result.append(js3)
                with open(filename, 'w', encoding="utf-8") as f1:
                    json.dump(result, f1,indent=4)
                    f1.close()
                validate_json(filename)
            end = time.time()
            print(f"Total runtime of the program is {round(end - begin, 2)} seconds")
            print("*********Program ended without problems**********")
        else:
            print("No query supplied, example -q 'hostName:globalnetworkissues.com OR objectIps:(204.188.205.176 OR 5.252.177.25)'")

    except Exception as err:
        print(f"main : {err}")
        exit(-1)


if __name__ == '__main__':
    args = optionparse()
    print('Welcome to Trend Micro Vision One Search script')
    print("Example :")
    print("V1Search.py  -d 1 -l edr -q 'endpointHostName:win110johnd-7001'")
    main(args)


