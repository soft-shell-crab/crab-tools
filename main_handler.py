# -*- coding: utf-8 -*-

import boto3
import os
def lambda_handler(event, context):

# sample from https://chiritsumo-life.com/20200920/serverless-dynamic-contents/
    
    # 環境変数
    region_name = os.environ.get('region_name')
    
    # インスタンスID一覧取得
    instance_id_list = []
    html_instance_id_list = ""
    
    ec2 = boto3.client('ec2' , region_name)
    all_info = ec2.describe_instances()
    for reservations in all_info['Reservations']:
        for instance in reservations['Instances']:
            instance_id_list.append(instance['InstanceId'])
            for instance_id in instance_id_list:
                div_instance_id = ""\
                    "<div>"\
                        f"<p><button type=\"button\" style = \"width:200px;\" onclick=test('{instance_id}')>{instance_id}</button></p>"\
                    "</div>"
    
            html_instance_id_list += div_instance_id
    # HTML構成                    
    html = ""\
        "<html lang='ja'>"\
        "<head>"\
        "<meta charset='utf-8'>"\
        "<style>"\
            ".header {color: white; background-color: grey;}"\
        "</style>"\
        "<body>"\
            "<div class='header'>"\
                "<h1>API Gateway + Lambdaのみの動的HTMLページ</h1>"\
            "</div>"\
            "<div class='main'>"\
                f"{html_instance_id_list}"\
            "</div>"\
        "<script>"\
            "function test(instance_id) {"\
                "console.log(instance_id);"\
            "};"\
        "</script>"\
        "</body>"\
        "<html>"
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "text/html"},
        "body": html
    }