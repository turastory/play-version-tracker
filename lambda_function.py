from argparse import ArgumentParser
import requests
import json
import boto3
import time

DEFAULT_PACKAGE = "co.riiid.vida"
SLACK_URL = "https://hooks.slack.com/services/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"
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("vida-version")
log = ""

def printToLog(string, last = False):
    global log
    log += string
    if not last:
        log += "\n"

def timestamp():
    return int(time.time())

def update_latest_version_in_db(new_version):
    printToLog("Update database")
    table.update_item(
        Key = { "id": "current_version" },
        UpdateExpression = "SET version = :newversion",
        ExpressionAttributeValues = {
            ":newversion": new_version
        }
    )

def find_after_index(html, keyword):
    index = html.find(keyword)
    if index == -1:
        return index
    else:
        return html.find(keyword) + len(keyword)

def find_end_tag_ignore_br(html, start_index):
    start = start_index
    index = start
    while True:
        index = html.index("<", start)
        br = html.index("<br>", start)
        start = br + 4
        if index != br:
            break
    return index

def find_first_body_after(html, start_index):
    index = start_index
    while True:
        start = html.index('>', index) + 1
        end = find_end_tag_ignore_br(html, start)
        body = html[start:end]
        index = end + 1
        if body:
            break
    return body.replace("<br>", "\n")

def get_package_name():
    parser = ArgumentParser()
    parser.add_argument("-p", "--package", dest="package",
                        help = "package name to find out version name")
    args = vars(parser.parse_args())
    package = args["package"]
    if package:
        return package
    else:
        printToLog("No package provided. Fall back to default.")
        return DEFAULT_PACKAGE

def find_version(body):
    index = find_after_index(body, "Current Version")
    return find_first_body_after(body, index)

def find_changelog(body):
    index = find_after_index(body, "What&#39;s New")
    if index == -1:
        return "변경 사항이 없습니다."
    else:
        return find_first_body_after(body, index)

def post_message_to_slack(package, version, changelog):
    data = {
        "text": f"`{version}` 버전이 플레이스토어에 업데이트되었습니다! <https://play.google.com/store/apps/details?id={package}|릴리즈 보러가기>",
        "attachments": [
            {
                "title": "변경 사항",
                "text": f"{changelog}"
            }
        ]
    }

    requests.post(SLACK_URL, json.dumps(data))

def get_latest_version_from_db():
    return table.get_item(Key = { "id": "current_version" })["Item"]["version"]
    

def handler_function(event, context):
    package = get_package_name()
    printToLog(f"Target package: {package}")

    body = requests.get(f"https://play.google.com/store/apps/details?id={package}").text
    version = find_version(body)
    changelog = find_changelog(body)

    prev_version = get_latest_version_from_db()
    printToLog(f"Prev version: {prev_version}")
    if prev_version != version:
        update_latest_version_in_db(version)
        post_message_to_slack(package, version, changelog)
    
    printToLog(f"Current Version: {find_version(body)}")
    printToLog(f"Changelog:")
    printToLog(f"{find_changelog(body)}", last = True)

    return log
