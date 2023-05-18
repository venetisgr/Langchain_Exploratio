import requests

def scrape_linkedin_profile(linkedin_profile_url: str, api_key: str):
    """scrape information from LinkedIn profiles,
    Manually scrape the information from the LinkedIn profile"""

    api_endpoint = "https://nubela.co/proxycurl/api/v2/linkedin"
    header_dic = {"Authorization": f'Bearer {api_key}'}

    try:
        response = requests.get(
            api_endpoint, params={"url": linkedin_profile_url}, headers=header_dic
        )
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print("couldn't retrieve information-1")
        print(e.request)
        print(e.response)
        return None,None
    

    data = response.json()
    if "code" in data:
        print("couldn't retrieve information-2")
        print(data)
        return None,None

    # data = {
    #     k: v
    #     for k, v in data.items()
    #     if v not in ([], "", "", None) #not empty info
    #     and k not in ["people_also_viewed"]
    #     #and k not in ["people_also_viewed", "certifications"]
    # }
    # if data.get("groups"):
    #     for group_dict in data.get("groups"):
    #         group_dict.pop("profile_pic_url")


    #Initialize our information dictionary
    ks = ["public_identifier","first_name","last_name", "full_name","follower_count","occupation","headline","summary","country_full_name","city","experiences","languages","accomplishment_courses","accomplishment_projects","volunteer_work",
    "certifications","phone_numbers","personal_emails","skills"]
    info = {k : "no info"for k  in ks}

    for k,v in data.items():
        if k in ks:#we keep only the fields in ks list
            if v not in ([], "", "", None): #not empty info
                info[k] = v

    #standardize experiences TODO
    #standardize accomplishment_projects TODO
    #standardize volunteer_work TODO
    #standardize skills TODO

    if info["accomplishment_courses"] != "no info":
        lst = []
        for info_dict in info["accomplishment_courses"]:
            lst.append(info_dict["name"])

    if info["certifications"] != "no info":
        lst = []
        for info_dict in info["certifications"]:
            lst.append(info_dict["name"])

    return (info,data)