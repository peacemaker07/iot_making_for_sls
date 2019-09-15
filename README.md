IoT Making for serverless framework
====

AWSのIoT関連をserverless frameworkを使用して構築する際の実装集

## Description

- service
  - DynamoDBのテーブル構築
  - S3 Bucketの構築
- AWS IoT
  - ルール、アクションを使用してDynamoDBへのレコード登録
  - ルール、アクションを使用してLambdaを実行
- その他
  - Lambdaからslack、LINE Notifyへ通知

## Requirement

- node 6 以上
- python3.7

## Install

### serverless framework のインストール

```
# Install the serverless cli
npm install -g serverless

# Or, update the serverless cli from a previous version
npm update -g serverless

# 参考
https://serverless.com/framework/docs/getting-started/
```

```
# プラグインをインストール
$ sls plugin install -n serverless-python-requirements
```

### deploy用のprofileを作成

```
$ aws configure --profile [任意のpfofile名(例:iot_making)]
AWS Access Key ID [None]: 任意のアクセスキー 
AWS Secret Access Key [None]: 任意のシークレットキー
Default region name [None]: ap-northeast-1
Default output format [None]: json
```

※ profile名を「iot_making」以外にした場合

serverless.ymlの「profile」を変更してください

```yaml
...
provider:
  name: aws
  runtime: python3.7
...
  profile: iot_making
...
```

### 環境変数の設定

serverless.env.yml.sampleをコピーし内容を各環境にあわせてください

```
$ cd リポジトリトップ
$ cp serverless.env.yml{.sample,}
$ vi serverless.env.yml
```

## Usage

### deploy

TODO : -sの補足を追加
TODO : S3 のprefixについて補足を追加

```
$ sls deploy -s dev -v
```

### Lambdaからslack、LINE Notifyへ通知

設定はこちら
- [[超簡単]LINE notify を使ってみる](https://qiita.com/iitenkida7/items/576a8226ba6584864d95)

## etc

### AUTH0

TODO
