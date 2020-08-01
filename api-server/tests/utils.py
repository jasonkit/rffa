from fastapi.encoders import jsonable_encoder


def check_minimal_request(fn, minimal_request):
    assert all([
        fn({
            k: v for k, v in minimal_request.items() if k != key
        }).status_code == 422
        for key in minimal_request.keys()
    ])


def check_error_response(response, error):
    assert response.status_code == error.status_code
    assert response.json() == {
        'error_code': error.error_code,
        'message': error.message,
        **({
            'detail': jsonable_encoder(error.detail)
        } if error.detail is not None else {})
    }

    if error.headers is not None:
        assert([
            response.headers[k] == v
            for k, v in error.header.items()
        ])


def ensure_dict_match_model(dict_, model, keys=None, schema=None):
    if keys is None:
        keys = dict_.keys()

    if schema is None:
        assert all([
            dict_[key] == getattr(model, key)
            for key in keys
        ])
    else:
        data = jsonable_encoder(schema.from_orm(model))
        assert all([
            dict_[key] == data[key]
            for key in keys
        ])
