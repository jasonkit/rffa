import os


def prefill_envvar_for_testing(default_dict):
    for key, value in default_dict.items():
        os.environ[key] = os.getenv(key, value)


prefill_envvar_for_testing({
    'DATABASE_URL': 'postgresql://rffa:rffa@127.0.0.1:54321/rffa',
    'TEST_DATABASE_URL': 'postgresql://rffa:rffa@127.0.0.1:54321/rffa',
    'ACCESS_TOKEN_SECRET': 'secret'
})
