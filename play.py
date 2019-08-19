from argparse import ArgumentParser
import requests

DEFAULT_PACKAGE="co.riiid.vida"

def find_after_index(html, keyword):
    return html.find(keyword) + len(keyword)

def find_first_body_after(html, start_index):
    index = start_index
    while True:
        start = html.index('>', index) + 1
        end = html.index('<', start)
        body = html[start:end]
        index = end + 1
        if body:
            break
    return body

def get_package_name():
    parser = ArgumentParser()
    parser.add_argument("-p", "--package", dest="package",
                        help = "package name to find out version name")
    args = vars(parser.parse_args())
    package = args["package"]
    if package:
        return package
    else:
        print("No package provided. Fall back to default.")
        return DEFAULT_PACKAGE

package = get_package_name()
print(f"Target package: {package}")

r = requests.get(f"https://play.google.com/store/apps/details?id={package}")

index = find_after_index(r.text, "Current Version")
print(f"Current Version: {find_first_body_after(r.text, index)}")
