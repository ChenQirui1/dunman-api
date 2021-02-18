#google oauth api
'''
@app.route("/login")
def login():
    # Find out what URL to hit for Google login
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    # Use library to construct the request for login and provide
    # scopes that let you retrieve user's profile from Google
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)


@app.route("/login/callback")
def callback():
    # Get authorization code Google sent back to you
    code = request.args.get("code")

    # Find out what URL to hit to get tokens that allow you to ask for
    # things on behalf of a user
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]

    # Prepare and send request to get tokens! Yay tokens!
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code,
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )

    # Parse the tokens!
    client.parse_request_body_response(json.dumps(token_response.json()))

    # Now that we have tokens (yay) let's find and hit URL
    # from Google that gives you user's profile information,
    # including their Google Profile Image and Email
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)
    temp = year + "Y"
    # We want to make sure their email is verified.
    # The user authenticated with Google, authorized our
    # app, and now we've verified their email through Google!
    if userinfo_response.json().get("email_verified"):
        users_email = userinfo_response.json()["email"]
        if users_email[-7:] == "@dhs.sg":
            users_classid = userinfo_response.json()["given_name"]
            if users_classid[:3] == temp or users_classid[:5].lower() == "staff":
                unique_id = userinfo_response.json()["sub"]
                picture = userinfo_response.json()["picture"]
                users_name = userinfo_response.json()["family_name"]
            else:
                return "You are no longer from DHS!"
        else:
            return "You are not from DHS!"
    else:
        return "User email not available or not verified by Google.", 400
    users_email = userinfo_response.json()["email"]
    # Doesn't exist? Add to database
    if not User.get(unique_id):
        if users_classid[:5].lower() == "staff" or users_email in PERMS:
            User.create(unique_id, users_classid, users_name, users_email, picture, 1)
        else:
            User.create(unique_id, users_classid, users_name, users_email, picture, 0)

    user = User.get(unique_id)

    # Begin user session by logging the user in
    login_user(user)
    
    
    #for debugging
    userinfo_response = requests.get(uri, headers=headers, data=body)
    users_email = userinfo_response.json()["email"]
    print("Success!", users_email, '1')
    
    # Send user back to homepage
    return redirect(url_for("index"))
    '''

