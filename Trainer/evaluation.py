from training import train_rfc, train_xgb
from connector_api_service import get_training_data

definition_key = 2251799817561228

df_with_context = get_training_data(definition_key, [])
df_without_context = df_with_context.copy()

for col in df_without_context.columns:
    if col.startswith('variables'):
        df_without_context = df_without_context.drop([col], axis=1)

print('##### Random Forest #####')
print('\n')
print('-----Evaluation with context data-----')
rfc_with_context = train_rfc(df_with_context)

print('-----Evaluation without context data-----')
rfc_without_context = train_rfc(df_without_context)

print('##### XGBoost #####')
print('\n')
print('-----Evaluation with context data-----')
xgb_with_context = train_xgb(df_with_context)

print('-----Evaluation without context data-----')
xgb_without_context = train_xgb(df_without_context)
