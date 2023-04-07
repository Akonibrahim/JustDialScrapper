import requests, pprint, time, csv, sys
from conf import params, cookies, headers, json_data, params2, cookies2, headers2, json_data2
from typing import List

def get_data(city: str, nct_id: str, PHPSESSID: str) -> List[dict]:
    """
    Get data from justdial
    :param city: city name
    :param nct_id: national category id
    :param PHPSESSID: PHPSESSID
    """
    output = []
    for i in range(1, 20):
        # Get the cookies from the browser
        json_data["pg_no"] = i
        cookies["scity"] = city
        cookies2["scity"] = city
        cookies["inweb_city"] = city
        cookies2["inweb_city"] = city
        json_data["city"] = city
        
        json_data["national_catid"] = nct_id
        json_data2["ncatid"] = nct_id
        cookies["PHPSESSID"] = PHPSESSID
        cookies2["PHPSESSID"] = PHPSESSID
        

        response = requests.post(
            "https://www.justdial.com/api/resultsPageListing",
            params=params,
            cookies=cookies,
            headers=headers,
            json=json_data,
            timeout=10
        )
        
        response = response.json()
        json_data["nextdocid"] = response.get("nextdocid")

        if response.get("results"):
            for item in response.get("results").get("data"):
                if len(item) and item[0] != 'null':
                    pprint.pprint(item)
                    tmp = {}
                    tmp["name"] = item[1]
                    tmp["address"] = ",".join(item[3:5])
                    tmp["phone"] = "Cant get phone number"
                    time.sleep(1)
                    if item[15] == "":
                        json_data2["allocateid"] = item[49]
                        response = requests.post(
                            "https://www.justdial.com/api/callallocate",
                            params=params2,
                            cookies=cookies2,
                            headers=headers2,
                            json=json_data2,
                            timeout=10
                        )
                        if response.status_code == 200:
                            data = response.json().get("result")
                            if data.get("status"):
                                tmp["phone"] = data.get("vn")

                    else:
                        tmp["phone"] = item[15]
                    # print(tmp)
                    output.append(tmp)

    # Convert to csv
    file_name  = f"{city}_{nct_id}.csv"
    with open(file_name, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=output[0].keys())
        writer.writeheader()
        writer.writerows(output)

if __name__ == "__main__":
    CITY = sys.argv[1]
    NCT_ID = sys.argv[2]
    PHPSESSID = sys.argv[3]
    get_data(CITY, NCT_ID, PHPSESSID)
