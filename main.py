import fitbit, os, json, subprocess, signal
from datetime import date

z = fitbit.Fitbit();

def GetNumberOfWeightReadingsToday():
    # Try to read existing token pair
    try:
        token = json.load(os.environ['FITBIT_TOKEN'])
    except:
        # If not generate a new file
        # Get the authorization URL for user to complete in browser.
        auth_url = z.GetAuthorizationUri()
        print "Please visit the link below and approve the app:\n %s" % auth_url
        # Set the access code that is part of the arguments of the callback URL FitBit redirects to.
        access_code = raw_input("Please enter code (from the URL you were redirected to): ")
        # Use the temporary access code to obtain a more permanent pair of tokens
        token = z.GetAccessToken(access_code)
        # Save the token to a file
        os.environ['FITBIT_TOKEN'] = json.dump(token)

    # Sample API call
    url = '/1/user/-/body/log/weight/date/{}.json'.format(date.today().strftime('%Y-%m-%d'))
    response = z.ApiCall(token, url)

    # Token is part of the response. Note that the token pair can change when a refresh is necessary.
    # So we replace the current token with the response one and save it.
    token = response['token']
    json.dump(token, os.environ['FITBIT_TOKEN'])

    # Do something with the response
    return len(response['weight'])

while GetNumberOfWeightReadingsToday() < 1:
    # kill omxplayer playing music
    p = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE)
    out, err = p.communicate()
    for line in out.splitlines():
        if 'omxplayer' in line:
            pid = int(line.split(None, 1)[0])
            os.kill(pid, signal.SIGKILL)
