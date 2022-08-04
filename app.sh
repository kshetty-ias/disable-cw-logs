export CW_LOGS=$(
    aws ssm get-parameter \
    --name "cw-logs" \
    --query "Parameter.Value" \
    --output text
)

echo $CW_LOGS