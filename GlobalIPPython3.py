"""
Global IP Locator returns geographic and connection information for an IP address,
such as city, region, country, postal code, latitude/longitude, ISP and domain name,
connection type/speed, and whether the address is a known proxy.

High-level flow of this sample:
  1. ARGS    - main reads any --flag values off the command line with argparse.
  2. INPUT   - call_api prompts for the IP address if it wasn't supplied.
  3. REQUEST - call_api builds the REST query string (license + input fields).
  4. CALL    - get_contents issues the GET request and pretty-prints the JSON response.

This sample is a thin HTTP client: it builds a query string, sends a GET request to
the Global IP Locator Cloud API, and prints the JSON response.

Reference:
  - Documentation: https://docs.melissa.com/cloud-api/global-ip/global-ip-index.html
  - Release notes: https://releasenotes.melissa.com/cloud-api/global-ip/
  - Result codes:  https://docs.melissa.com/melissa/result-codes/result-codes-index.html
"""

import json
import requests
import argparse
import urllib.parse

def main():
  """
  Entry point. Reads the optional command-line arguments, then hands control to
  call_api, which performs the actual request/response cycle.

  Recognized flags (each followed by its value, e.g. --ip "12.203.219.6"):
  --license/-l, --ip.
  Any flag not supplied is None, and call_api prompts for the IP interactively.
  """
  base_service_url = "https://globalip.melissadata.net/"
  service_endpoint = "v4/web/iplocation/doiplocation"; #please see https://www.melissa.com/developer/ip-locator for more endpoints

  # Create an ArgumentParser object
  parser = argparse.ArgumentParser(description='Global IP command line arguments parser')

  # Define the command line arguments
  parser.add_argument('--license', '-l', type=str, help='License key')
  parser.add_argument('--ip', type=str, help='IP address')

  # Parse the command line arguments
  args = parser.parse_args()

  # Access the values of the command line arguments
  license = args.license
  ip = args.ip

  # Run the lookup with whatever values were passed on the command line.
  call_api(base_service_url, service_endpoint, license, ip)

def get_contents(base_service_url, request_query):
    """
    Issues the GET request against the Global IP endpoint and pretty-prints
    the API call and the JSON response to the console.

    Args:
        base_service_url: The Global IP Cloud API base URL.
        request_query: The endpoint path plus query string built by call_api.
    """
    url = urllib.parse.urljoin(base_service_url, request_query)
    response = requests.get(url)

    # Re-serialize with indentation so the raw response is easier to read.
    obj = json.loads(response.text)
    pretty_response = json.dumps(obj, indent=4)

    print("\n=============================== OUTPUT ===============================\n")

    print("API Call: ")
    for i in range(0, len(url), 70):
        if i + 70 < len(url):
            print(url[i:i+70])
        else:
            print(url[i:len(url)])
    print("\nAPI Response:")
    print(pretty_response)

def call_api(base_service_url, service_endpoint, license, ip):
    """
    Drives the interactive/CLI loop: gathers the IP address, builds and submits the
    REST query, prints the result, and optionally repeats for another record.

    It runs a single pass and exits when an IP was supplied on the command line.
    Otherwise it loops, asking for a new IP each pass until the user answers "N".

    Args:
        base_service_url: The Global IP Cloud API base URL.
        service_endpoint: The specific Global IP endpoint path to call.
        license: The Melissa license string sent with every request.
        ip: An IP address to test, or None to prompt for it.
    """
    print("\n=============== WELCOME TO MELISSA GLOBAL IP CLOUD API ===============\n")

    should_continue_running = True
    while should_continue_running:
        input_ip = ""

        # No IP was supplied via command line, so prompt for it.
        if not ip:
            print("\nFill in each value to see results")
            input_ip = input("IP: ")
        else:
            # The IP was supplied via command line; use it as-is.
            input_ip = ip

        # Keep prompting until a non-empty IP is entered.
        while not input_ip:
            print("\nFill in each value to see results")
            if not input_ip:
                input_ip = input("\nIP: ")

        # Map input fields to the API's expected query parameter names and
        # request a JSON response.
        inputs = {
            "format": "json",
            "ip": input_ip
        }

        print("\n=============================== INPUTS ===============================\n")
        print(f"\t   Base Service Url: {base_service_url}")
        print(f"\t  Service End Point: {service_endpoint}")
        print(f"\t                 IP: {input_ip}")

       # Create Service Call
        # Set the License String in the Request
        rest_request = f"&id={urllib.parse.quote_plus(license)}"

        # Set the Input Parameters
        for k, v in inputs.items():
            rest_request += f"&{k}={urllib.parse.quote_plus(v)}"

        # Build the final REST String Query
        rest_request = service_endpoint + f"?{rest_request}"

        # Submit to the Web Service.
        success = False
        retry_counter = 0

        while not success and retry_counter < 5:
            try: #retry just in case of network failure
                get_contents(base_service_url, rest_request)
                print()
                success = True
            except Exception as ex:
                retry_counter += 1
                print(ex)
                return

        is_valid = False;

        # If the IP came from the command line, treat this as a one-shot run rather
        # than looping for additional records.
        if ip is not None and ip != "":
            is_valid = True
            should_continue_running = False

        # Otherwise ask whether to test another record. Keep prompting until we get a
        # valid Y/N. "N" ends the program; "Y" falls through to another pass.
        while not is_valid:
            test_another_response = input("\nTest another record? (Y/N)")
            if test_another_response != '':
                test_another_response = test_another_response.lower()
                if test_another_response == 'y':
                    is_valid = True
                elif test_another_response == 'n':
                    is_valid = True
                    should_continue_running = False
                else:
                    print("Invalid Response, please respond 'Y' or 'N'")

    print("\n=============== THANK YOU FOR USING MELISSA CLOUD API ===============\n")

main()
