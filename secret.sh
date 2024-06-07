# !/bin/bash

current_secret=$(aws secretsmanager get-secret-value --secret-id <secret-id> | jq -r '.SecretString // @csv')
echo "$current_secret"

random_string=$(openssl rand -base64 16)
echo "$random_string"

secret_dict=$(echo "$current_secret")

if [[ ${secret_dict+"${secret_dict["AUTHKEY"]}"} ]]; then
  secret_dict=$(echo "$secret_dict" | sed 's/\"AUTHKEY\":\"[^"]*\"\,/\"AUTHKEY\":\"'"$random_string"'"\,/')
else
  echo "Key 'AUTHKEY' not found in secret data."
fi

updated_secret="$secret_dict"

aws secretsmanager put-secret-value --secret-id <secret-id> --secret-string "$updated_secret"

echo "$updated_secret"
